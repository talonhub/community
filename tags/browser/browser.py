from urllib.parse import urlparse

from talon import Context, actions

ctx = Context()
ctx.matches = r"""
tag: browser
"""


def is_url(url):
    try:
        # Valid if url successfully parsed
        result = urlparse(url)
        # and contains both scheme (e.g. http) and netloc (e.g. github.com)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@ctx.action_class("browser")
class BrowserActions:
    def address():
        # Split title by space, check each token and token[1: -1] (it might be in brackets) for valid url.
        # Prioritize last one if multiple are valid, return empty string if none is valid.
        tokens = (
            url[1:-1] if not is_url(url) else url
            for url in reversed(actions.win.title().split(" "))
        )
        return next((url for url in tokens if is_url(url)), "")
