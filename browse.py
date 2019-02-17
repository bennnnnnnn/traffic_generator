from traffic_generator import WebWander
import os

if __name__ == "__main__":
    sites = os.environ.get("BROWSE_SITES", "https://reddit.com,https://digg.com,https://9gag.com,https://popurls.com")
    sites = sites.replace(" ", "").split(',')
    sites_depth = os.environ.get("SITES_DEPTH", 5)
    sites_min_wait = os.environ.get("SITES_MIN_WAIT", 1)
    sites_max_wait = os.environ.get("SITES_MAX_WAIT", 10)
    chromedriver_location = os.environ.get("CHROMEDRIVER_LOCATION", "/usr/lib/chromium/chromedriver")
    browse = WebWander(sites=sites, depth=sites_depth, min_wait=sites_min_wait, max_wait=sites_max_wait, chromedriver_location=chromedriver_location)
    browse.run_forever()