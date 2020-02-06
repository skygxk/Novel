import re

# get the novel name from the html
def get_name(html):
    return re.search(r'&gt;.*?&gt; <a.*?>(.*)</a> &gt;', html).group(1)

# get the title of the chapter from the html
def get_title(html):
    return re.search(r'<h1>(.*)</h1>', html).group(1)

# get the text of the chapter from the html
def get_text(html):
    text = re.search(r'<div id="content">(.*)<p>', html, re.DOTALL).group(1)
    text = re.sub(r' ', '', text, 0, re.DOTALL)
    text = re.sub('\n', '', text, 0, re.DOTALL)
    text = re.sub(r'<br/>', '', text, 0, re.DOTALL)
    text = re.sub(r'&nbsp;', '\n', text, 0, re.DOTALL)
    text = re.sub('[\r|\n]+', '\n', text)
    text = re.sub('\n', '\n    ', text, 0, re.DOTALL)
    return text

# get the url of next chapter from the html
def get_url(html):
    url = re.search(r'&rarr; <a href="(.*?)">', html).group(1)
    url = r'http://www.xbiquge.la' + url
    return url

# whether the html should be get again or not
def is_error(html):
    if r'&rarr;' in html:
        return False
    else:
        return True

# whether the next html contains a chapter or not
def is_over(html):
    return not re.search(r'.html', get_url(html))
