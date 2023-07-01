def output ( source, message, type = 'error' ):

	result = ''

	start  = '\t~ '

	cursor = '>> '


	source = f'{source}.py\n'

	ahead  = f'{cursor}[ {type.lower ( )} ] - '


	match message:

		case str ( ):

			result = f'{start}{message}'

		case list ( ):

			if len ( message ) > 1:

				for note in message:

					result += f'{start}{note}\n'


				result = result.rstrip ( '\n' )

			else:

				result = f'{start}{message [ 0 ]}'


	print ( f'{ahead}{source}{result}')
