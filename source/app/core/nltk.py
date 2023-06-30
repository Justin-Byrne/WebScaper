import os
import json

from utilities.util 	import Util

from nltk.tokenize 		import sent_tokenize, word_tokenize

class Nlprocess:

	def __init__ ( self ):

		#### 	GLOBALS 	################################

		self.job_offers = {
			'indeed':    None,
			'monster':   None,
			'linkedin':  None,
			'wellfound': None
		}

		#### 	INITIALIZE 	################################

		self.init ( )

	#### 	INITIATORS 	########################################

	def init ( self ):

		self.fetch_cached_jobs ( )

		self.process_details   ( )


	def fetch_cached_jobs ( self ):

		for ( root, dirs, files ) in os.walk ( 'cache/' ):

			for index, entry in enumerate ( files ):

				if 'job_offers.info' in entry:

					basename = os.path.basename ( root )


					with open ( f'{root}/{entry}', 'r' ) as reader:

						self.job_offers [ basename ] = json.loads ( f'[{reader.read ( ).strip ( )}]' )

	def process_details   ( self ):


