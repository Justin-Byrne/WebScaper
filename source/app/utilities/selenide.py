import time

from utilities.util 					import Util

from selenium                       	import webdriver
from selenium.webdriver 				import ChromeOptions, FirefoxOptions, EdgeOptions, ActionChains, Keys
from selenium.webdriver.common.by   	import By
from selenium.webdriver.support 		import expected_conditions
from selenium.webdriver.support.wait 	import WebDriverWait

class Selenide:

	def __init__( self, browser_type, switches, url ):

		self.driver = None;

		self.set_driver ( browser_type, switches )

		self.set_url    ( url, 0.5 )


	############################################################
	#### 	SETTERS    #########################################

	def set_driver ( self, browser_type, switches ):

		browser_type = browser_type.lower ( )


		match browser_type:

			case 'chrome':

				if switches is None:

					self.driver = webdriver.Chrome ( )

				else:

					options     = self.get_driver_options ( ChromeOptions ( ), switches )

					self.driver = webdriver.Chrome ( options )

			case 'firefox':

				if switches is None:

					self.driver = webdriver.FirefoxDriver ( )

				else:

					options = self.get_driver_options ( FirefoxOptions ( ), switches )

					self.driver = webdriver.FirefoxDriver ( options )

			case 'safari':

				if switches is None:

					self.driver = webdriver.SafariDriver ( )

				else:

					options = self.get_driver_options ( SafariOptions ( ), switches )

					self.driver = webdriver.SafariDriver ( options )

			case 'edge':

				if switches is None:

					self.driver = webdriver.EdgeDriver ( )

				else:

					options = self.get_driver_options ( EdgeOptions ( ), switches )

					self.driver = webdriver.EdgeDriver ( options )

			case 'ie':

				if switches is None:

					self.driver = webdriver.InternetExplorerDriver ( )

				else:

					options = self.get_driver_options ( InternetExplorerOptions ( ), switches )

					self.driver = webdriver.InternetExplorerDriver ( options )

			case _:

				Util.output ( 'Selenide {Class}', f'Browser type "{browser_type}," is not a valid browser type !' )

	def set_url    ( self, url, wait ):

		self.driver.get ( url )


		if wait != None:

			self.implicit_wait ( wait )

	############################################################
	#### 	GETTERS    #########################################

	def get_element_id ( self, identifier ):

		return self.driver.find_element ( By.ID, identifier )


	def get_element_id_explicit_wait ( self, identifier, timeout ):

		result = None


		try:

			result = self.explicit_wait ( timeout, expected_conditions.visibility_of_element_located ( ( By.ID, identifier ) ) )

		except Exception as e:

			print ( ' >> Exception', f'[ {identifier} ]:', str ( e )  )


		return result


	def get_element_css ( self, cssSelector ):

		return self.driver.find_element ( By.CSS_SELECTOR, cssSelector )


	def get_element_css_explicit_wait ( self, cssSelector, timeout ):

		result = None


		try:

			result = self.explicit_wait ( timeout, expected_conditions.visibility_of_element_located ( ( By.CSS_SELECTOR, cssSelector ) ) )

		except Exception as e:

			print ( ' >> Exception', f'[ {cssSelector} ]:', str ( e )  )


		return result


	def get_elements_css ( self, cssSelector ):

		return self.driver.find_elements ( By.CSS_SELECTOR, cssSelector )


	def get_element_tag ( self, tag ):

		return self.driver.find_elements ( By.TAG_NAME, tag )


	def get_driver_options ( self, options, switches ):

		for switch in switches:

			options.add_argument ( switch )


		return options

	############################################################
	#### 	WAITS 	############################################

	def implicit_wait ( self, timeout ):

		self.driver.implicitly_wait ( timeout )


	def explicit_wait ( self, timeout, conditional ):

		return WebDriverWait ( self.driver, timeout ).until ( conditional )

	############################################################
	#### 	ACTIONS    #########################################

	def scroll_to ( self, identifier, conditional ):

		script = f"document.getElementById ( '{identifier}' ).scrollIntoView ( );"


		if conditional:

			self.execute_script ( script )


	############################################################
	#### 	DRIVER FUNCTIONS    ################################

	def execute_script ( self, script ):

		self.driver.execute_script ( script )


	############################################################
	#### 	INPUT ELEMENTS    ##################################

	def send_keys_to_element ( self, element, keys, clear = True ):

		if clear:

			self.clear_input ( element )


		ActionChains              ( self.driver   )\
			.send_keys_to_element ( element, keys )\
			.perform              (               )


	def send_keys_to_element_id ( self, identifier, keys, clear = True ):

		element = self.get_element_id ( identifier )


		if clear:

			self.clear_input ( element )


		ActionChains              ( self.driver   )\
			.send_keys_to_element ( element, keys )\
			.perform              (               )


	def clear_input ( self, element ):

		element.click ( )

		ActionChains       ( self.driver  )\
		        .key_down  ( Keys.COMMAND )\
		        .send_keys ( "a"          )\
		        .key_up    ( Keys.COMMAND )\
		        .key_down  ( Keys.DELETE  )\
		        .key_up    ( Keys.DELETE  )\
		        .perform   (              )


	def scroll_down ( self, element ):

		ActionChains       ( self.driver  )\
		        .key_down  ( Keys.END     )\
		        .key_up    ( Keys.END     )\
		        .perform   (              )
