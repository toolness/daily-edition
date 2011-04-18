from sys import stdout
import os
import logging
import traceback
import cPickle as pickle
from datetime import date, datetime, timedelta

try:
    import json
except ImportError:
    import simplejson as json

import feedparser
from url_cache import UrlCache

AUTHORS_FILENAME = 'authors.txt'
URLS_FILENAME = 'url_cache.dat'
ARTICLES_FILENAME = 'articles.dat'
ISSUES_FILENAME = 'issues.dat'
JSON_FILENAME = 'daily-edition.json'
ISSUE_FILENAME = 'issue-%d.json'

def set_stdout(new_stdout):
    global stdout
    stdout = new_stdout

def load(filename, default):
    if os.path.exists(filename):    
        return pickle.load(open(filename, 'r'))
    return default

def save(obj, filename):
    f = open(filename, 'w')
    pickle.dump(obj, f)
    f.close()

def to_date_tuple(dt):
    return (dt.year, dt.month, dt.day)

def refresh_urls(feeds, urls):
    ucache = UrlCache(urls)
    for feed_urls in feeds.values():
        for url in feed_urls:
            try:
                ucache.refresh(url)
            except Exception, e:
                logging.error(traceback.format_exc(e))

def refresh_articles(articles, feeds, urls):
    for author, feed_urls in feeds.items():
        articles[author] = []
        relevant_urls = [url for url in feed_urls
                         if url in urls]
        for url in relevant_urls:
            stdout.write('parsing feed at %s.\n' % url)
            feed = feedparser.parse(urls[url]['data'])
            for entry in feed['entries']:
                updated = entry.get('updated_parsed')
                updated = date(year=updated.tm_year,
                               month=updated.tm_mon,
                               day=updated.tm_mday)
                content = entry.get('content', '')
                summary = entry.get('summary', '')
                summary_detail = entry.get('summary_detail', {})
                if not content:
                    if not (summary_detail and
                            summary_detail.get('value')):
                        if not summary:
                            pass
                        else:
                            content = [{'type': 'text/plain',
                                        'value': summary}]
                    else:
                        content = [summary_detail]
                if content:
                    article = {'url': entry.get('link'),
                               'title': entry.get('title'),
                               'pub_date': updated,
                               'content': content}
                    articles[author].append(article)

