from selenium                       import webdriver
from selenium.webdriver 			import ChromeOptions, FirefoxOptions, ActionChains, Keys
from selenium.webdriver.common.by   import By

from utilities.util 				import Util

class Selenide:

	def __init__( self, browser_type, width = 1280, height = 720 ):

		self.driver = None;


		browser_type = browser_type.lower ( )


		match browser_type:

		    case 'chrome':

		    	options = ChromeOptions ( )


    			options.add_argument ( f"--window-size={width},{height}" )


    			self.driver = webdriver.Chrome ( options = options );

		    case 'firefox':

		        print ( 'Firefox driver !' )

		    case 'safari':

		        print ( 'Safari driver !' )

		    case 'edge':

		        print ( 'Edge driver !' )

		    case 'ie':

		        print ( 'IE driver !' )

		    case _:

		    	Util.output ( 'Selenide {Class}', f'Browser type "{browser_type}," is not a valid browser type !' )


	def set_url ( self, url, wait = 0.5 ):

		self.driver.get             ( url )

		self.driver.implicitly_wait ( wait )

	def get_element_id ( self, id ):

		return self.driver.find_element ( by = By.ID, value = id )

	def get_element_css ( self, cssSelector ):

		return self.driver.find_element ( by = By.CSS_SELECTOR, value = cssSelector )

	def get_elements_css ( self, cssSelector ):

		return self.driver.find_elements ( by = By.CSS_SELECTOR, value = cssSelector )


	def send_keys_to_element ( self, element, keys, clear = True ):

		if clear:

			element.click ( )

			ActionChains   ( self.driver  )\
		        .key_down  ( Keys.COMMAND )\
		        .send_keys ( "a"          )\
		        .key_up    ( Keys.COMMAND )\
		        .key_down  ( Keys.DELETE  )\
		        .key_up    ( Keys.DELETE  )\
		        .perform   (              )


		ActionChains ( self.driver )\
			.send_keys_to_element ( element, keys )\
			.perform ( )
