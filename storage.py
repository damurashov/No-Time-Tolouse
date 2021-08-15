import csv
import os
import datetime


_DATETIME_FORMAT = "%Y-%m-%d"


class Csv:
	def __init__(self, filename):
		_f_write_header = not os.path.isfile(filename)

		self.filename = filename
		self._field_names = ["date", "lang1", "lang2"]
		self._date = datetime.datetime.strftime(datetime.datetime.now(), _DATETIME_FORMAT)

		if not os.path.isfile(self.filename):
			with open(self.filename, "a+") as file_instance:
				csv.DictWriter(file_instance, self._field_names).writeheader()

	def write(self, lang1: str, lang2: str):
		with open(self.filename, "a+") as file_instance:
			writer = csv.DictWriter(file_instance, fieldnames=self._field_names)
			writer.writerow({
				"date": self._date,
				"lang1": lang1,
				"lang2": lang2
			})

	def find(self, query):
		"""
		Search for a substring ignoring case
		:param query: substring
		:return: list of tuples: [(lang1, lang2)]
		"""
		results = []

		with open(self.filename, "r") as file_instance:
			reader = csv.reader(file_instance)
			for _, lang1, lang2 in reader:
				if lang1.lower().find(query.lower()) != -1 or lang2.lower().find(query.lower()) != -1:
					results += [(lang1, lang2)]

		return results


if __name__ == "__main__":
	s = Csv("storage.csv")
	s.write("echo", "well, very well")
	print(s.find("very"))