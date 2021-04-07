import requests
from bs4 import BeautifulSoup
import pprint


def nbr_pages(nbr_pages):
    first_page = requests.get('https://news.ycombinator.com/news')
    soup = BeautifulSoup(first_page.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')
    if nbr_pages > 1:
        for page in range(2, nbr_pages + 1):
            res = requests.get(
                'https://news.ycombinator.com/news?p=' + str(page))
            extra_soup = BeautifulSoup(res.text, 'html.parser')
            extra_link = extra_soup.select('.storylink')
            extra_subtext = extra_soup.select('.subtext')
            links = links + extra_link
            subtext = subtext + extra_subtext
    return (links, subtext)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories(list(filter(lambda item: item.get('votes') > 99, hn)))


def sort_stories(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


(mega_links, mega_subtext) = nbr_pages(2)

pprint.pprint(create_custom_hn(mega_links, mega_subtext))
