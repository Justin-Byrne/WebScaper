import re


def strip_unique_character ( string, character ):

	return re.sub ( rf'.?{character}.', character, string )
