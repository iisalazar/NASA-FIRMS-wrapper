import requests
#from image.mixins import NoneCheckerMixin


KEY = "28d9f87b1ee160b01466110cae4bfb52"

SAMPLE_URL = url = "https://firms.modaps.eosdis.nasa.gov/wms/?REQUEST=GetMap&BBOX=-180,-90,180,90"

'''
a = "&SYMBOL=cross"
s = "&layers=fires_terra_24&WIDTH=1024&HEIGHT=512"
b = "https://firms.modaps.eosdis.nasa.gov/wms/?REQUEST=GetMap&layers=fires_aqua_7&WIDTH=1024&HEIGHT=512&BBOX=-180,-90,180,90&MAP_KEY=YOUR_MAP_KEY"
'''

class NoneCheckerMixin(object):
	def message(self, status, message):
		return {'status': status, 'message': message}

class ImageGetter(NoneCheckerMixin):
	
	'''
	Attributes that are needed for sending requests to FIRMS
	'''

	intervals = (24, 48, 72, 168) # limited choices for the query in hours

	wms = {
		"VIIRS": 'viirs',
		"MODIS": 'modis',
		"MODIS-Aqua": 'aqua',
		"MODIS-Terra": 'terra'
	}
	symbols = (
		"circle", 
		"circle-uf", 
		'cross', 
		'square', 
		'square-uf', 
		'triangle', 
		'triangle-uf', 
		'utriangle', 
		'utriangle-uf'
	)

	layer_template = "fires_"

	size = 5 # Default size
	url = "https://firms.modaps.eosdis.nasa.gov/wms/?REQUEST=GetMap&BBOX=-180,-90,180,90"
	

	def __init__(self, url, key):
		self.url = url
		self.key = key

	def set_layer(self, layer):
		for key in self.wms:
			if layer == key:
				return "&layers="+self.layer_template + self.wms[key]
		return None

	def set_interval(self, interval=24):
		for i in self.intervals:
			if i is interval:
				return i
		return None

	def set_dimensions(self, dimensions = (1024, 512)): # width=1024, height=512
		
		if type(dimensions) == 'tuple':
			return None

		if type(dimensions[0]) is int and type(dimensions[1]) is int:
			width = dimensions[0]
			height = dimensions[1]
			return "&WIDTH={width}&HEIGHT={height}".format(width=width, height=height)
			
		return None

	def set_symbol(self, symbol):
		for s in self.symbols:
			if s is symbol:
				return "&SYMBOL="+s
		return None

	def set_key(self):
		key = "&MAP_KEY=" + self.key
		return key

	def get_image(self, layer, symbol, dimensions, interval, filename):
		final_layer = self.set_layer(layer=layer)
		if not final_layer:
			return self.message(status="error", message="Layer not found!")
		final_symbol = self.set_symbol(symbol=symbol)
		if not final_symbol:
			return self.message(status="error", message="Symbol not found!")

		final_dimensions = self.set_dimensions(dimensions=dimensions)
		if not final_dimensions:
			return self.message(status="error", message="Dimensions must be an int and inside a tuple!")

		final_interval = self.set_interval(interval=interval)
		
		if not final_interval:
			return self.message(status="error", message="Cannot find interval in " + self.interval)

		if final_interval == 168:
			final_interval = 7

		key = self.set_key()
		final_url = self.url + final_layer + '_' + str(final_interval) + final_symbol + final_dimensions + key
		print("URL: {}".format(final_url))
		response = requests.get(final_url)
		if response.status_code == requests.codes.ok:
			open('./images/{filename}.png'.format(filename=filename), 'wb').write(response.content)
			return self.message(status="success", message="Image retrieved")
		return self.message(status="error", message="Image not retrieved")


if __name__ == '__main__':
	#app = App(url=SAMPLE_URL, key=KEY)
	imageGetter = ImageGetter(url=SAMPLE_URL, key=KEY)
	response = imageGetter.get_image(layer="VIIRS", symbol="circle", dimensions=(1024, 512), interval=48, filename="final")
	print(response)
