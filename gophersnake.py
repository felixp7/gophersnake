#!/usr/bin/python3
# coding=utf-8
#
# Gophersnake -- stand-alone Gopher client for modern desktops
# Copyright 2016 Felix Pleșoianu <http://felix.plesoianu.ro/>
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
import sys

if sys.version_info.major >= 3:
	from urllib.parse import urlparse
	
	from tkinter import *
	from tkinter import ttk
	from tkinter.messagebox import showinfo, showerror
	from tkinter.filedialog import askopenfilename, asksaveasfilename
else:
	from urlparse import urlparse
	
	from Tkinter import *
	import ttk
	from tkMessageBox import showinfo, showerror
	from tkFileDialog import askopenfilename, asksaveasfilename

about = """Gophersnake version 2016-08-24, running on Python %d.%d.%d
Created by Felix Pleşoianu and offered under the MIT License.
See the source code for full text.""" % (
	sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

entry_types = {"0": "[TXT]", "1": "[DIR]", "2": "[CSO]", "3": "[ERR]",
	"4": "[HEX]", "5": "[ARC]", "6": "[ENC]", "7": "[QRY]",
	"8": "[TLN]", "9": "[BIN]", "g": "[GIF]", "h": "[HTM]",
	"i": "", "I": "[IMG]", "s": "[SND]", "T": "[TN3]"}

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
dir_entries = []

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

def parse_file(filename):
	with open(filename, "r") as f:
		for i in f:
			yield (i[0],) + tuple(i[1:].rstrip().split("\t"))

def write_to_file(filename, entries):
	with open(filename, "w", newline="\r\n") as f:
		for i in entries:
			print("%s%s\t%s\t%s\t%s" % i, file=f)

def fetch_data(selector, host, port):
	global raw_data
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, port))
	sock.sendall((selector + "\r\n").encode())
	
	raw_data = b""
	data = sock.recv(1024)
	while data:
		raw_data += data
		yield True
		data = sock.recv(1024)
	
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()
	yield False

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
address_bar = Entry(toolbar, textvariable=address)
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
	command=lambda: open_text_viewer(location, raw_data.decode()))
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
viewport.tag_configure("5", font="TkFixedFont")
viewport.tag_configure("7", foreground="blue", font="TkFixedFont")
viewport.tag_configure("9", font="TkFixedFont")
viewport.tag_configure("g", foreground="blue", font="TkFixedFont")
viewport.tag_configure("h", foreground="blue", font="TkFixedFont")
viewport.tag_configure("i", font="TkFixedFont")

scroll = ttk.Scrollbar(
	main_pane, orient=VERTICAL, command=viewport.yview)
viewport["yscrollcommand"] = scroll.set
scroll.grid(row=0, column=1, sticky=(N, S))

statusbar = Label(main_pane)
statusbar.grid(row=1, column=0, sticky=(E, W))

grip = ttk.Sizegrip(main_pane)
grip.grid(row=1, column=1, sticky=(S, E))

main_pane.rowconfigure(0, weight=1)
main_pane.columnconfigure(0, weight=1)

top.bind("<Control-l>", lambda e: address_bar.focus())
top.bind("<Control-r>", lambda e: handle_command(location))
top.bind("<F5>", lambda e: handle_command(location))
top.bind("<Control-o>", lambda e: open_as_directory())
top.bind("<Control-u>",
	lambda e: open_text_viewer(location, raw_data.decode()))
top.bind("<Control-s>", lambda e: save_directory_as())
top.bind("<Control-q>", lambda e: top.destroy())

all_buttons["Back"]["state"] = "disabled"
#all_buttons["Forward"]["state"] = "disabled"
all_buttons["Home"]["command"] = lambda: go_home()

address_bar.bind("<Return>", lambda e: handle_command(address.get()))

all_buttons["Reload"]["command"] = lambda: handle_command(location)
all_buttons["Bookmark"]["state"] = "disabled"

viewport.bind("<<TreeviewSelect>>", lambda e: update_status())
viewport.bind("<Return>", lambda e: handle_entry(selection2entry()))
viewport.bind("<Double-1>", lambda e: handle_entry(selection2entry()))

def handle_entry(entry):
	global location
	if entry[0] == "0":
		if load_with_status(entry[2], entry[3], int(entry[4])):
			open_text_viewer(entry2url(entry), raw_data.decode())
	elif entry[0] == "1":
		if load_with_status(entry[2], entry[3], int(entry[4])):
			del dir_entries[:] #dir_entries.clear()
			for i in raw_data.decode().split("\r\n"):
				e = str2entry(i)
				if e != None:
					dir_entries.append(e)
			location = entry2url(entry)
			refresh_display()
	elif entry[0] == "7":
		showinfo(
			parent=top,
			title="Gophersnake says:",
			message="Search not yet implemented.")
	elif entry[0] == "g":
		showinfo(
			parent=top,
			title="Gophersnake says:",
			message="GIF files not yet supported.")
	elif entry[0] == "h":
		if entry[2].startswith("URL:"):
			statusbar["text"] = "Opening in browser..."
			webbrowser.open_new_tab(entry[2][4:])

def handle_command(text):
	text = text.strip()
	if text == "home":
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
		entry = ("1", "", "", parsed.hostname, port)
		handle_entry(entry)

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

def load_with_status(selector, host, port):
	try:
		for i in fetch_data(selector, host, port):
			statusbar["text"] = str(
				len(raw_data)) + " bytes loaded"
		return True
	except Exception as e:
		showerror(
			parent=top,
			title="Error loading content",
			message=str(e))
		return False

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

def open_text_viewer(url, text):
	window = Toplevel(top)
	window.title("Gophersnake text viewer")
	
	textview = Text(window, width=80, height=25, wrap="word")
	textview.insert("1.0", text.replace("\r\n", "\n"))
	textview.bind("<Control-a>", lambda e: select_all())
	textview.bind("<Control-c>", lambda e: copy_to_clipboard())
	#textview["state"] = "disabled"
	
	def select_all():
		textview.tag_remove("sel", "1.0", "end")
		textview.tag_add("sel", "1.0", "end")
	
	def copy_to_clipboard():
		window.clipboard_clear()
		window.clipboard_append(textview.get("sel.first", "sel.last"))
	
	textview.grid(row=0, column=0, sticky=(N, S, E, W))

	textscroll = ttk.Scrollbar(
		window, orient=VERTICAL, command=textview.yview)
	textview["yscrollcommand"] = textscroll.set
	textscroll.grid(row=0, column=1, sticky=(N, S))

	textstatus = Label(window, text=url)
	textstatus.grid(row=1, column=0, sticky=(E, W))

	textgrip = ttk.Sizegrip(window)
	textgrip.grid(row=1, column=1, sticky=(S, E))

	window.rowconfigure(0, weight=1)
	window.columnconfigure(0, weight=1)

def show_about():
	showinfo(
		parent=top,
		title="About Gophersnake",
		message=about)

def open_as_directory():
	global location
	fn = askopenfilename(parent=top, title="Open as directory")
	if fn == "":
		return
	try:
		del dir_entries[:]
		for i in parse_file(fn):
			dir_entries.append(i)
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
