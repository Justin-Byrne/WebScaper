import re

def clean_character ( string, character, multiply = 1 ):

	return re.sub ( rf'\s*?{character}\s+', character * multiply, string ).strip ( character )
