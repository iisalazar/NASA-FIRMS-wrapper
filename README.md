# NASA-FIRMS-wrapper
A python wrapper for the API of NASA'S FIRMS

### How to use
1. Request a map key from [NASA FIRMS Official Website](https://firms.modaps.eosdis.nasa.gov/web-services/)
2. Install the necessary libraries from the requirements.txt
 * ```shell
	pip install -r requirements.txt
   	```
3. Run the **app.py**
  * ```shell 
  	./app.py
  	```

### Note: 

* The script will prompt questions about the following:
   * Your map key
   * The layer to use
   * Symbol to use
   * What time interval to use
   * The dimensions of the output image
   * The filename you want for the output

* The image generated will be in .png format
* The image generated is located in the **"root"/images** directory