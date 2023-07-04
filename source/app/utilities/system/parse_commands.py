import re

def parse_commands ( commands ):

	#### 	GLOBALS 	####################################

	arguments = {
		'domains':
		{
			'indeed':    False,
			'monster':   False,
			'linkedin':  False,
			'wellfound': False
		},
		'inputs':
		{
			'role':     None,
			'location': None
		},
		'browser':
		{
			'type': 	None,
			'switches': None
		},
		'help_menu': False
	}

	regexes = {
		'domains':  r'\s*-d\s*|\s*--domains\s*',
		'role':   	r'\s*-r\s*|\s*--r\s*',
		'location': r'\s*-l\s*|\s*--location\s*',
		'type':     r'\s*-b\s*|\s*--browser\s*',
		'switches': r'\s*-s\s*|\s*--switches\s*'
	}

	#### 	FUNCTIONS 	####################################

	def check_command_line ( ):

		for i in range ( 1, ( len ( commands ) - 1 ) ):

			command = commands [ i ]


			for regex in regexes:

				if ( re.search ( regexes [ regex ], command ) ):

					match regex:

						case 'domains':

							values = commands [ i + 1 ].split ( '|' )


							for value in values:

								value = value.lower ( )


								if value in arguments [ regex ].keys ( ):

									arguments [ regex ] [ value ] = True


						case 'role' | 'location':

							arguments [ 'inputs' ] [ regex ] = commands [ i + 1 ]

						case 'type':

							arguments [ 'browser' ] [ regex ] = commands [ i + 1 ].lower ( )

						case 'switches':

							arguments [ 'browser' ] [ regex ] = commands [ i + 1 ].split ( '|' )

	def check_config_file  ( ):

		config_regex = {
			'domains':  r'DOMAIN ADDRESSES',
			'inputs':   r'INPUT VALUES',
			'browser':  r'BROWSER TYPE',
			'switches': r'BROWSER SWITCHES'
		}

		for regex in config_regex:

			match regex:

				case 'domains':

					if all ( value == False for value in arguments [ regex ].values ( ) ):

						lines   = open ( './config/config.txt', 'r' ).readlines ( )

						capture = False


						for line in lines:

							if capture and line [ 0 ] == '\n': break


							if re.search ( config_regex [ regex ], line ):

								capture = True

								continue


							if capture:

								if line [ 0 ] == '#':

									continue

								else:

									value = line.replace ( '\n', '' )

									arguments [ regex ] [ value ] = True

				case 'inputs' | 'browser':

					regex_capture = re.compile ( r'([^=]+)\s*=\s*(\'|\"?)([^(\'|\"?)]+)(\'|\"?)' )


					if any ( value == None for value in arguments [ regex ].values ( ) ):

						lines   = open ( './config/config.txt', 'r' ).readlines ( )

						capture = False


						for line in lines:

							if capture and line [ 0 ] == '\n': break


							if re.search ( config_regex [ regex ], line ):

								capture = True

								continue


							if capture:

								if line [ 0 ] == '#':

									continue

								else:

									value = line.replace ( '\n', '' )

									match = regex_capture.findall ( value ) [ 0 ]


									key, value = match [ 0 ], match [ 2 ]


									arguments [ regex ] [ key ] = value

				case 'switches':

					if arguments [ 'browser' ] [ regex ] is None:

						lines   = open ( './config/config.txt', 'r' ).readlines ( )

						capture = False


						for line in lines:

							if capture and line [ 0 ] == '\n': break


							if re.search ( config_regex [ regex ], line ):

								capture = True

								continue


							if capture:

								if line [ 0 ] == '#':

									continue

								else:

									value = line.replace ( '\n', '' )


									if arguments [ 'browser' ] [ regex ] is None:

										arguments [ 'browser' ] [ regex ] = [ ]


									arguments [ 'browser' ] [ regex ].append ( value )

	#### 	LOGIC 		####################################

	check_command_line ( )

	check_config_file  ( )


	return arguments
