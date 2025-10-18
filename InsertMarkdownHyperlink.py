import sublime
import sublime_plugin
import urllib.request
import re
import socket
import subprocess
import binascii


class InsertMarkdownHyperlinkCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		
		for region in view.sel():
			if region.empty():
				# Check if cursor is on a URL
				cursor_pos = region.begin()
				url_region = self.find_url_at_cursor(view, cursor_pos)
				
				if url_region:
					# Found URL under cursor, use it as target
					url_text = view.substr(url_region)
					title = self.get_url_title(url_text, view)
					hyperlink = "[{}]({})".format(title, url_text)
					view.replace(edit, url_region, hyperlink)
					if title:
						# Select the title text for easy editing
						title_start = url_region.begin() + 1
						title_end = title_start + len(title)
						view.sel().clear()
						view.sel().add(sublime.Region(title_start, title_end))
					else:
						new_pos = url_region.begin() + 1
						view.sel().clear()
						view.sel().add(sublime.Region(new_pos, new_pos))
				else:
					# No URL under cursor, check clipboard for rich content first
					rich_content = self.get_rich_clipboard_content()
					if rich_content:
						title, url = rich_content
						hyperlink = "[{}]({})".format(title, url)
						view.insert(edit, region.begin(), hyperlink)
						new_pos = region.begin() + len(hyperlink)
						view.sel().clear()
						view.sel().add(sublime.Region(new_pos, new_pos))
					else:
						# Check plain text clipboard
						clipboard_text = sublime.get_clipboard().strip()
						if self.is_url(clipboard_text):
							title = self.get_url_title(clipboard_text, view)
							hyperlink = "[{}]({})".format(title, clipboard_text)
							view.insert(edit, region.begin(), hyperlink)
							if title:
								# Select the title text for easy editing
								title_start = region.begin() + 1
								title_end = title_start + len(title)
								view.sel().clear()
								view.sel().add(sublime.Region(title_start, title_end))
							else:
								new_pos = region.begin() + 1
								view.sel().clear()
								view.sel().add(sublime.Region(new_pos, new_pos))
						else:
							view.insert(edit, region.begin(), "[]()")
							new_pos = region.begin() + 1
							view.sel().clear()
							view.sel().add(sublime.Region(new_pos, new_pos))
			else:
				# Text is selected
				selected_text = view.substr(region)
				
				if self.is_url(selected_text):
					# Selected text is a URL, put it in parentheses with title in brackets
					title = self.get_url_title(selected_text)
					hyperlink = "[{}]({})".format(title, selected_text)
					view.replace(edit, region, hyperlink)
					if title:
						# Select the title text for easy editing
						title_start = region.begin() + 1
						title_end = title_start + len(title)
						view.sel().clear()
						view.sel().add(sublime.Region(title_start, title_end))
					else:
						new_pos = region.begin() + 1
						view.sel().clear()
						view.sel().add(sublime.Region(new_pos, new_pos))
				else:
					# Selected text is not a URL, wrap it with markdown hyperlink syntax
					# Check if clipboard contains rich content first
					rich_content = self.get_rich_clipboard_content()
					if rich_content:
						title, url = rich_content
						hyperlink = "[{}]({})".format(selected_text, url)
						view.replace(edit, region, hyperlink)
						new_pos = region.begin() + len(hyperlink)
						view.sel().clear()
						view.sel().add(sublime.Region(new_pos, new_pos))
					else:
						# Check plain text clipboard for URL
						clipboard_text = sublime.get_clipboard().strip()
						if self.is_url(clipboard_text):
							# Insert hyperlink with clipboard URL
							hyperlink = "[{}]({})".format(selected_text, clipboard_text)
							view.replace(edit, region, hyperlink)
							# Position cursor after the closing parenthesis
							new_pos = region.begin() + len(hyperlink)
							view.sel().clear()
							view.sel().add(sublime.Region(new_pos, new_pos))
						else:
							# Insert hyperlink with empty URL, cursor inside parentheses
							hyperlink = "[{}]()".format(selected_text)
							view.replace(edit, region, hyperlink)
							# Position cursor inside parentheses
							new_pos = region.begin() + len(selected_text) + 3
							view.sel().clear()
							view.sel().add(sublime.Region(new_pos, new_pos))
	
	def get_rich_clipboard_content(self):
		"""Extract title and URL from RTF or HTML clipboard content on macOS"""
		try:
			# Try HTML first (more common for web links)
			proc = subprocess.Popen(['osascript', '-e', 'the clipboard as «class HTML»'], 
				stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout, stderr = proc.communicate()
			if proc.returncode == 0 and stdout.strip():
				html_hex = stdout.decode('utf-8').strip()
				if html_hex.startswith('«data HTML') and html_hex.endswith('»'):
					hex_data = html_hex[10:-1]  # Remove «data HTML and »
					try:
						html_data = binascii.unhexlify(hex_data).decode('utf-8')
						link_match = re.search(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>', html_data, re.IGNORECASE)
						if link_match:
							return link_match.group(2).strip(), link_match.group(1)
					except:
						pass
			
			# Try RTF as fallback
			proc = subprocess.Popen(['osascript', '-e', 'the clipboard as «class RTF »'], 
				stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout, stderr = proc.communicate()
			if proc.returncode == 0 and stdout.strip():
				rtf_data = stdout.decode('utf-8').strip()
				url_match = re.search(r'\\field.*?HYPERLINK "([^"]+)"', rtf_data)
				text_match = re.search(r'\\fldrslt\s*([^}]+)', rtf_data)
				if url_match and text_match:
					return text_match.group(1).strip(), url_match.group(1)
		except:
			pass
		return None

	def is_url(self, text):
		"""Simple URL detection"""
		return text.startswith(('http://', 'https://', 'ftp://', 'www.'))
	
	def find_url_at_cursor(self, view, cursor_pos):
		"""Find URL boundaries around cursor position"""
		line = view.line(cursor_pos)
		line_text = view.substr(line)
		cursor_col = cursor_pos - line.begin()
		
		# Find start of URL (go backward to start of line or first non-URL char)
		start_col = cursor_col
		while start_col > 0 and self.is_url_char(line_text[start_col - 1]):
			start_col -= 1
		
		# Find end of URL (go forward to end of line or first non-URL char)
		end_col = cursor_col
		while end_col < len(line_text) and self.is_url_char(line_text[end_col]):
			end_col += 1
		
		# Check if we found a valid URL
		if start_col < end_col:
			url_text = line_text[start_col:end_col]
			if self.is_url(url_text):
				return sublime.Region(line.begin() + start_col, line.begin() + end_col)
		
		return None
	
	def is_url_char(self, char):
		"""Check if character is valid in URL"""
		return char.isalnum() or char in '.-_~:/?#[]@!$&\'()*+,;=%'
	
	def get_url_title(self, url, view):
		"""Fetch HTML title from HTTP/HTTPS URL"""
		if not url.startswith(('http://', 'https://')) or not self.has_internet():
			return ""
		
		try:
			view.set_status('finding_title', 'Loading URL Title...')
			opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
			req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
			with opener.open(req, timeout=5) as response:
				html = response.read().decode('utf-8', errors='ignore')
				match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
				view.erase_status('finding_title')
				if match: return match.group(1).strip()
		except:
			pass

		view.erase_status('finding_title')
		return ""
	
	def has_internet(self):
		"""Quick check for internet connectivity"""
		try:
			socket.create_connection(("8.8.8.8", 53), timeout=0.5)
			return True
		except:
			return False