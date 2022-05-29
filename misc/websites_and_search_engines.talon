open {user.website}: user.open_url(website)
open that:
    text = edit.selected_text()
    user.open_url(text)
{user.search_engine} hunt <user.text>$: user.search_with_search_engine(search_engine, user.text)
# example: google that
{user.search_engine} (that|this):
    text = edit.selected_text()
    user.search_with_search_engine(search_engine, text)