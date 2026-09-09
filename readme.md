# Insert Markdown

A [Sublime Text](https://www.sublimetext.com/) Package


## Description

Markdown authoring helpers, all under the "Insert Markdown:" command prefix.

- **Insert Markdown: Link** — a more intelligent 'insert link' tool. \
  Uses the selected text or clipboard as title or url. \
  And grabs the title from the url if available.
- **Insert Markdown: Paste** — paste rich clipboard content (HTML/RTF) converted to Markdown.


## Commands & Hotkeys

| Command Palette | Command id | Suggested key (mac) |
|---|---|---|
| Insert Markdown: Link | `insert_markdown_link` | <kbd>shift+command+k</kbd> |
| Insert Markdown: Paste | `insert_markdown_paste` | <kbd>shift+command+v</kbd> |

To bind them: 'Sublime Text' menu > 'Settings...' > 'Key Bindings', and add to the right (user) side:

```json
{ "keys": ["shift+super+k"], "command": "insert_markdown_link" },
{ "keys": ["shift+super+v"], "command": "insert_markdown_paste" },
```


## Insert Markdown: Link — General Flow

1. If cursor is over a url or a url is selected, it will be put in the url spot of the hyperlink.
2. Otherwise if a url is in the clipboard, it will be used in the url spot.
3. If text was selected, it'll be used for the title.
4. If text wasn't selected, and there was a url, and there's an active internet connection, then the title of the url will be attempted to be retrieved and used.
5. The cursor and text selected will be left in the spot that most likely needs to be updated
6. Will also use HTML or RTF links in the clipboard and populate both the title and URL from those
7. A line or selection of the form `title, URL` or `title URL` becomes `[title](URL)`

Just try it. Should work 'like magic' 🪄✨🙂


## Insert Markdown: Paste — Requirements

macOS only (falls back to a normal paste elsewhere). Reads the rich clipboard with system
Python and converts it with [Pandoc](https://pandoc.org/):

```bash
brew install pandoc
pipi richxerox beautifulsoup4
```

The interpreter and pandoc paths are the `PYTHON` / `PANDOC` constants at the top of
`InsertMarkdownPaste.py`.


## Also

Check out my other [Sublime Text packages](https://gist.github.com/noahcoad/712ba4e38467f5126eb8cedd9ecbc842)
