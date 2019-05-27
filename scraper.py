import json

import requests
from bs4 import BeautifulSoup

from episode import Episode

# The directory to save the episode index pages.
EPISODE_INDICES_PATH = "./pages/episodeIndices"


def nextUrlGenerator():
    """Yields URLs for each episode index page."""
    base = "https://uhhyeahdude.com/index.php"
    yield base
    # yield "https://uhhyeahdude.com/index.php/P810"

    current = 0
    while True:
        current += 15
        nextPage = f"{base}/P{current}"
        yield nextPage


def isLastPage(soup):
    """Returns True if the soup representing an episode index page is the last page.
    The last page does not have a Last page button."""

    def lastPageLink(tag):
        return tag.name == "a" and tag.string == "Last ›"

    lastPageLink = soup.find(lastPageLink)
    return lastPageLink is None


def episodeIndexPageGenerator():
    """Serves all episode index pages as Beautiful Soup"""
    url = nextUrlGenerator()
    nextUrl = next(url)
    r = requests.get(nextUrl)
    soup = BeautifulSoup(r.text, "html.parser")

    while not isLastPage(soup):
        yield nextUrl, soup

        nextUrl = next(url)
        r = requests.get(nextUrl)
        soup = BeautifulSoup(r.text, "html.parser")


def articleToEpisode(article):
    # Parse out date, episode number, link to show notes
    date = article.find("span", class_="date").string

    episodeLink = article.find("h2").find("a")
    if episodeLink is None:
        # This article is a 'Seth's clips' or something
        return None

    number = episodeLink.string
    linkToNotes = episodeLink["href"]

    return Episode(date, number, linkToNotes)


def fetchSongs(noteLink):
    r = requests.get(noteLink)
    soup = BeautifulSoup(r.text, "html.parser")

    # TODO: what happens if an episode has no intro or no outro?
    introHeading = soup.find(lambda tag: tag.name == "h3" and tag.string == "Intro")
    intro = introHeading.next_sibling.next_sibling.string

    outroHeading = soup.find(lambda tag: tag.name == "h3" and tag.string == "Outro")
    outro = outroHeading.next_sibling.next_sibling.string

    return intro, outro


def main():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Starting uhh yeah music scraper...")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    episodes = set()

    print("Part 1.\nScraping episode index pages...")
    # This collects the following episode information:
    #   - date
    #   - number
    #   - linkToNotes (this is a string url to this episode's show notes).
    pageGen = episodeIndexPageGenerator()
    for url, page in pageGen:
        print(f"On page {url}, {len(episodes)} retrieved so far.")
        articles = page.find_all("article", class_="episode")

        for article in articles:
            ep = articleToEpisode(article)
            if ep is not None:
                episodes.add(ep)

    print("...done!\n")

    print("Part 2.\nScraping show note pages...")
    # For each episode, fetch the show notes and collect song intros and outros.
    for episode in episodes:
        try:
            intro, outro = fetchSongs(episode.linkToNotes)
            print(f"{episode.number}:")
            print(f"\tintro: {intro}")
            print(f"\toutro: {outro}")
            episode.intro = intro
            episode.outro = outro
        except Exception as e:
            print("Failed to fetch songs...", e)
            continue

    # Prepare episodes for output.
    episodes = list(episodes)
    episodes.sort(key=lambda ep: ep.number)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Scraping complete! Outputting to ./uym.json")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    with open("uym.json", "w") as output:
        # dataclasses are not JSON serializable, so they must be converted to dicts.
        episodeDicts = [ep.todict() for ep in episodes]
        json.dump(episodeDicts, output, ensure_ascii=False)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("DONE!")


main()
