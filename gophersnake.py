#!/usr/bin/env python3
# coding=utf-8
#
# Gophersnake: stand-alone Gopher client for modern desktops
# Copyright 2016-2018 Felix Pleșoianu <https://felix.plesoianu.ro/>
# IPv6 support by madscientistninja <https://github.com/madscientistninja>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function

import webbrowser
import socket
from threading import Thread
import sys
from io import BytesIO

if sys.version_info.major >= 3:
	from urllib.parse import urlparse
	
	from tkinter import *
	from tkinter import ttk
	from tkinter.simpledialog import askstring
	from tkinter.messagebox import showinfo, showerror
	from tkinter.filedialog import askopenfilename, asksaveasfilename
else:
	from urlparse import urlparse
	
	from Tkinter import *
	import ttk
	from tkSimpleDialog import askstring
	from tkMessageBox import showinfo, showerror
	from tkFileDialog import askopenfilename, asksaveasfilename

about = """Gophersnake version 2016-08-29, running on Python %d.%d.%d
Created by Felix Pleşoianu and offered under the MIT License.
See the source code for full text.""" % (
	sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

entry_types = {"0": "[TXT]", "1": "[DIR]", "2": "[CSO]", "3": "[ERR]",
	"4": "[HEX]", "5": "[ARC]", "6": "[ENC]", "7": "[QRY]",
	"8": "[TLN]", "9": "[BIN]", "g": "[GIF]", "h": "[HTM]",
	"i": "", "I": "[IMG]", "s": "[SND]", "M": "MIME?", "d": "[PDF]"}

icon_data = {}
icon_data["Back"] = """
R0lGODlhGAAYAIABAAAAAP///yH5BAEKAAEALAAAAAAYABgAAAJKjI+py+0GwHMxzlXjTTXEfVRG
dB0VkqUVUimqalTlEQXVfKT4ke5GFKj4IobKLnKoKF4pRAXBzCgqhoivEoj4AqltIOMNRMJkXwEA
Ow==
"""
icon_data["Forward"] = """
R0lGODlhGAAYAIABAAAAAP///yH5BAEKAAEALAAAAAAYABgAAAJJjI+py+0KwHMxTlbjVTHUjURG
pWRmhVTIeSrVEV1IZUQyUgXRjZj8YfoFKoHIr2JgmRQVhDKDqPAihsovEqgITcJApmuIgMe8AgA7
"""
icon_data["Home"] = """
R0lGODlhGAAYAIABAAAAAP///yH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEKAAEALAAAAAAYABgA
AAJ1jI8BkO231psmRuqiiRhFFGFG1ERYhCBRikQsEr3Rm0ZpRLPREeVvFLAAfAhhQJg7CFOLpGFB
WzgDC9oCYUEsaIuDEHBY0BaHhWFxWNAWh4VhcVjQFoeFYXFY0BaHhWFxsECzcLBgsHCwQPMFYMCY
I4QglFIAADs=
"""
icon_data["Reload"] = """
R0lGODlhGAAYAIABAAAAAP///yH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEKAAEALAAAAAAYABgA
AAJNjI+py+0PowO0WtuuvoxCylAQxVAOEFABoFCOplCPtVAQxVBRQ+0MFQEEhsQhpYgkUpJDChNJ
eVKeRcpzgwVQsxei9wsOi8fksvl8LgAAOw==
"""
icon_data["Bookmark"] = """
R0lGODlhGAAYAIABAAAAAP///yH5BAEKAAEALAAAAAAYABgAAAJKjI+py+0PgZxUwooBlExCyUiQ
xEiQxEiQxEiQxEiQxEiQxEiQdEiHBJEYKAYJRBLABCSQiqECoSAokIliApEwJBCAAwAJi8dkRgEA
Ow==
"""
icon_data["Menu"] = """
R0lGODlhGAAYAIABAAAAAP///yH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEKAAEALAAAAAAYABgA
AAImhI+py+0Po5yh2ouz3rz7D2LTSJbmOVnqyrbuC8fy7KL2jecJDRcAOw==
"""

home_dir = [('i', 'Welcome to Gophersnake, a simple client for the Gopher protocol.', 'fake', '(NULL)', '0'),
	('i', 'Here are some good starting points for surfing Gopherspace:', 'fake', '(NULL)', '0'),
	('1', 'gopher.floodgap.com', '', 'gopher.floodgap.com', '70'),
	('i', '(Gopher software, advocacy, search engine.)', 'fake', '(NULL)', '0'),
	('1', 'gopher.quux.org', '', 'gopher.quux.org', '70'),
	('i', '(gopher.quux.org is sort of an Internet archival server)', 'fake', '(NULL)', '0'),
	('1', 'The Online Book Initiative', '', 'gopher.std.com', '70'),
	('i', '(A huge archive of freely redistributable texts.)', 'fake', '(NULL)', '0'),
	('1', 'SDF Public Access UNIX System', '', 'sdf.org', '70'),
	('i', '(Old UNIX shell account provider)', 'fake', '(NULL)', '0'),
	('1', 'SDF Europe', '', 'sdf-eu.org', '70'),
	('i', '(European branch of the same)', 'fake', '(NULL)', '0'),
	('1', 'The Interactive Fiction Archive', '/if-archive', 'gopher.feedle.net', '70'),
	('i', '--------', 'fake', '(NULL)', '0'),
	('h', 'Gophersnake on GitHub', 'URL:https://github.com/felixplesoianu/gophersnake', '(NULL)', '0'),
	('i', 'Feel free to open an issue.', 'fake', '(NULL)', '0'),
	('h', 'Wikipedia page on gophersnakes', 'URL:http://en.wikipedia.org/wiki/Gophersnake', '(NULL)', '0'),
	('i', "(Yes, it's a real animal.)", 'fake', '(NULL)', '0'),
	('h', "Author's website", 'URL:http://felix.plesoianu.ro/', '(NULL)', '0')]

raw_data = b""
location = ""
history = []
dir_entries = []
cache = {}

def entry2url(e):
	#type label selector host port
	if e[0] == "h" and e[2].startswith("URL:"):
		return e[2][4:]
	elif len(e) < 5:
		return str(e)

	if e[4] == "70":
		port = ""
	else:
		port = ":" + str(e[4])

	if is_it_ipv6(e[3], port, True):
		if (e[2] == ""):
			return "gopher://%s%s" % (("["+e[3]+"]"), port)
		else:
			return "gopher://%s%s/%1s%s" % (
				("["+e[3]+"]"), port, e[0], e[2])
	else:
		if e[2] == "":
			return "gopher://%s%s" % (e[3], port)
		else:
			return "gopher://%s%s/%1s%s" % (e[3], port, e[0], e[2])

def str2entry(line):
	line = line.strip()
	if len(line) == 0:
		return None
	elif len(line) == 1 and line[0] == ".":
		return None
	else:
		return (line[0],) + tuple(line[1:].rstrip().split("\t"))

def parse_bytes(data):
	del dir_entries[:] #dir_entries.clear()
	for i in data.decode(encoding="latin_1").split("\r\n"):
		e = str2entry(i)
		if e != None:
			dir_entries.append(e)

def parse_file(filename):
	with open(filename, "r") as f:
		for i in f:
			yield (i[0],) + tuple(i[1:].rstrip().split("\t"))

def write_to_file(filename, entries):
	with open(filename, "w", newline="\r\n") as f:
		for i in entries:
			print("%s%s\t%s\t%s\t%s" % i, file=f)

def is_it_ipv6(host, port, nodnslookup):
	if nodnslookup:
		try:
			socket.inet_pton(socket.AF_INET6, str(host))
		except socket.error:
			return False
		return True
	else:
		try:
			socket.inet_pton(
				socket.AF_INET6,
				socket.getaddrinfo(host, port)[0][4][0])
		except socket.error:
			return False
		return True

def fetch_data(selector, host, port):
	#global raw_data
	if is_it_ipv6(host, port, False):
	    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	    sock.connect((host, port))
	    sock.sendall((selector + "\r\n").encode())
	else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.sendall((selector + "\r\n").encode())
	#raw_data = b""
	data = sock.recv(1024)
	while data:
		#raw_data += data
		yield data
		data = sock.recv(1024)
	
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()
	#yield False

top = Tk()
top.title("Gophersnake")

toolbar = ttk.Frame(top)
toolbar.pack(side=TOP, fill="x", padx=4, pady=4)

icons = {}

buttons1 = [("Back", "back-icon.gif"),
	#("Forward", "forward-icon.gif"),
	("Home", "home-icon.gif")]
buttons2 = [("Reload", "reload-icon.gif"),
	("Bookmark", "bookmark-icon.gif")]
all_buttons = {}

def add_buttons(buttons):
	def show_help(e):
		statusbar["text"] = e.widget["text"]
	for lbl, img in buttons:
		button = ttk.Button(toolbar, text=lbl)
		#icons[lbl] = PhotoImage(file=img)
		icons[lbl] = PhotoImage(data=icon_data[lbl])
		button["image"] = icons[lbl]
		button.pack(side=LEFT)
		all_buttons[lbl] = button
		button.bind("<Enter>", show_help)

add_buttons(buttons1)

address = StringVar()
address_bar = ttk.Entry(toolbar, textvariable=address)
address_bar.pack(
	side=LEFT, fill="x", padx=4, ipadx=8, ipady=8, expand=TRUE)

add_buttons(buttons2)

main_menu = Menu(top, tearoff=0)
main_menu.add_command(label="About...", underline=0,
	command=lambda:show_about())
main_menu.add_separator()
main_menu.add_command(
	label="Open as page...", underline=0, accelerator="Ctrl-O",
	command=lambda: open_as_directory())
main_menu.add_command(
	label="View source...", underline=0, accelerator="Ctrl-U",
	command=lambda: open_text_viewer(
		location, raw_data.decode(encoding="latin_1")))
main_menu.add_command(
	label="Save page as...", underline=0, accelerator="Ctrl-S",
	command=lambda: save_directory_as())
main_menu.add_separator()
main_menu.add_command(label="History", underline=0, state="disabled")
main_menu.add_command(label="Bookmarks", underline=0, state="disabled")
main_menu.add_separator()
main_menu.add_command(
	label="Quit", underline=0, accelerator="Ctrl-Q", command=top.destroy)

menu_button = ttk.Menubutton(
	toolbar, text="Menu", menu=main_menu)
#menu_icon = PhotoImage(file="menu-icon.gif")
menu_icon = PhotoImage(data=icon_data["Menu"])
menu_button["image"] = menu_icon
menu_button.pack(side=LEFT)

main_pane = Frame(top)
main_pane.pack(side=BOTTOM, fill="both", expand=TRUE)

viewport = ttk.Treeview(main_pane,
	columns="type label", show="headings",
	height=25, selectmode="browse")
viewport.column("type", width=48, minwidth=48)
viewport.column("label", width=720)
viewport.grid(row=0, column=0, sticky=(N, S, E, W))
viewport.heading("type", anchor="e")
viewport.tag_configure("0", foreground="blue", font="TkFixedFont")
viewport.tag_configure("1", foreground="blue", font="TkFixedFont")
viewport.tag_configure("3", foreground="red")
viewport.tag_configure("5", foreground="blue", font="TkFixedFont")
viewport.tag_configure("7", foreground="blue", font="TkFixedFont")
viewport.tag_configure("9", foreground="blue", font="TkFixedFont")
viewport.tag_configure("g", foreground="blue", font="TkFixedFont")
viewport.tag_configure("h", foreground="blue", font="TkFixedFont")
viewport.tag_configure("i", font="TkFixedFont")
viewport.tag_configure("I", foreground="blue", font="TkFixedFont")
viewport.tag_configure("M", font="TkFixedFont")
viewport.tag_configure("d", foreground="blue", font="TkFixedFont")

scroll = ttk.Scrollbar(
	main_pane, orient=VERTICAL, command=viewport.yview)
viewport["yscrollcommand"] = scroll.set
scroll.grid(row=0, column=1, sticky=(N, S))

statusbar = ttk.Label(main_pane)
statusbar.grid(row=1, column=0, sticky=(E, W))

grip = ttk.Sizegrip(main_pane)
grip.grid(row=1, column=1, sticky=(S, E))

main_pane.rowconfigure(0, weight=1)
main_pane.columnconfigure(0, weight=1)

top.bind("<Control-l>", lambda e: address_bar.focus())
top.bind("<Control-r>", lambda e: reload_command(location))
top.bind("<F5>", lambda e: reload_command(location))
top.bind("<Control-o>", lambda e: open_as_directory())
top.bind("<Control-u>",
	lambda e: open_text_viewer(location, raw_data.decode()))
top.bind("<Control-s>", lambda e: save_directory_as())
top.bind("<Control-q>", lambda e: top.destroy())

all_buttons["Back"]["state"] = "disabled"
#all_buttons["Forward"]["state"] = "disabled"
all_buttons["Back"]["command"] = lambda: go_back()
all_buttons["Home"]["command"] = lambda: handle_command("home")

address_bar.bind("<Return>", lambda e: handle_command(address.get()))

all_buttons["Reload"]["command"] = lambda: reload_command(location)
all_buttons["Bookmark"]["state"] = "disabled"

viewport.bind("<<TreeviewSelect>>", lambda e: update_status())
viewport.bind("<Return>", lambda e: handle_entry(selection2entry()))
viewport.bind("<Double-1>", lambda e: handle_entry(selection2entry()))

def handle_entry(entry):
	if entry[0] == "i":
		pass
	elif entry[0] == "0":
		def load_fn():
			load_with_status(entry, open_text_viewer)
		load_op = Thread(None, load_fn)
		load_op.start()
	elif entry[0] == "1":
		load_as_directory(entry)
	elif entry[0] == "7":
		if entry[1] != "":
			msg = entry[1] + ":"
		else:
			msg = "Search " + entry2url(entry) + " for:"
		query = askstring("Gophersnake asks", msg, parent=top)
		load_as_directory(entry, query)
	elif entry[0] == "g":
		# TO DO: open GIF files in own window.
		def save_fn():
			load_with_status(entry, open_image_viewer)
			#save_with_status(entry[2], entry[3], int(entry[4]))
		save_op = Thread(None, save_fn)
		save_op.start()
	elif entry[0] == "h":
		if entry[2].startswith("URL:"):
			statusbar["text"] = "Opening in browser..."
			webbrowser.open_new_tab(entry[2][4:])
		else:
			save_with_status(entry[2], entry[3], int(entry[4]))
	elif entry[0] in ("5", "9", "I", "s", "d"):
		def save_fn():
			save_with_status(entry[2], entry[3], int(entry[4]))
		save_op = Thread(None, save_fn)
		save_op.start()
	else:
		error = "Can't handle " + entry_types[entry[0]] + "."
		showinfo(
			parent=top,
			title="Navigation issue",
			message=error)

def reload_command(text):
	text = text.strip()
	if text in cache:
		del cache[text]
	handle_command(text)

def handle_command(text):
	text = text.strip()
	if text == "home":
		if location != "home":
			history.append(location)
			all_buttons["Back"]["state"] = "enabled"
		go_home()
	else:
		handle_url(text)

def handle_url(url):
	parsed = urlparse(url)
	if parsed.scheme == "http" or parsed.scheme == "https":
		webbrowser.open_new_tab(url)
	elif parsed.scheme == "gopher":
		if parsed.port == None:
			port = 70
		else:
			port = str(parsed.port)

		if parsed.path == "" or parsed.path == "/":
			selector = ""
			sel_type = "1"
		elif parsed.path[0] == "/":
			selector = parsed.path[1:]
			if selector[0] in entry_types:
				sel_type = selector[0]
				selector = selector[1:]
			else:
				showerror(
					parent=top,
					title="Address bar error",
					message="Unknown selector type.")
				return
				
		entry = (sel_type, "", selector, parsed.hostname, port)
		handle_entry(entry)
	elif parsed.scheme == "file":
		if parsed.path != "":
			handle_filename(parsed.path)
		else:
			showerror(
				parent=top,
				title="Address bar error",
				message="No filename given.")
	elif parsed.scheme == "":
		showinfo(
			parent=top,
			title="Address bar issue",
			message="Unknown address type.")
	else:
		error = "Can't handle " + parsed.scheme + " addresses."
		showinfo(
			parent=top,
			title="Address bar issue",
			message=error)

def selection2entry():
	item = viewport.selection()[0]
	return dir_entries[viewport.index(item)]

def update_status():
	item = viewport.selection()[0]
	entry = dir_entries[viewport.index(item)]
	if entry[0] == "i":
		statusbar["text"] = ""
	else:
		statusbar["text"] = entry2url(entry)

def load_as_directory(entry, query=None):
	global location
	
	if query != None:
		selector = entry[2] + "\t" + query
	else:
		selector = entry[2]
	
	url = entry2url(entry)
	
	# Can't use collections.OrderedDict here because it's Python 3.x only.
	# Hopefully the RAM of a modern PC can hold the cache for one session.
	if url in cache:
		data = cache[url]
		del dir_entries[:]
		for i in data:
			dir_entries.append(i)
	elif load_raw_data(selector, entry[3], int(entry[4])):
		parse_bytes(raw_data)
		if query == None:
			cache[url] = []
			for i in dir_entries:
				cache[url].append(i)
	else:
		return

	history.append(location)
	location = url
	refresh_display()
	all_buttons["Back"]["state"] = "enabled"

def load_raw_data(selector, host, port):
	global raw_data
	data = b""
	try:
		for i in fetch_data(selector, host, port):
			data += i
		raw_data = data
		return True
	except Exception as e:
		showerror(
			parent=top,
			title="Error loading content",
			message=str(e))
		return False

def load_with_status(entry, callback):
	prog_win = Toplevel(top, padx=8, pady=8)
	prog_win.title = "Loading..."
	prog_win.transient(top)
	prog_win.resizable(FALSE, FALSE)
	
	prog_bar = ttk.Progressbar(
		prog_win, orient=HORIZONTAL, length=300, mode="indeterminate")
	prog_bar.pack()

	data = b""
	try:
		for i in fetch_data(entry[2], entry[3], int(entry[4])):
			data += i
			prog_bar.step()
		callback(entry2url(entry), data)
	except Exception as e:
		showerror(
			parent=top,
			title="Error loading content",
			message=str(e))
	finally:
		prog_win.destroy()

def save_with_status(selector, host, port):
	fn = asksaveasfilename(parent=top, title="Save file as")
	if fn == "":
		return
	
	prog_win = Toplevel(top, padx=8, pady=8)
	prog_win.title = "Downloading..."
	prog_win.transient(top)
	prog_win.resizable(FALSE, FALSE)
	
	prog_bar = ttk.Progressbar(
		prog_win, orient=HORIZONTAL, length=300, mode="indeterminate")
	prog_bar.pack()
	
	try:
		with open(fn, "wb") as f:
			for i in fetch_data(selector, host, port):
				f.write(i)
				prog_bar.step()
		return True
	except Exception as e:
		showerror(
			parent=top,
			title="Error loading content",
			message=str(e))
		return False
	finally:
		prog_win.destroy()

def show_entries(entries):
	viewport.delete(*viewport.get_children())
	for i in range(len(entries)):
		e = entries[i]
		if e == None:
			continue
		elif e[0] in entry_types:
			t = entry_types[e[0]]
		else:
			t = "[???]"
		viewport.insert(
			"", "end", values=(t, e[1]), tags=(e[0],))

def go_back():
	if len(history) > 0:
		handle_command(history.pop())
		history.pop() # 'cause the entry will promptly add itself back.
		if len(history) < 1:
			all_buttons["Back"]["state"] = "disabled"

def go_home():
	global location, raw_data
	#dir_entries.clear()
	del dir_entries[:]
	#for i in parse_file("home.txt"):
	for i in home_dir:
		dir_entries.append(i)
	location = "home"
	raw_data = b""
	refresh_display()

def refresh_display():
	show_entries(dir_entries)
	address.set(location)
	viewport.selection_set(viewport.get_children()[0])
	viewport.focus(viewport.get_children()[0])
	viewport.focus_set()

def open_text_viewer(url, data):
	text = data.decode(encoding="latin_1")
	
	window = Toplevel(top)
	window.title("Gophersnake text viewer")
	
	textview = Text(window, width=80, height=25, wrap="word")
	textview.insert("1.0", text.replace("\r\n", "\n"))
	window.bind("<Control-a>", lambda e: select_all())
	textview.bind("<Control-c>", lambda e: copy_to_clipboard())
	#textview["state"] = "disabled"
	
	def select_all():
		textview.tag_remove("sel", "1.0", "end")
		textview.tag_add("sel", "1.0", "end")
	
	def copy_to_clipboard():
		window.clipboard_clear()
		window.clipboard_append(textview.get("sel.first", "sel.last"))
	
	textview.grid(row=0, column=0, sticky=(N, S, E, W))
	textview.focus_set()
	
	textscroll = ttk.Scrollbar(
		window, orient=VERTICAL, command=textview.yview)
	textview["yscrollcommand"] = textscroll.set
	textscroll.grid(row=0, column=1, sticky=(N, S))
	
	textstatus = ttk.Label(window, text=url)
	textstatus.grid(row=1, column=0, sticky=(E, W))
	
	textgrip = ttk.Sizegrip(window)
	textgrip.grid(row=1, column=1, sticky=(S, E))
	
	window.rowconfigure(0, weight=1)
	window.columnconfigure(0, weight=1)

# Broken as of 2016-08-29
def open_image_viewer(url, bdata):
	global img
	stream = BytesIO(bdata)
	img = PhotoImage(data=stream.read())
	
	window = Toplevel(top)
	window.title("Gophersnake image viewer")
	
	imgview = ttk.Label(window, image=img)
	imgview.pack(side=TOP, fill="both", expand=TRUE)

	imgstatus = ttk.Label(window, text=url)
	imgstatus.pack(side=BOTTOM, fill="x", expand=TRUE)

def show_about():
	showinfo(
		parent=top,
		title="About Gophersnake",
		message=about)

def open_as_directory():
	fn = askopenfilename(parent=top, title="Open as directory")
	if fn != "":
		handle_filename(fn)

def handle_filename(fn):
	global location
	try:
		del dir_entries[:]
		for i in parse_file(fn):
			dir_entries.append(i)
		history.append(location)
		location = "file://" + fn.replace("\\", "/")
		refresh_display()
	except Exception as e:
		showerror(
			parent=top,
			title="Error opening directory",
			message=str(e))

def save_directory_as():
	fn = asksaveasfilename(parent=top, title="Save directory as")
	if fn == "":
		return
	try:
		write_to_file(fn, dir_entries)
	except Exception as e:
		showerror(
			parent=top,
			title="Error saving directory",
			message=str(e))
	
go_home()

top.mainloop()
