import requests
import redis
from functools import wraps

# Connect to the Redis server
store = redis.Redis()

def count_url_access(method):
    """ Decorator counting how many times a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        # URL not in cache, fetch the content
        html = method(url)

        # Cache the result with an expiration time of 10 seconds
        store.setex(cached_key, 10, html)

        count_key = "count:" + url
        # Increment the access count
        store.incr(count_key)

        return html
    return wrapper

@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a URL """
    res = requests.get(url)
    return res.text

if __name__ == "__main__":
    # Example usage of the decorated get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://example.com"
    html_content = get_page(url)
    print(html_content)

    # Check the number of times the URL was accessed
    count_key = "count:" + url
    access_count = store.get(count_key)
    print(f'Access count for {url}: {access_count.decode("utf-8")}')
