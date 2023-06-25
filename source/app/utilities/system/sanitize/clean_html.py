import re

regex = re.compile ( '<.*?>' )


def clean_html ( html ):

	return re.sub ( regex, '', html )
