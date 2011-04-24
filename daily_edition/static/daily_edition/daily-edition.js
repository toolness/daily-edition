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

function showContent(info) {
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

$(window).ready(function() {
  showContent(issueData);
});
