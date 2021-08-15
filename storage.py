import csv
import os
import datetime


_DATETIME_FORMAT = "%Y-%m-%d"


class Csv:
	def __init__(self, filename):
		_f_write_header = not os.path.isfile(filename)

		self._field_names = ["date", "lang_target", "lang_origin"]
		self._file = open(filename, "a+")
		self._file_close_callback = lambda f: f.close()
		self._date = datetime.datetime.strftime(datetime.datetime.now(), _DATETIME_FORMAT)

		if _f_write_header:
			csv.DictWriter(self._file, self._field_names).writeheader()

	def __del__(self):
		self._file_close_callback

	def write(self, target: str, origin: str):
		writer = csv.DictWriter(self._file, self._field_names)
		writer.writerow({
			"date": self._date,
			"lang_origin": origin,
			"lang_target": target
		})


if __name__ == "__main__":
	s = Csv("storage.csv")
	s.write("echo", "well, very well")