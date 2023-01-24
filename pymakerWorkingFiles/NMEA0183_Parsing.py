import re
import binascii
# Parts Barrowed from https://github.com/nsweeting/NMEA0183
# Splitting adapted to using as a function with a sentance that needs parsing.
# Scott N. 1/15/2023
class NMEA0183():


	def __init__(self):
		'''
		Initiates variables.
		
		Keyword arguments:
		location -- the location of the serial connection
		baud_rate -- the baud rate of the connection
		timeout -- the timeout of the connection
		
		'''


		#Ready the GPS variables
		self.data_gps = {'lat': float(0.0), 'lon': float(0.0), 'speed': float(0.0), 'track': float(0.0), 'utc': '0.0', 'status': 'A'}
		#Ready the depth variables
		self.data_depth = {'feet': float(0.0), 'meters': float(0.0), 'fathoms': float(0.0), 'offset': float(0.0)}
		#Ready the weather variables
		self.data_weather = {'wind_angle': float(0.0), 'wind_ref': 'R', 'wind_speed': float(0.0), 'wind_unit': 'K', 'water_temp': float(0.0), 'water_unit': 'C', 'air_temp': float(0.0), 'air_unit': 'C'}
		#Ready the rudder variables
		self.data_rudder = {'stdb_angle': float(0.0), 'stdb_status': 'A', 'port_angle': float(0.0), 'port_status': 'A'}
		#Ready the turn variables
		self.data_turn = {'rate': float(0.0), 'status': 'A'}


	def processSentance(self, rawSentance):
		try:
			self.serial_data = bytes(rawSentance)
			#process
			# TODO ADD checksum to generator
			# if self.checksum(self.serial_data):
			self.check_type()
		except:
			self.quit()

	def make_checksum(self,data):
		'''
		Calculates a checksum from a NMEA sentence.
		
		Keyword arguments:
		data -- the NMEA sentence to create
		
		'''
		csum = 0
		i = 0
		# Remove ! or $ and *xx in the sentence
		data = data[1:data.rfind('*')]
		while (i < len(data)):
			input = binascii.b2a_hex(data[i])
			input = int(input,16)
			#xor
			csum = csum ^ input
			i += 1
		return csum

	def checksum(self,data):
		'''
		Reads the checksum of an NMEA sentence.
		
		Keyword arguments:
		data -- the NMEA sentence to check
		
		'''
		try:
			# Create an integer of the two characters after the *, to the right
			supplied_csum = int(data[data.rfind('*')+1:data.rfind('*')+3], 16)
		except:
			return ''
		# Create the checksum
		csum = self.make_checksum(data)
		# Compare and return
		if csum == supplied_csum:
			return True
		else:
			return False

	def check_type(self):
		'''
		Reads the sentence type, and directs the data to its respective function.
		'''
		# print("NMEA checkType:",self.serial_data[3:6])
		# array = self.serial_data.split(",")
		# print("array", len(array))

		# self.serial_data = bytes(self.serial_data).split('*')
		#Splits up the NMEA data by comma
		self.serial_data = str(self.serial_data).split(",")

		sentanceType = self.serial_data[0][5:9]
		# print("NMEA checkType:",sentanceType)

		#Incoming serial data is GPS related
		if sentanceType == "RMC":
			self.nmea_rmc()
		#Incoming serial data is weather related
		elif sentanceType == "MWV":
			self.nmea_mwv()
		#Incoming serial data is depth related
		elif sentanceType in ("DBS","DBT", "DBK"):
			self.nmea_dbs()
		#Incoming serial data is depth related
		elif sentanceType == "DPT":
			self.nmea_dpt()
		#Incoming serial data is weather related
		elif sentanceType == "MTW":
			self.nmea_mtw()
		#Incoming serial data is weather related
		elif sentanceType == "MTA":
			self.nmea_mta()
		#Incoming serial data is rudder related
		elif sentanceType == "RSA":
			self.nmea_rsa()
		#Incoming serial data is turn related
		elif sentanceType == "ROT":
			self.nmea_rot()
		elif sentanceType == "XDR":
			self.nmea_rot()

	def nmea_rmc(self):
		'''
		Deconstructs NMEA gps readings.
		'''
		# print("InGPS - speed", self.serial_data[7])
		self.data_gps['utc'] = self.gps_nmea2utc()
		self.data_gps['status'] = self.serial_data[2]
		self.data_gps['lat'] = self.gps_nmea2dec(0)
		self.data_gps['lon'] = self.gps_nmea2dec(1)
		self.data_gps['speed'] = float(self.serial_data[7])
		self.data_gps['track'] = float(self.serial_data[8])

	def nmea_dbs(self):
		'''
		Deconstructs NMEA depth readings.
		'''
		self.data_depth['feet'] = self.serial_data[1]
		self.data_depth['meters'] = self.serial_data[3]
		self.data_depth['fathoms'] = self.serial_data[5]
		self.data_depth['offset'] = 0

	def nmea_dpt(self):
		'''
		Deconstructs NMEA depth readings.
		'''
		self.data_depth['meters'] = self.serial_data[1]
		self.data_depth['offset'] = self.serial_data[2]

	def nmea_mwv(self):
		'''
		Deconstructs NMEA weather readings.
		'''
		# print("WindAngle:", self.serial_data[1])
		self.data_weather['wind_angle'] = float(self.serial_data[1])
		self.data_weather['wind_ref'] = self.serial_data[2]
		self.data_weather['wind_speed'] = float(self.serial_data[3])
		self.data_weather['wind_unit'] = self.serial_data[4]

	def nmea_mtw(self):
		'''
		Deconstructs NMEA water readings.
		'''
		self.data_weather['water_temp'] = self.serial_data[1]
		self.data_weather['water_unit'] = self.serial_data[2]

	def nmea_mta(self):
		'''
		Deconstructs NMEA air temp readings.
		'''
		self.data_weather['air_temp'] = self.serial_data[1]
		self.data_weather['air_unit'] = self.serial_data[2]


	def nmea_rsa(self):
		'''
		Deconstructs NMEA rudder angle readings.
		'''
		self.data_rudder['stbd_angle'] = self.serial_data[1]
		self.data_rudder['stdb_status'] = self.serial_data[2]
		self.data_rudder['port_angle'] = self.serial_data[3]
		self.data_rudder['port_status'] = self.serial_data[4]

	def nmea_rot(self):
		'''
		Deconstructs NMEA rudder angle readings.
		'''
		self.data_turn['rate'] = self.serial_data[1]
		self.data_turn['status'] = self.serial_data[2]

	def nmea_xdr(self):
		'''
		Deconstructs NMEA weather readings.
		'''
		if self.serial_data[0][0:2] == '$WI':
			self.data_weather['wind_angle'] = self.serial_data[1]
			self.data_weather['wind_ref'] = self.serial_data[2]
			self.data_weather['wind_speed'] = self.serial_data[3]
			self.data_weather['wind_unit'] = self.serial_data[4]

	def gps_nmea2dec(self,type):
		'''
		Converts NMEA lat/long format to decimal format.
		
		Keyword arguments:
		type -- tells whether it is a lat or long. 0=lat,1=long
		
		'''
		#Represents the difference in list position between lat/long
		x = type*2
		#Converts NMEA format to decimal format
		data = float(self.serial_data[3+x][0:2+type]) + float(self.serial_data[3+x][2+type:9+type])/60
		#Adds negative value based on N/S, W/E
		if self.serial_data[4+x] == 'S': data = data*(-1)
		elif self.serial_data[4+x] == 'W': data = data*(-1)
		return data

	def gps_nmea2utc(self):
		'''
		Converts NMEA utc format to more standardized format.
		'''
		time = self.serial_data[1][0:2] + ':' + self.serial_data[1][2:4] + ':' + self.serial_data[1][4:6]
		date = '20' + self.serial_data[9][4:6] + '-' + self.serial_data[9][2:4] + '-' + self.serial_data[9][0:2]
		return date + 'T' + time + 'Z'

	def quit(self):
		'''
		Enables quiting the serial connection.
		'''
		self.exit = True