def is_only_character ( string ):

	length = len ( string )


	if length == 1:

		return True

	else:

		for i in range ( 1, length ):

			if string [ i ] != string [ 0 ]: 						return False

			if i == length - 1 and string [ i ] == string [ 0 ]: 	return True


def to_titlecase ( string ):

	values = string.split ( )


	for index, value in enumerate ( values ):

		if value.isalpha ( ) and value.islower ( ) or value.isupper ( ):

			values [ index ] = value.upper ( ) if is_only_character ( value ) else value.title ( )


	return ' '.join ( values )
