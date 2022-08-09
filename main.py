import os

import bs4
import requests
import tqdm
from urlextract import URLExtract

base_url = "http://www.watch-movies.xyz/tv-show/sarabhai-vs-sarabhai/"

# get the page
page = requests.get(base_url)
soup = bs4.BeautifulSoup(page.text, "html.parser")

# get the 'episode__body' class:
episodes = soup.find_all(class_="episode__body")

# get href in a tag for all episodes:
base_links = []
for episode in episodes:
    base_links.append(episode.a['href'])

first_level_links = []
for episode in tqdm.tqdm(base_links):
    page = requests.get(episode)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    # episode__player class:
    player = soup.find(class_="episode__player")
    # get the 'src' attribute in iframe:
    first_level_links.append(player.iframe['src'])

download_links = []

for link in tqdm.tqdm(first_level_links):
    page = requests.get(link)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    # get id 'playlist1' in class 'embedded clear-adblock':
    player = soup.find(id="playlist1")
    # get 'data-video-source' attribute in li tag:
    download_links.append(player.li['data-video-source'])

os.mkdir("episodes")

counter = 0

for download_link in tqdm.tqdm(download_links):
    # extract url from download_link:
    extractor = URLExtract()
    url = extractor.find_urls(download_link)[0]
    # download the video:
    with open(f'./episodes/{counter}.mp4', 'wb') as f:
        f.write(requests.get(url).content)
        counter += 1

print("Done!")