def normalize(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = normalize(obj[i])
    elif isinstance(obj, dict):
        for key in obj:
            obj[key] = normalize(obj[key])
    elif isinstance(obj, str):
        try:
            obj = obj.decode('utf-8')
        except UnicodeDecodeError, e:
            logging.warn('error decoding "%s" (%s).' % (repr(obj), e))
            obj = obj.decode('utf-8', 'ignore')
    return obj

def filter_articles(names, articles, issues,
                    max_articles_per_author=1,
                    min_article_word_count=50,
                    max_article_age=timedelta(days=15),
                    max_issue_word_count=2500):
    min_date = date.today() - max_article_age

    published_authors = [author for author in names
                         if author in articles]

    filtered_articles = {}
    words_left = max_issue_word_count

    total_potentials = 0
    total_articles = 0
    total_word_count = 0

    for author in published_authors:
        articles_left = max_articles_per_author
        potential_articles = [
            {'url': article['url'],
             'title': article['title'],
             'content': article['content'],
             'pubDate': to_date_tuple(article['pub_date'])}
            for article in articles[author]
            if (article['pub_date'] > min_date
                and article['url'] not in issues['urls']
                and article['url'].startswith('http'))
            ]

        total_potentials += len(potential_articles)

        for article in potential_articles:
            html = [ctype['value']
                    for ctype in article['content']
                    if ctype.get('type') == 'text/html'
                    and ctype.get('value')]
            if not html:
                logging.warn('no html content for %s.' % article['url'])
            elif len(html) > 1:
                logging.warn('multiple html found for %s.' % article['url'])
            else:
                word_count = len(html[0].split())
                if (word_count > min_article_word_count and
                    word_count < words_left):
                    if author not in filtered_articles:
                        filtered_articles[author] = []
                    total_word_count += word_count
                    total_articles += 1
                    filtered_articles[author].append(article)
                    words_left -= word_count
                    articles_left -= 1
                    if not articles_left:
                        break
                elif word_count > max_issue_word_count:
                    logging.warn(
                        'article will never be included in an '
                        'issue due to word count: %s (%d words)' % (
                            article['url'],
                            word_count
                            ))

    stdout.write('found %d articles (out of a potential %d), totalling '
                 '%d words, with contibutions by %s.\n' % 
                 (total_articles, total_potentials, total_word_count,
                 ', '.join(filtered_articles.keys())))
    return normalize(filtered_articles)

def publish_edition(people,
                    output_dir='',
                    cache_dir='',
                    update_urls=False,
                    update_articles=False,
                    authors_filename=AUTHORS_FILENAME,
                    dry_run=False):
    if update_urls:
        update_articles = True

    def cachepath(filename):
        return os.path.join(cache_dir, filename)

    names = [line.strip()
             for line in open(authors_filename, 'r').readlines()
             if line and not line.startswith('#')]

    unknown_names = []
    following = []
    for name in names:
        try:
            person = people.objects.get(name=name)
        except Exception:
            unknown_names.append(name)
            continue
        
        # Convert person record to the JSON format that
        # the rest of this legacy code expects.
        
        json_person = {
            'name': person.name,
            'sites': {}
        }
        for site in person.sites.all():
            json_person['sites'][str(site.id)] = {
                'type': site.kind,
                'url': site.url,
                'feed': site.feed,
                'title': site.title
            }
        following.append(json_person)

    if unknown_names:
        logging.warn('could not find information on: %s.' % 
                     ', '.join(unknown_names))

    feeds = {}

    for person in following:
        person_feeds = []
        for site in person['sites'].values():
            if site['type'] == 'feed':
                person_feeds.append(site['feed'])
        feeds[person['name']] = person_feeds

    urls = load(cachepath(URLS_FILENAME), {})

    if update_urls:
        refresh_urls(feeds=feeds, urls=urls)
        if not dry_run:
            save(urls, cachepath(URLS_FILENAME))

    articles = load(cachepath(ARTICLES_FILENAME), {})

    if update_articles:
        refresh_articles(articles=articles,
                         feeds=feeds,
                         urls=urls)
        if not dry_run:
            save(articles, cachepath(ARTICLES_FILENAME))

    issues = load(cachepath(ISSUES_FILENAME), {'urls': {},
                                               'pub_dates': []})

    filtered_articles = filter_articles(names=names,
                                        articles=articles,
                                        issues=issues)

    issue_id = len(issues['pub_dates'])
    issues['pub_dates'].append(datetime.now())
    for author in filtered_articles:
        for article in filtered_articles[author]:
            issues['urls'][article['url']] = issue_id
    if not dry_run:
        save(issues, cachepath(ISSUES_FILENAME))

    if not dry_run:
        blob = {'id': issue_id,
                'authors': names,
                'articles': filtered_articles,
                'pubDate': to_date_tuple(date.today())}

        json_filename = os.path.join(output_dir, JSON_FILENAME)
        issue_filename = os.path.join(output_dir,
                                      ISSUE_FILENAME % (issue_id+1))
        json.dump(blob, open(json_filename, 'w'))
        json.dump(blob, open(issue_filename, 'w'))

        stdout.write('wrote %s\n' % json_filename)
        stdout.write('wrote %s\n' % issue_filename)

parser_options = {
    ('-f', '--refresh-feeds',): 
    dict(dest='update_urls',
         help='refresh feeds',
         action='store_true',
         default=False),

    ('-p', '--reparse-feeds',): 
    dict(dest='update_articles',
         help='re-parse feeds',
         action='store_true',
         default=False),

    ('-d', '--dry-run',): 
    dict(dest='dry_run',
         help='do not write anything to disk',
         action='store_true',
         default=False),

    ('-a', '--authors-file',):
    dict(dest='authors_filename',
         help='authors filename (default is %s)' % repr(AUTHORS_FILENAME),
         default=AUTHORS_FILENAME),

    ('-c', '--cache-dir',):
    dict(dest='cache_dir',
         help='directory to store cached data in',
         default=''),

    ('-o', '--output-dir',):
    dict(dest='output_dir',
         help='directory to output issue JSON files to',
         default='')
}
