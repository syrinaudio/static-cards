import codecs
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from datetime import date

# extracts card elements and next page path from url
# returns list of Tags
def read_page(url):

    # get and ingest page
    with urlopen(url) as page:
        content = page.read()

    soup = BeautifulSoup(content, "lxml")

    # get list of all card elements
    cards = soup.find_all('div', {'class': 'grid-item'})

    # get next page path or None
    next = soup.find('a', {'class': 'w-pagination-next'})
    next = next.get('href') if next is not None else None

    return cards, next

# iterates through library pages to collect all cards
# saves cards to new syrin-library-YYYYMMDD.html file
# returns list of cards
def static_pull(url):

    # get date for filename, define url and page (count) variables
    today = date.today().strftime("%Y%m%d")
    url = url
    page = 0

    # retrieve first page
    cards, next = read_page(url)
    content = cards

    page += 1
    print(f"page {page}")

    # while there are additional pages to retrieve
    while next is not None:

        # retrieve next page and add cards to element list
        cards, next = read_page(url + next)
        for card in cards:
            content.append(card)

        page += 1
        print(f"page {page}")

    print(f"retrieved {len(content)} cards")

    # create new BeautifulSoup instance
    # append each element to instance and prettify
    html = BeautifulSoup()
    for card in content:
        html.append(card)
    html = html.prettify()

    # save BeautifulSoup instance to new file
    with open(f"syrin-library.html", "w") as file:
        file.write(html)

    print(f"saved cards to syrin-library.html")
    return content

url = 'https://syrin2.webflow.io/library/grid'
results = static_pull(url)
