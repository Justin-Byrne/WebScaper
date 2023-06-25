import time
import re

from utilities.util 		import Util
from utilities.selenide 	import Selenide

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

		self.job_offers = [ ]

		#### 	INITIALIZE 	################################

		Util.view_arguments ( arguments )

		self.init ( )

		self.process_job_offers ( )

		# self.driver.quit ( )

	#### 	INITIATORS 	########################################

	def init ( self ):

		####################################################
		#### 	FUNCTIONS    ###############################

		def set_job_offers ( list ):

			job_pane_id = 'jobsearch-ViewjobPaneWrapper'


			for job in list:

				job.click ( )


				selenide.scroll_to (
						     job_pane_id,  												# Identifier
						     selenide.get_element_id_explicit_wait ( job_pane_id, 3 ) 	# Conditional
						 )


				job_details = selenide.get_element_id ( job_pane_id ).get_attribute ( 'innerHTML' )


				self.job_offers.append ( f'<-- START --!\n{job_details}\n¡-- END -->' )

		####################################################
		#### 	LOGIC    ###################################

		for site in self.arguments [ 'domains' ]:

			if self.arguments [ 'domains' ] [ site ]:

				selenide = Selenide (
							   self.arguments [ 'browser' ] [ 'type'     ],
							   self.arguments [ 'browser' ] [ 'switches' ],
							   self.urls      [ site      ]
						   )


				selenide.send_keys_to_element_id ( 'text-input-what',  self.arguments [ 'inputs' ] [ 'job'      ] )

				selenide.send_keys_to_element_id ( 'text-input-where', self.arguments [ 'inputs' ] [ 'location' ] )


				selenide.get_element_css ( '.yosegi-InlineWhatWhere-primaryButton' ).click ( )


				job_list = selenide.get_elements_css ( '.job_seen_beacon' )


				set_job_offers ( job_list )

				# driver.quit ( )

	def process_job_offers ( self ):

		file    = '../../docs/dump/job_offers.txt'

		regexes = {
			'title': 	r'jobsearch-JobInfoHeader-title\s[^<]+<span>([^<]+)<',
			'party': 	r'<div data-company-name=\"true\"[^<]+<span[^<]+<a[^>]+>([^<]+)<',
			'locale': 	r'<\/div><\/div><div\sclass=\"css[^>]+><div>([^<]+)<',
			'pay': 		r'salaryInfoAndJobType[^<]+<[^>]+>([^<]+)<',
			'type':		r'Job\sType<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^>]+>([^<]+)<',
			'setting':  r'<div\sclass=\"css[^>]+><div>[^>]+>•<[^>]+>([^<]+)<',
			'details':  r'id=\"jobDescriptionText\"[^<]+([^¡]+)¡'
		}


		for index, job in enumerate ( self.job_offers ):

			offer = { }


			for regex in regexes:

				value = None


				if re.search ( regexes [ regex ], job ):

					if regex == 'details':

						value = Util.clean_html ( re.search ( regexes [ regex ], job ).group ( 1 ) )

					else:

						value = re.search ( regexes [ regex ], job ).group ( 1 )


				offer.update ( { regex: value } )


			self.job_offers [ index ] = '\n'.join ( '{}{}'.format ( f'{key}: ', val ) for key, val in offer.items ( ) )


		with open ( file, 'w+' ) as writer:

			writer.write ( '\n¡-- NEXT JOB --!\n\n'.join ( self.job_offers ) )
