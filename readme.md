# Insert Markdown Hyperlink

A more intelligent 'insert link' tool for markdown files.

## General Flow
1. If cursor is over a url or a url is selected, it will be put in the url spot of the hyperlink.
2. Otherwise if a url is in the clipboard, it will be used in the url spot.
3. If text was selected, it'll be used for the title.
4. If text wasn't selected, and there was a url, and there's an active internet connection, then the title of the url will be attempted to be retrieved and used.
5. The cursor and text selected will be left in the spot that most likely needs to be updated

## Recommended Hotkey

    { "keys": ["shift+super+k"], "command": "insert_markdown_hyperlink" }
