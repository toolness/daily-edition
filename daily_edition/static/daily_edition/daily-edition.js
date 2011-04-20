function isUrlSafe(url) {
  if (typeof(url) != "string")
    return false;
  return (url.match("^https?://") != null);
}

var imgRemover = html.makeHtmlSanitizer(
  function(tagName, attribs) {
    if (/^img$/i.test(tagName))
      return null;
    return attribs;
  });

function safeHtml(html) {
  var out = [];
  imgRemover(html, out);
  html = out.join('');
  return html_sanitize(
    html,
    function urlPolicy(url) {
      return isUrlSafe(url) ? url : null;
    });
}

const JSON_DIR = 'json/';
const DEFAULT_JSON_FILE = JSON_DIR + 'daily-edition.json';
var jsonFile = DEFAULT_JSON_FILE;

function showError() {
  var json;

  if (jsonFile == DEFAULT_JSON_FILE)
    json = window.localStorage[DEFAULT_JSON_FILE];

  if (json)
    showContent(json);
  else {
    $("#error").show();
    $("#container").fadeIn("fast");
  }
}

function showContent(json) {
  var info;

  if (window.JSON)
    info = JSON.parse(json);
  else
    info = eval("(" + json + ");");

  $("#issue-no").text(info.id + 1);
  $("#pub-date").text(info.pubDate.join("."));

  info.authors.forEach(
    function(author) {
      if (author in info.articles)
        info.articles[author].forEach(
          function(article) {
            var div = $("#templates .article").clone();
            var date = article.pubDate.join(".");
            var title = safeHtml(article.title);
            div.find(".title .link").html(title);
            div.find(".title .link").attr("href", article.url);
            div.find(".author").text(author);
            
            var html = [];
            article.content.forEach(
              function(content) {
                if (content.type == "text/html")
                  html.push(safeHtml(content.value));
              });

            if (html.length > 0) {
              var content = div.find(".content");
              content.html(html[0]);
              if (content.get(0).firstChild.nodeType == 3)
                // The child isn't wrapped in a containing block
                // element, so do that to ensure it has some
                // padding from everything around it.
                content.html("<p>" + html[0] + "</p>");
            }
            div.find(".date").text(date);
            $("#articles").append(div);
          });
    });

  $("#container").fadeIn("fast");
}

$(window).ready(
  function() {
    var req = new XMLHttpRequest();

    var matches = location.search.match(/\?issue=([0-9]+)/);
    if (!matches)
      matches = location.hash.match(/\#issue=([0-9]+)/);
    if (matches)
      jsonFile = JSON_DIR + 'issue-' + parseInt(matches[1]) + '.json';

    req.open('GET', jsonFile);
    req.overrideMimeType('text/plain');
    req.addEventListener("error", showError, false);
    req.addEventListener(
      "load",
      function(event) {
        if (req.status != 200) {
          showError();
          return;
        }

        if (jsonFile == DEFAULT_JSON_FILE)
          window.localStorage[DEFAULT_JSON_FILE] = req.responseText;

        showContent(req.responseText);
      },
      false
    );
    req.send(null);
  });
