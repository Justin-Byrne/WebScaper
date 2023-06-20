def view_arguments ( arguments ):

	print ( '-' * 100 );


	if arguments != -1:

		for argument in arguments:

			if isinstance ( arguments [ argument ], dict ):

				for domain in arguments [ argument ]:

					print ( f'[ {domain} ]\n >>', arguments [ argument ] [ domain ], f'\n' );

			else:

				print ( f'[ {argument} ]\n >>', arguments [ argument ], f'\n' );

	else:

		print ( ' >> [ error ]: not enough input to Scrape !' );


	print ( '-' * 100 );
