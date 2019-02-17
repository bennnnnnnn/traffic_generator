from traffic_generator import RandomFilesDownloader
import os
import time

if __name__ == "__main__":
    rss_feed = os.environ.get("FREEWARE_RSS_FEED", "https://www.freewarefiles.com/rss/tophundred.xml")
    download_urls = os.environ.get("DOWNLOAD_URLS", "https://speed.hetzner.de/10GB.bin,https://cdimage.debian.org/cdimage/weekly-builds/amd64/iso-dvd/debian-testing-amd64-DVD-1.iso,https://cdimage.debian.org/cdimage/weekly-builds/amd64/iso-dvd/debian-testing-amd64-DVD-2.iso,https://cdimage.debian.org/cdimage/weekly-builds/amd64/iso-dvd/debian-testing-amd64-DVD-3.iso")
    download_urls = download_urls.replace(" ", "").split(',')
    downloader = RandomFilesDownloader()
    downloader.get_download_urls_from_freewarefiles_rss(rss_location=rss_feed)
    while True:
        time.sleep(3600)
        downloader.download_list()
        downloader.set_urls()
        downloader.download_list()