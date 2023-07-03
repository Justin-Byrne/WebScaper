import re

def is_non_word ( string, index ):

	length = len ( string )


	if re.search ( r'\((\w+)\)', string ): 						# (abc)

		return True


	if length <= 4 and index > 1: 								# abcd

		return True

	else: 														# iii

		for i in range ( 1, length ):

			if string [ 0 ] != string [ i ]:

				return False


			if i == length - 1 and string [ 0 ] == string [ i ]:

				return True


def to_titlecase ( string ):

	values = string.split ( )


	for index, value in enumerate ( values ):

		values [ index ] = value.upper ( ) if is_non_word ( value, index ) else value.title ( )


	return ' '.join ( values )
