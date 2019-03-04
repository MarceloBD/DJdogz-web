import csv

class tsv:
	def __init__():
		return

	def open_tsv(file):
		with open(file) as tsvfile:
			reader = csv.DictReader(tsvfile, dialect='excel-tab')
			return reader 