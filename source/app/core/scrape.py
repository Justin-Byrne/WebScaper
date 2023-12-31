import os
import re
import json
import time

from utilities.util 		import Util
from utilities.selenide 	import Selenide

class Scrape:

	def __init__ ( self, arguments ):

		#### 	GLOBALS 	################################

		self.arguments = arguments

		self.urls = {
			'indeed':    'https://www.indeed.com',
			'monster':   'https://www.monster.com',
			'linkedin':  'https://linkedin.com/jobs',
			'wellfound': 'https://wellfound.com/jobs'
		}

		self.regexes = {
			'indeed':
			{
				'role': 	r'jobsearch-JobInfoHeader-title\s[^<]+<span>([^<]+)<',
				'firm': 	r'<div data-company-name=\"true\"[^<]+<span[^<]+<a[^>]+>([^<]+)<',
				'locale': 	r'<\/div><\/div><div\sclass=\"css[^>]+><div>([^<]+)<',
				'pay': 		r'salaryInfoAndJobType[^<]+<[^>]+>([^<]+)<',
				'type':		r'Job\sType<[^<]+<[^<]+<[^<]+<[^<]+<[^<]+<[^>]+>([^<]+)<',
				'setting':  r'<div\sclass=\"css[^>]+><div>[^>]+>•<[^>]+>([^<]+)<',
				'details':  r'id=\"jobDescriptionText\"[^<]+([^¡]+)¡'
			},
			'monster':
			{
				'role': 	r'',
				'firm': 	r'',
				'locale': 	r'',
				'pay': 		r'',
				'type':		r'',
				'setting':  r'',
				'details':  r''
			},
			'linkedin':
			{
				'role': 	r'',
				'firm': 	r'',
				'locale': 	r'',
				'pay': 		r'',
				'type':		r'',
				'setting':  r'',
				'details':  r''
			},
			'wellfound':
			{
				'role': 	r'',
				'firm': 	r'',
				'locale': 	r'',
				'pay': 		r'',
				'type':		r'',
				'setting':  r'',
				'details':  r''
			}
		}

		self.job_offers = {
			'indeed':    [ ],
			'monster':   [ ],
			'linkedin':  [ ],
			'wellfound': [ ]
		}

		#### 	INITIALIZE 	################################

		Util.view_arguments ( arguments )

		self.init ( )

		# self.driver.quit ( )

	#### 	INITIATORS 	########################################

	def init ( self ):

		for site in self.arguments [ 'domains' ]:

			if self.arguments [ 'domains' ] [ site ]:

				selenide = Selenide (
							   self.arguments [ 'browser' ] [ 'type'     ],
							   self.arguments [ 'browser' ] [ 'switches' ],
							   self.urls      [ site      ]
						   )


				match site:

					case 'indeed':

						####################################
						#### 	INPUT 	####################

						selenide.send_keys_to_element_id ( 'text-input-what',  self.arguments [ 'inputs' ] [ 'role'     ] )

						selenide.send_keys_to_element_id ( 'text-input-where', self.arguments [ 'inputs' ] [ 'location' ] )

						selenide.get_element_css ( '.yosegi-InlineWhatWhere-primaryButton' ).click ( )

						####################################
						#### 	GET JOBS    ################

						job_list = selenide.get_elements_css ( '.job_seen_beacon' )

						####################################
						#### 	SET JOBS    ################

						job_pane_id = 'jobsearch-ViewjobPaneWrapper'


						for job in job_list:

							job.click ( )


							selenide.scroll_to (
									     job_pane_id,  												# Identifier
									     selenide.get_element_id_explicit_wait ( job_pane_id, 3 ) 	# Conditional
									 )


							job_details = selenide.get_element_id ( job_pane_id ).get_attribute ( 'innerHTML' )


							self.job_offers [ site ].append ( f'<-- START --!\n{job_details}\n¡-- END -->' )

						####################################
						#### 	PROCESS JOBS    ############

						file = f'cache/{site}/job_offers.info'

						##################
						##  CHECK PATH  ##

						path = os.path.dirname ( file )


						if Util.is_directory ( path ) is False:

							os.makedirs ( path )

						#######################
						##  ITEMIZE CONTENT  ##

						for index, job in enumerate ( self.job_offers [ site ] ):

							offer = { }


							for regex in self.regexes [ site ]:

								value = None


								if re.search ( self.regexes [ site ] [ regex ], job ):


									match regex:

										case 'role':

											value = Util.get_hi_similarity ( self.arguments [ 'inputs' ] [ 'role' ], re.search ( self.regexes [ site ] [ regex ], job ).group ( 1 ) )

											value = Util.to_titlecase      ( value )

										case 'details':

											value = Util.clean_html      ( re.search ( self.regexes [ site ] [ regex ], job ).group ( 1 ) )

											value = Util.clean_character ( value, '\n', 2 )

											# value = Util.clean_structure ( value )

										case _:

											value = re.search ( self.regexes [ site ] [ regex ], job ).group ( 1 )


								offer.update ( { regex: value } )


							self.job_offers [ site ] [ index ] = json.dumps ( offer, indent = 4 )

						#####################
						##  WRITE CONTENT  ##

						with open ( file, 'w+' ) as writer:

							writer.write ( ','.join ( self.job_offers [ site ] ) )


						# driver.quit ( )

					case 'monster':

						# code ...

						pass

					case 'linkedin':

						# code ...

						pass

					case 'wellfound':

						# code ...

						pass
