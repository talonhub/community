open {user.website}: user.open_url(website)
open that: user.open_url(edit.selected_text())
open paste: user.open_url(clip.text())

{user.search_engine} hunt <user.text>$:
    user.search_with_search_engine(search_engine, user.text)
{user.search_engine} (that | this):
    text = edit.selected_text()
    user.search_with_search_engine(search_engine, text)
{user.search_engine} paste: user.search_with_search_engine(search_engine, clip.text())
