import csv
import json

class CSVtoJSON:  
	"""
	Converts a csv file to a JSON file 
	"""
	def __init__(self, csv_file):
		"""
		Stores csv file in JSON format
		"""	
		with open(csv_file, "rt") as data:
			reader = csv.reader(data)
			self.data_list = []

			# iterate through rows of csv file 
			for row in reader:
				if not row:
					continue
				elif row[0] == "-":
					self.data_list.append({"nextTrajectory":"True"})
				else:
					dictionary = ({"station1":row[0],"station2":row[1],"time":int(row[2]),"nextTrajectory":"False"})
					self.data_list.append(dictionary)

	def write_JSON(self, outfile):
		"""
		Writes out csv file as JSON to respective JSON file
		"""
		with open(outfile, 'w') as outfile:
			json.dump(self.data_list, outfile)


Convert = CSVtoJSON("connections_visualisation.csv")
Convert.write_JSON("connections_visualisation.json")


