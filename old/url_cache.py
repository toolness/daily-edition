import urllib2
import logging

class UrlCache(object):
    def __init__(self, storage):
        self.urls = storage

    def refresh(self, url):
        req = urllib2.Request(url)
        if url in self.urls and 'lastmod' in self.urls[url]:
            req.add_header('If-Modified-Since', self.urls[url]['lastmod'])
        try:
            logging.debug('fetching %s.' % url)
            response = urllib2.urlopen(req)
            info = {'data': response.read()}
            if 'Last-Modified' in response.info():
                info['lastmod'] = response.info()['Last-Modified']
            self.urls[url] = info
        except urllib2.HTTPError, e:
            if e.code == 304:
                logging.debug('url not modified.')
            else:
                raise
