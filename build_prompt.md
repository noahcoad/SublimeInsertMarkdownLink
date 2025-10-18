started 2025-10-10 w Amazon Q CLU
Create a Sublime Text plugin that provides a hotkey to insert a hyperlink in markdown.
See `~/code/prj/sublime/` for exampls of other subline plugins I've written.
And read  `https://www.sublimetext.com/docs/api_reference.html` for sublime API.
Remember that Sublime uses Python 3.3

## flow
1. User presses cmd+K
2. if text is selected in editor, surreound with markdown hyperlink syntax brackets `[text]()` add parenthasis, and set cursor inside parenthasis
3. if there is a hyperlink already in the clipboard, put that link inside the parenthasis and set cursor after the close parenthasis
4. if there is no selected text, but there is a url in the clipboard, then insert `[](url)` and set cursor inside the square brackets
5. if there is nothing selected and no URL in clipboard, then insert `[]()` but set cursor inside square brackets
6. if a url is selected on command invocation, ignore what's in the clipboard and add `[](url)` w the url inside paranthasis and cursor in square brackets
7. check the text under the cursor and go backward to start of line or first non-URL character and same to the right (EOL or non-URL character), and if it finds it's a URL the cursor is on, then use that as the target URL
8. if there was a URL under cursor, selected, or in clipboard and the user hadn't selected other text to be the title of the URL, then after updating the text as per previous rules, then if an HTTP/HTTPS url pull a request on it to see if we can get and html title tag and use that as the default text and select that text (so user can easily change if needed) .. if there are redirects follow those till landing on the target page

## coding guidelines
read `~/code/conf/dot/aws/amazonq/cli-agents/coder.md` for coding guidelines
don't add error checking

## test playground
Sublime API Reference
https://www.sublimetext.com/docs/api_reference.html

[Sublime API Reference](https://www.sublimetext.com/docs/api_reference.html)

## Noah's Notes
https://sublimetext-markdown.github.io/MarkdownEditing/
https://math2001.github.io/MarkdownLivePreview/
https://github.com/jonschlinkert