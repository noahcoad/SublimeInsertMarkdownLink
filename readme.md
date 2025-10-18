# Insert Markdown Hyperlink

A [Sublime Text](https://www.sublimetext.com/) Package


## Description

A more intelligent 'insert link' tool for markdown files. \
Use the hotkey (below) to insert a link. \
Uses the selected text or clipboard as title or url. \
And grabs the title from the url if available.


## Hotkey

- Command is called "Insert Markdown Hyperlink".
- I recommend mapping to <kbd>shift+command+k</kbd> on mac.
- To do that, 'Sublime Text' menu > 'Settings...' menu > 'Key Bindings' menu > and add `{ "keys": ["shift+super+k"], "command": "insert_markdown_hyperlink" }` to the right (user) side.


## General Flow

1. If cursor is over a url or a url is selected, it will be put in the url spot of the hyperlink.
2. Otherwise if a url is in the clipboard, it will be used in the url spot.
3. If text was selected, it'll be used for the title.
4. If text wasn't selected, and there was a url, and there's an active internet connection, then the title of the url will be attempted to be retrieved and used.
5. The cursor and text selected will be left in the spot that most likely needs to be updated

Just try it. Should work 'like magic' 🪄✨🙂