import time

from utilities.util 				import Util
from utilities.selenide				import Selenide

from selenium                       import webdriver
from selenium.webdriver 			import ChromeOptions, FirefoxOptions, ActionChains, Keys
from selenium.webdriver.common.by   import By

class Scrape:

	def __init__( self, arguments ):

		#### 	GLOBALS 	################################

		self.arguments = arguments

		self.urls = {
			'indeed':    'https://www.indeed.com',
			'monster':   'https://www.monster.com',
			'linkedin':  'https://linkedin.com/jobs',
			'wellfound': 'https://wellfound.com/jobs'
		}

		#### 	INITIALIZE 	################################

		Util.view_arguments ( arguments )

		self.init ( )

	#### 	INITIATORS 	########################################

	def init ( self ):

		for site in self.arguments [ 'domains' ]:

			if self.arguments [ 'domains' ] [ site ] != None:

				selenide = Selenide ( 'chrome' )

				selenide.set_url ( self.urls [ site ] )


				job_search      = selenide.get_element_id  ( 'text-input-what' )

				location_search = selenide.get_element_id  ( 'text-input-where' )

				search_button   = selenide.get_element_css ( '.yosegi-InlineWhatWhere-primaryButton' )


				selenide.send_keys_to_element ( job_search,      self.arguments [ 'inputs' ] [ 'job'      ] )

				selenide.send_keys_to_element ( location_search, self.arguments [ 'inputs' ] [ 'location' ] )

				search_button.click ( )



				job_list        = selenide.get_elements_css ( '.job_seen_beacon' )


				for element in job_list:

					print ( ' >> element:\n', element.text, '\n' )

					element.click ( )



				time.sleep ( 1000 )

				driver.quit ( )
