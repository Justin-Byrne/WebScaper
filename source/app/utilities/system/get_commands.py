from .parse_commands 		import parse_commands
from .debug.output	import output

ERROR = -1

def get_commands   ( commands ):

	arguments  = parse_commands ( commands )


	if all ( value == False for value in arguments [ 'domains' ].values ( ) ):

		output ( 'get_commands', [ 'No domain(s) available !', 'Please verify your command string or config.txt settings !' ] );

		return ERROR


	if any ( value == None for value in arguments [ 'inputs' ].values ( ) ):

		output ( 'get_commands', [ 'Both, a searchable "job" and "location" needs to be present !', 'Please verify your command string or config.txt settings !' ] );

		return ERROR


	return arguments
