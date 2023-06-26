import sys
import nltk

from utilities.util     			import Util
from core.scrape 					import Scrape


ERROR = -1

def main ( commands ):

	arguments = Util.get_commands ( commands )

	# Util.view_arguments ( arguments )


	if arguments != ERROR:

		Scrape ( arguments )

		# NLP ( )


main ( sys.argv )
