# Super Simple Wishlist
A really basic self-hosted wishlist app which renders a simple plaintext file of urls as a wishlist. Additionally, keeps track of when someone buys something for you.

![wl](https://user-images.githubusercontent.com/13795113/173165446-e1487d46-0003-40fd-98d9-19df9ac3683f.png)

# Setup
## Docker-compose
Here's a basic docker-compose snippet:
```yaml
version: "2.1"
services:
  supersimplewishlist:
    image: ghomashudson/supersimplewishlist
    container_name: supersimplewishlist
    volumes:
      - /path/to/wishlists:/usr/src/app/wishlists
      - /path/to/db.json:/usr/src/app/db.json
    ports:
      - 5000:5000
    restart: unless-stopped
```

## Manually
1. Install the python depenancies with `pip install -r requirements.txt`
2. Run the flask app with `flask run`


# How it Works
Fill the `/wishlists` directory with `wishlist_name.txt` files with one product url per line, e.g.
```
https://www.amazon.co.uk/Innovative-Designs-Mandalorian-Sticker-Stickers/dp/B087H4HZQ7
https://www.ikea.com/gb/en/p/markus-office-chair-vissle-dark-grey-30261152/
https://www.dell.com/en-uk/shop/laptop-computers-2-in-1-pcs/xps-13-9305/spd/xps-13-9305-laptop/cn93509sc11
```
An example `example_list.txt` has been provided. The products will appear in your wishlist in the same order as the txt file.

The wishlist can be viewed by going to `SERVER_URL/wishlists/wishlist_name.txt`.

It may take a few seconds to load the first time while the product details are grabbed. The product details along with the "Bought" status are saved in the `db.json` file. Item details are refreshed once a day in case of price changes.

Navigating to `SERVER_URL/wishlists/wishlist_name.txt?exclude_purchased=1` will remove products that people have bought for you. Without this a prompt `Someone may have purchaced this item` will appear, when clicking to prevent spoilers.


