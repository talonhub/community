These talon files mostly match based on the URL of the target site, by looking
for the URL in the window title. However by default most browsers do not show
the URL in the title.

Browser extensions can add the URL to the win.title and thus browser.url.

Firefox:
- https://addons.mozilla.org/en-US/firefox/addon/keepass-helper-url-in-title/

Chrome:
- https://chrome.google.com/webstore/detail/url-in-title/ignpacbgnbnkaiooknalneoeladjnfgb

The scripts here look for a word with the scheme (protocol) and hostname.
Please ensure your browser extension is configured appropriately.

Alternatively if you are comfortable with using a name that's possibly more
prone to false positives, you can optionally use the commented out name-based
match that is present in many of the files.
