'''Simple Wishlist App'''
from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from requests_html import HTMLSession
from pathlib import Path
import re
import json
import os
import glob

CACHE_FILENAME = ".cache"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    "referer": "https://www.google.com"
}

app = Flask(__name__)
scheduler = APScheduler()
session = HTMLSession()

def get_details(url):
    item_details = {"url": url}

    r = session.get(url, headers=headers)
    if "amazon.co" in url:
        item_details["name"] = r.html.find('#productTitle', first=True).full_text.strip()
        item_details["price"] = re.search("\£[0-9]+\.[0-9]+",r.html.text).group()
        try:
            item_details["image"] = r.html.find("#landingImage",first=True).attrs["src"]
        except:
            pass
    else:

        # Get meta data
        metadata = {}
        for meta_tag in r.html.xpath("//meta[@property]"):
            metadata[meta_tag.xpath(".//@property")[0]] = meta_tag.xpath(".//@content")[0]

        if "og:title" in metadata:
            item_details["name"] = metadata["og:title"]
        else:
            item_details["name"] = r.html.element("title").text()

        if "og:description" in metadata:
            item_details["description"] = metadata["og:description"]

        if "og:image" in metadata:
            item_details["image"] = metadata["og:image"]

        try:
            item_details["price"] = re.search("\£[0-9]+\.[0-9]+",r.html.text).group()
        except:
            try:
                item_details["price"] = re.search("\$[0-9]+\.[0-9]+",r.html.text).group()
            except:
                pass

    return item_details


@app.route("/")
def list_wishlists():
    wishlists = list(glob.glob("wishlists/*.txt"))
    wishlists = [os.path.split(w)[1] for w in wishlists]
    return render_template("wishlist_dir.html", wishlists=wishlists)


@app.route("/bought", methods=['POST'])
def bought():
    url = request.get_json(force=True)["url"]
    cache = json.load(open(CACHE_FILENAME))
    cache[url]["bought"] = True
    json.dump(cache, open(CACHE_FILENAME, 'w'))
    return "Success", 200


@app.route("/wishlist/<path:wishlist_path>")
def wishlist(wishlist_path):
    if os.path.exists(CACHE_FILENAME):
        cache = json.load(open(CACHE_FILENAME))
    else:
        cache = {}

    urls = open(os.path.join("wishlists",wishlist_path)).read().splitlines()
    items = []
    for url in urls:
        if url in cache:
            item = cache[url]
        else:
            item = get_details(url)
            cache[url] = item

        if not(request.args.get("exclude_purchased") and item.get("bought")):
            items.append(item)



    # Save out
    json.dump(cache, open(CACHE_FILENAME, 'w'))

    wishlist_name = Path(wishlist_path).stem.replace("_", " ").title()

    return render_template("wishlist.html", items=items, wishlist_name=wishlist_name)


@scheduler.task('cron', id='refresh_cache', hour='4', misfire_grace_time=900)
def updateDetails():
    '''Refresh item details in case of price change'''
    app.logger.info("Beginning Cache update...")
    cache = json.load(open(CACHE_FILENAME))
    for url in cache:
        bought = cache[url]["bought"]
        cache[url] = get_details(url)
        cache[url]["bought"] = bought
    json.dump(cache, open(CACHE_FILENAME, 'w'))
    app.logger.info("Cache update complete")

scheduler.init_app(app)
scheduler.start()

if __name__ == "__main__":
    # app.run()
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0')
