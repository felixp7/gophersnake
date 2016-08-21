#!/usr/bin/python3

from __future__ import print_function

import sys

if len(sys.argv) > 1:
	entries = []
	with open(sys.argv[1], "r") as f:
		for i in f:
			entries.append(
				(i[0],) + tuple(i[1:].rstrip().split("\t")))
	print(str(entries).replace("), ", "),\n\t"))
else:
	print("Usage:\n\tdir2python <filename>")
