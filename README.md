# Super Simple Wishlist
A really basic self-hosted wishlist app which renders a simple plaintext file of urls as a wishlist. Additionally, keeps track of when someone buys something for you.

![wl](https://user-images.githubusercontent.com/13795113/173165446-e1487d46-0003-40fd-98d9-19df9ac3683f.png)

# Setup
## Docker-compose (WIP)
Here's a basic docker-compose snippet:
```yaml
version: "2.1"
services:
  supersimplewishlist:
    image: ghomashudson/supersimplewishlist
    container_name: supersimplewishlist
    volumes:
      - /path/to/wishlists:/usr/src/app/wishlists
      - /path/to/cache.json:/usr/src/app/.cache
    ports:
      - 5000:5000
    restart: unless-stopped
```

## Manually
1. Install the python depenancies with `pip install -r requirements.txt`
2. Run the flask app with `flask run`


