import urllib
import bs4

def get_tags_for_link(link, tags):
    html = urllib.urlopen(link).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    results = {}
    for tag in tags:
        results[tag] = soup.find("meta", property=tag)
    
    return results
