Some of the files (e.g. github.talon) use a browser.host matcher. These talon files should work out of the box for Safari and Chrome on Mac, but require additional configuration on other browsers/operating systems. `knasuj_talon` is set up so that if a URL is found in the titlebar of an application matching the 'browser' tag it will be used to populate the browser.host matcher (see `code/browser.py`). This probably means that you will need an extension to make the browser.host based scripts work.

Browser extensions that can add the protocol and hostname or even the entire URL to the window title:

Firefox:
- https://addons.mozilla.org/en-US/firefox/addon/keepass-helper-url-in-title/

Chrome:
- https://chrome.google.com/webstore/detail/url-in-title/ignpacbgnbnkaiooknalneoeladjnfgb
