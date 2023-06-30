# SYSTEM
from .system.validation.is_directory 	import is_directory 	# VALIDATION
from .system.validation.is_file      	import is_file
from .system.validation.is_program 		import is_program

from .system.get_commands 			 	import get_commands 	# COMMAND

from .system.debug.output 				import output 			# DEBUG
from .system.debug.view_arguments 		import view_arguments

from .system.file.get_eof 			 	import get_eof 			# FILE
from .system.file.get_files 			import get_files

from .system.list.list_to_string 		import list_to_string 	# LIST

from .system.sanitize.clean_html 		import clean_html 		# SANITIZE

# CUSTOM
from .custom.string.get_similarity 		import get_similarity 	# STRING

class Util:

	def __init__ (  ): pass

	#### 	SYSTEM 	########################################

	# VALIDATION

	def is_directory 	 ( path ) 				  				: return is_directory     ( path )

	def is_file 	 	 ( path,   type = None )  				: return is_file          ( path, type )

	def is_flag      	 ( string, flag = '-'  )  				: return is_flag 	      ( string, flag )

	def is_program 		 ( program )							: return is_program 	  ( program )

	# COMMAND

	def get_command_type ( command  ) 		 	  				: return get_command_type ( command  )

	def get_commands     ( commands ) 		 	  				: return get_commands     ( commands )

	# DEBUG

	def output 			 ( source, message, type = 'error' ) 	: return output 		  ( source, message, type )

	def view_arguments   ( arguments ) 							: return view_arguments   ( arguments )

	# FILE

	def get_eof 		 ( file ) 				  				: return get_eof          ( file )

	def get_files 		 ( path, type, omissions = '' ) 		: return get_files        ( path, type, omissions )

	# STRING

	def repeat_character ( character, times = 0 ) 				: return repeat_character ( character, times )

	# LIST

	def create_2d_list   ( depth ) 				  				: return create_2d_list   ( depth )

	def entry_padding    ( tuple_list, padding = 3, entry = 0 ) : return entry_padding 	  ( tuple_list, padding, entry )

	def list_to_string   ( list ) 								: return list_to_string   ( list )

	# SANITIZE

	def clean_html 		 ( html )								: return clean_html 	  ( html )

	#### 	CUSTOM 	########################################

	# STRING

	def get_similarity	 ( root, comparison ) 					: return get_similarity   ( root, comparison )
