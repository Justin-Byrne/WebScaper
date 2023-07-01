from .parse_commands	import parse_commands
from .debug.output		import output


supported_browsers = [
	'chrome',
	'edge',
	'firefox',
	'ie',
	'safari'
]

ERROR = -1


def get_commands   ( commands ):

	arguments  = parse_commands ( commands )


	if all ( value == False for value in arguments [ 'domains' ].values ( ) ):

		output ( 'get_commands', [ 'No domain(s) available !', 'Please verify your command string or config.txt settings !' ] );

		return ERROR


	if any ( value == None for value in arguments [ 'inputs' ].values ( ) ):

		output ( 'get_commands', [ 'Both, a searchable "role" and "location" needs to be present !', 'Please verify your command string or config.txt settings !' ] );

		return ERROR


	if arguments [ 'browser' ] [ 'type' ] not in supported_browsers:

		output ( 'get_commands.py', f"Browser \"{arguments [ 'browser' ] [ 'type' ]}\" is not a supported browser type !" )

		return ERROR


	return arguments
