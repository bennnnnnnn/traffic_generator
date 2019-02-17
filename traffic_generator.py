import random
import subprocess
import time

import feedparser
import requests
import cssselect

from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebWander:
    def __init__(self, sites="https://reddit.com", depth=5, min_wait=1, max_wait=10, chromedriver_location="/usr/lib/chromium-browser/chromedriver"):
        if isinstance(sites, str):
            sites = [sites]
        self.sites = sites
        self.depth = depth
        if max_wait >= min_wait:
            self.max_wait = max_wait
            self.min_wait = min_wait
        else:
            raise ValueError("max_wait ({0}) has to be larger or equal to min_wait ({1})".format(max_wait, min_wait))
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chromedriver_location, chrome_options=chrome_options)

    def run_forever(self):
        while True:
            self._navigate()

    def run_once(self):
        self._navigate()

    def _navigate(self):
        site = self._get_random_site()
        print("Navigating to {0}".format(site))
        self.driver.get(site)
        for x in range(0, self.depth):
            new_site = self._get_random_hyperlink()
            if not new_site:
                print("Couldn't find any more links...navigating to different site")
                break
            print("Following hyperlink {0}".format(new_site))
            time.sleep(random.randint(self.min_wait,self.max_wait))
            self.driver.get(new_site)

    def _get_random_hyperlink(self):
        elems = self.driver.find_elements_by_css_selector('a[href^="http"]:link')
        if elems:
            return random.choice(elems).get_attribute("href")
        else:
            return None

    def _get_random_site(self):
        return random.choice(self.sites)

    def close(self):
        driver.close()


class RandomFilesDownloader:
    def __init__(self, url_list = [], wget_binary = "/usr/bin/wget"):
        self.wget_binary = wget_binary
        self.url_list = url_list

    def _get_links_from_rss(self, rss_location):
        feed = feedparser.parse(rss_location)
        rss_links = []
        for entry in feed.entries:
            rss_links.append(entry["link"])
        return rss_links

    def get_download_urls_from_freewarefiles_rss(self, rss_location="https://www.freewarefiles.com/rss/tophundred.xml"):
        rss_links = self._get_links_from_rss(rss_location)
        for rss_link in rss_links:
            print("Processing link {0}".format(rss_link))
            r = requests.get(rss_link)
            download_url = self._rreplace(r.url, "_program_", "-Download-Page-", 1)
            r = requests.get(download_url)
            tree = html.fromstring(r.content)
            if r.status_code < 200 or r.status_code >= 400:
                print("Unable to continue with url {0}".format(download_url))
                continue
            down_url_list = tree.cssselect("a.dwnlocations")

            if down_url_list:
                print("Added url {0} to list".format(down_url_list[0].get('href')))
                self.url_list.append(down_url_list[0].get('href'))
            else:
                print("Couldn't find a link for url {0}".format(download_url))
        self._shuffle_url_list()

    def _shuffle_url_list(self):
        random.shuffle(self.url_list)

    def download_list(self):
        for url in self.url_list:
            url = url.replace("https", "http")
            time.sleep(5)
            print("Downloading {0}".format(url))
            subprocess.run([self.wget_binary, "-O", "/dev/null", "-q", url])
            print("Downloaded {0}!".format(url))

    def _rreplace(self, s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def set_urls(self, urls):
        self.url_list = urls


if __name__ == "__main__":
    navigation = WebWander(sites=["https://reddit.com", "https://digg.com", "https://9gag.com"])
    navigation.run_forever()
    navigation.run_once()
    navigation.close()
    downloader = RandomFilesDownloader()
    downloader.get_download_urls_from_freewarefiles_rss(rss_location="https://www.freewarefiles.com/rss/topten.xml")
    downloader.download_list()