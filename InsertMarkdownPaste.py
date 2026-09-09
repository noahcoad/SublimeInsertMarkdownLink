import sublime
import sublime_plugin
import subprocess
import threading

PYTHON = '/opt/homebrew/bin/python3.12'
PANDOC = 'pandoc'

# Clipboard-reading logic: uses richxerox + BeautifulSoup from system Python 3.12.
# Outputs "<format>\n<content>" to stdout; exits 1 if no rich format on clipboard.
_CLIPBOARD_SCRIPT = r"""
import sys
import richxerox
from bs4 import BeautifulSoup

KEEP_TAGS = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
             'ul', 'ol', 'li', 'blockquote', 'pre', 'code',
             'strong', 'b', 'em', 'i', 'a', 'br', 'hr', 'table',
             'thead', 'tbody', 'tr', 'th', 'td'}
STRIP_TAGS = {'script', 'style', 'button', 'img', 'svg', 'input', 'form'}

def clean_html(raw):
	soup = BeautifulSoup(raw, 'html.parser')
	for tag in soup.find_all(STRIP_TAGS):
		tag.decompose()
	for tag in soup.find_all(True):
		if tag.name not in KEEP_TAGS:
			tag.unwrap()
		else:
			attrs = {'href': tag.get('href')} if tag.name == 'a' and tag.get('href') else {}
			tag.attrs = attrs
	return str(soup)

formats = richxerox.available()
if 'html' in formats:
	fmt = 'html'
	content = clean_html(richxerox.paste(format='html'))
elif 'rtf' in formats:
	fmt = 'rtf'
	content = richxerox.paste(format='rtf')
else:
	sys.exit(1)

print(fmt)
print(content, end='')
"""


class InsertMarkdownPasteCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		if sublime.platform() != 'osx':
			self.view.run_command('paste')
			return
		threading.Thread(target=self._convert_and_paste).start()

	def _convert_and_paste(self):
		try:
			r1 = subprocess.run([PYTHON, '-c', _CLIPBOARD_SCRIPT],
			                    capture_output=True, text=True)
			if r1.returncode != 0 or not r1.stdout.strip():
				sublime.set_timeout(lambda: self.view.run_command('paste'), 0)
				return

			lines = r1.stdout.split('\n', 1)
			fmt     = lines[0].strip()
			content = lines[1] if len(lines) > 1 else ''

			r2 = subprocess.run(
				[PANDOC, '-f', fmt, '-t', 'markdown', '--wrap=none'],
				input=content, capture_output=True, text=True
			)
			if r2.returncode != 0:
				sublime.set_timeout(lambda: self.view.run_command('paste'), 0)
				return

			markdown = r2.stdout.replace('\u00a0', ' ').strip()
			sublime.set_timeout(lambda: self._insert(markdown), 0)

		except Exception as e:
			msg = str(e)
			sublime.set_timeout(lambda: sublime.error_message('Insert Markdown: Paste: ' + msg), 0)

	def _insert(self, text):
		self.view.run_command('insert_markdown_paste_insert', {'text': text})


class InsertMarkdownPasteInsertCommand(sublime_plugin.TextCommand):
	def run(self, edit, text=''):
		for region in reversed(list(self.view.sel())):
			self.view.replace(edit, region, text)
