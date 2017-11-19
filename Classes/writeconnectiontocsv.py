import csv


class connection_csv:
	"""
	writes a connection to a csv file 
	"""
	def __init__(self, connection, output_file):
		self.writer = csv.writer(output_file)
		writer.writerow(connection)



