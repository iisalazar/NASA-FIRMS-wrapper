from image.get_img import ImageGetter

# Python 2 and 3 compatibility
from builtins import input

class App(ImageGetter):
	def __init__(self, url=None, key=None):

		if url is None:
			self.url = "https://firms.modaps.eosdis.nasa.gov/wms/?REQUEST=GetMap&BBOX=-180,-90,180,90"
		else:
			self.url = url

		# By default, you can use my key
		if key is None:
			self.get_key()
		else:
			self.key = key

	def get_key(self):
		print("Key is required...")
		while True:
			try:
				key = str(input("Please input key: "))
			except ValueError:
				print("Error, please input a string")
			else:
				if len(key) == 32:
					self.key = key
					break
				else:
					printt("Error! Key must be 32 characters long!")
		return self.key
		

	# Ask the user for the layer to use
	def get_layer(self):
		layers = ["VIIRS", "MODIS", "MODIS-Aqua", "MODIS-Terra"]
		found = False
		while not found:
			print("Choose among the following layers to use")
			for index, layer in enumerate(layers):
				print("{index}. {layer}".format(index=index+1, layer=layer))
			try:
				choice = int(input(""))
			except ValueError:
				print("Error! Input must be an integer")
			else:
				if choice > 0 and choice <= 5:
					break
				else:
					continue
		return layers[choice-1]

	# Ask the user for the symbol to use
	def get_symbol(self):
		found = False
		print("Choose among the following symbols\n")
		while not found:
			for index, symbol in enumerate(self.symbols):
				print("[{index}] {symbol}".format(index=index+1, symbol=symbol))
			try:
				choice = int(input(""))
			except ValueError:
				print("Error! Input must be an integer")
			else:
				if choice > 0 and choice <= len(self.symbols):
					found = True
				else:
					print("Again, choose among them (fuck)\n")
					continue
		
		return self.symbols[choice-1]
	

	# Ask for the interval
	# Returns an integer
	def get_interval(self):
		print("Choose among the following intervals\nNOTE: Unit is in hours. Therefore 168 hours means 7 days")
		while True:
			for index, interval in enumerate(self.intervals):
				print("[{index}] {interval}".format(index=index+1, interval=interval))
			try:
				choice = int(input(""))
			except ValueError:
				print("Error! Input must be an integer")
			else:
				if choice > 0 and choice <= len(self.intervals):
					break
				else:
					print("Again, choose among them (fuck)\n")
					continue	
		return self.intervals[choice-1]

	# Ask the user for the dimensions
	# Returns a tuple
	def get_dimensions(self):
		print("Input the dimension (width and height)\n")
		while True:
			try:
				width = int(input("Width:"))
				height = int(input("Height:"))
			except ValueError:
				print("Error! Input must be an integer")
			else:
				if width < 0 or height < 0:
					print("Width and height must be greater than 0")
				else:
					break

		return (width, height)


	# Ask the user for the name of the output
	# returns a string
	def get_filename(self):
		print("Input the name you want for the image (NOTE: Don't include the extension)\n")
		while True:
			try:
				name = str(input(""))
			except ValueError:
				print("Error! Must be a string")
			else:
				if len(name.split('.')) > 1:
					print("Again, don't include the extesion!")
				else:
					break
		return name

if __name__ == '__main__':

	# By default, you can use my key
	# The url is already set
	app = App()
	
	layer = app.get_layer()
	
	symbol = app.get_symbol()
	
	interval = app.get_interval()

	dimensions = app.get_dimensions()
	filename = app.get_filename()
	print("Getting image...")
	response = app.get_image(layer=layer, symbol=symbol, interval=interval, dimensions=dimensions, filename=filename)
	print(response)

