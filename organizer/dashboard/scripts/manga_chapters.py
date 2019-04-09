#!/usr/bin/env python3


import urllib.request
import re
from bs4 import BeautifulSoup as BS


def get_manga(manga_name):  # gets the first link that matches the words specified
    url = 'https://readms.net/'
    hdr = {'User-Agent': 'Mozilla/5.0'}  # we need to use a header because we get a 403 HTTP error
    request = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(request)
    soup = BS(page, 'html.parser')
    links_in_page = soup.find_all('a')  # all <a> tags in the page
    for link in str(links_in_page).split(','):
        if re.match('.*/r/{}.*'.format(manga_name), link, re.IGNORECASE):
            link_manga = link.strip()  # we keep the first result only, since it's the latest
            return link_manga
    else:
        return None


def parse_link(link_manga):  # gets the name, chapter and the date from the link
    link_regex = '<a href="/r/.*right">(.*)</span>(.*</i>)*(.*)<strong>(.*)</strong>.*<em>(.*)</em></a>'
    link_search = re.search(link_regex, link_manga, re.IGNORECASE)
    if link_search:
        published_date = link_search.group(1)
        manga = link_search.group(3)
        chapter = link_search.group(4)
        title = link_search.group(5)
        mangas = 'Manga: {};Chapter: {} - {}; Released: {};'.format(manga.strip(),
                                                               chapter,
                                                               title,
                                                               published_date,
                                                               )
    else:
        mangas = ""

    return mangas


def main():
    mangas = ''
    for manga_name in ['One Piece', 'Fairy Tail', 'Boruto', 'OnePunch Man']:
        if get_manga(manga_name.replace(' ', '_')):
            manga_details = parse_link(get_manga(manga_name.replace(' ', '_')))
            if manga_details and re.match('.*Released: .*day.*', manga_details, re.IGNORECASE):
                mangas += manga_details
    print(mangas)

if __name__ == "__main__":
    main()
