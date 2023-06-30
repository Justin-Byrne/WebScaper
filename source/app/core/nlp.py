import os
import json
import re
import spacy

from utilities.util 	import Util

class Nlp:

	def __init__ ( self ):

		#### 	GLOBALS 	################################

		self.nl_parser = spacy.load ( 'en_core_web_sm' )

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


	def fetch_cached_jobs ( self ):

		for ( root, dirs, files ) in os.walk ( 'cache/' ):

			for index, entry in enumerate ( files ):

				if 'job_offers.info' in entry:

					basename = os.path.basename ( root )


					with open ( f'{root}/{entry}', 'r' ) as reader:

						self.job_offers [ basename ] = json.loads ( f'[{reader.read ( ).strip ( )}]' )
