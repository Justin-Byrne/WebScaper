import re

from difflib 	import SequenceMatcher


def hi_similarity ( root, compare_a, compare_b ):

	result_a = SequenceMatcher ( None, root, compare_a ).ratio ( )

	result_b = SequenceMatcher ( None, root, compare_b ).ratio ( )


	return compare_a if result_a > result_b else compare_b


def get_hi_similarity ( root, comparison ):

	delimiter = re.search ( r'([-|,|.|:])', comparison )


	if delimiter is not None:

		delimiter = delimiter.group ( 0 )

	else:

		return comparison


	split = comparison.split ( delimiter, maxsplit = 1 )

	split = [ entry.strip ( ) for entry in split ]


	return hi_similarity ( root, split [ 0 ], split [ 1 ] )
