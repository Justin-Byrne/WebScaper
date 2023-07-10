import os
import json
import re
import html
import spacy

from utilities.util 	import Util

from spacy.language 	import Language

class Nlp:

	def __init__ ( self ):

		#### 	GLOBALS 	################################

		self.nlp = spacy.load ( 'en_core_web_sm' )

		self.job_offers = {
			'indeed':    None,
			'monster':   None,
			'linkedin':  None,
			'wellfound': None
		}

		self.details = {
			'indeed':    None,
			'monster':   None,
			'linkedin':  None,
			'wellfound': None
		}

		# self.pipeline = [
		# 	'tok2vec',
		# 	'tagger',
		# 	'parser',
		# 	'ner',
		# 	'attribute_ruler',
		# 	'lemmatizer'
		# ]

		#### 	INITIALIZE 	################################

		self.init ( )

	#### 	INITIATORS 	########################################

	def init ( self ):

		# self.get_meaning ( )

		self.load_cached_jobs ( )

		# self.parse_details ( )

		self.sentence_detection ( )

		print ( ' >> self.details:', self.details )

		# self.print_tokens ( )

		# self.pipeline ( )

	def load_cached_jobs ( self ):

		for ( root, dirs, files ) in os.walk ( 'cache/' ):

			for index, entry in enumerate ( files ):

				if 'job_offers.info' in entry:

					basename = os.path.basename ( root )


					with open ( f'{root}/{entry}', 'r' ) as reader:

						self.job_offers [ basename ] = json.loads ( f'[{reader.read ( ).strip ( )}]' )

	def print_tokens ( self ):

		list = [
			'Strong communication skills',
			'Strong product sense',
			'Learning mentality',
			'Job Duties',
			'Minimum Requirements',
			'Special Skill Requirements',
			'Salary',
			'Strong communication skills',
			'Strong product sense',
			'Learning mentality',
			'Title',
			'Job Summary',
			'Description',
			'Education',
			'Job Type',
			'Pay',
			'Work Location',
			'Job Title',
			'Job Location',
			'Job Type',
			'Job Type',
			'Pay',
			'Work Location',
			'Why Join Us',
			'Team Introduction',
			'Job Information',
			'Who we are',
			'The Opportunity',
			'Job Category Software Engineering',
			'Job Duties',
			'Minimum Requirements',
			'Special Skill Requirements'
		]

		for item in list:

			text = self.nlp ( item )

			print ( f'[ {text} ]\n' )


			for token in text:

				dict = {
					'text': 	token.text,
					'lemma_': 	token.lemma_,
					'pos_': 	token.pos_,
					'tag_': 	token.tag_,
					'dep_': 	token.dep_,
					'shape_': 	token.shape_,
					'is_alpha': token.is_alpha,
					'is_sto': 	token.is_stop,
				}

				################################################
				#### 	SPACING    #############################

				spacing = [ ]

				padding = 3


				# STRING LENGTH OF KEY(S)
				for key in dict.keys ( ):

					spacing.append ( len ( key ) )


				max_length = max ( spacing ) + padding


				# SPACING FOR KEY(S)
				for index, space in enumerate ( spacing ):

					spacing [ index ] = max_length - space


				for index, entry in enumerate ( dict ):

					space = ' ' * spacing [ index ]

					print ( f'  >> {entry}:{space}{dict [ entry ]}\n' )


				#### 	SPACING    #############################
				################################################

				print ( '-' * 32, '\n' )

	@Language.component ( 'set_custom_boundaries' )
	def set_custom_boundaries ( document ):

		for token in document:

			if token.text in [ ':', '\n', '\n\n' ]:

				document [ token.i + 1 ].is_sent_start = True


		return document


	def add_pipes ( self ):

		self.nlp.add_pipe ( 'set_custom_boundaries', before = 'parser' )



	def sentence_detection ( self ):

		self.add_pipes ( )


		for site in self.job_offers:

			if self.job_offers [ site ] is not None:

				for offer in self.job_offers [ site ]:

					details   = offer [ 'details' ]


					data = {
						'raw': f"{details}\n\n{'-' * 60}\n\n",
						'new':  [ ],
					}


					document  = self.nlp ( details )

					sentences = list ( document.sents )


					preserve  = None


					for sentence in sentences:

						if str ( sentence ).isdigit ( ):

							preserve = str ( sentence )

							continue


						if str ( sentence ).isspace ( ) is False:

							result = f'{preserve} {sentence}' if preserve else f'{sentence}'

							result = html.unescape ( repr ( result ).replace ( '\\n', '' ) [ 1:-1 ] )


							data [ 'new' ].append ( result )


							preserve = None


					#####################
					##  CLEAN CONTENT  ##

					if '/' in offer [ 'role' ]:

						offer [ 'role' ] = offer [ 'role' ].replace ( '/', '\\' )


					if re.search ( r'(,?)\s*[I|i][N|n][C|c](\.?)', offer [ 'firm' ] ):

						offer [ 'firm' ] = re.sub ( r'(,?)\s*[I|i][N|n][C|c](\.?)', '', offer [ 'firm' ] )



					key   = f"{offer [ 'firm' ]}-[{offer [ 'role' ]}]"

					value = data [ 'new' ].copy ( )


					# print ( ' >> key:  ', key )

					# print ( ' >> value:', value )



					if self.details [ site ] is None:

						self.details [ site ]  = { key: value }

					else:

						# self.details [ site ] |= { key: value }

						self.details [ site ].update ( self.details [ site ], key = value )

						# print ( self.details [ site ] )



					# print ( ' >> self.details:', self.details )

					#####################
					##  WRITE CONTENT  ##

					file = f"cache/reports/{site}/{offer [ 'firm' ]}-[{offer [ 'role' ]}]-details-sentences.info"

					##################
					##  CHECK PATH  ##

					path = os.path.dirname ( file )


					if Util.is_directory ( path ) is False:

						os.makedirs ( path )

					##################
					##     WRITE    ##

					with open ( file, 'w+' ) as writer:

						writer.write ( data [ 'raw' ] + '\n'.join ( data [ 'new' ] ) )



	def parse_details ( self ):

		file     = f'cache/indeed/details.info'
		file_two = f'cache/indeed/details-sentences.info'

		details = [
			"JOB SUMMARY\n\nYou will be building scalable systems and shipping features in a complex environment, where one must contend with challenges such as modernizing legacy applications and managing technical debt.\n\nROLES AND RESPONSIBILTIES\n\nDesign, develop, and deploy applications that can handle high request volumes with high reliability and low latency\n\nCollaborate with product managers to build product requirements against business objectives and drive teams through the complete software development lifecycle\n\nEnvision system features and functionality, create detailed design documentation, and decide on tradeoffs between technical and design approaches.\n\nIdentify any technical issues that arise and follow up with root-cause analysis and resolution\n\nIdentify key application metrics, build necessary dashboards for monitoring performance, and add necessary logging for real-time debugging\n\nReview code, support continuous improvement, and investigate alternatives\n\nUtilize CI/CD tools to support system integration and deployment\n\nMentor other engineers to help build a high-performing engineering culture\n\nQUALIFICATIONS\n\n2+ of experience in the technology industry, and a B.S. in Computer Science or equivalent\n\nProficiency in one or more programming languages and common data structures / algorithms\n\nAbility to write production-ready code with moderate supervision\n\nAbility to design systems of moderate complexity\n\nAbility to conduct code reviews and give sign-off for code merges\n\nStrong communication skills. You must be able to work with cross-functional partners to gather requirements and explain outcomes\n\nStrong product sense. You must be able to align your work with business objectives and make appropriate tradeoffs\n\nLearning mentality. You must be able to pick up new skills as needed and demonstrate a curiosity about new technologies\n\nHIGHLY PREFERRED\n\nEngineering experience at high-tech firms (e.g. Amazon, Meta, DoorDash, Twilio)\n\nExperience architecting and building large-scale systems in an agile development environment\n\nExperience working alongside technical product managers to drive projects and flesh out product requirements\n\nWe expect the starting salary to be around $100,000 with annual bonus and profit sharing eligibility. The actual salary will be determined based on years of relevant work experience The Hertz Corporation operates the Hertz, Dollar Car Rental, Thrifty Car Rental brands in approximately 9,700 corporate and franchisee locations throughout North America, Europe, The Caribbean, Latin America, Africa, the Middle East, Asia, Australia and New Zealand. The Hertz Corporation is one of the largest worldwide airport general use vehicle rental companies, and the Hertz brand is one of the most recognized in the world.\n\nUS EEO STATEMENT\n\nAt Hertz, we champion and celebrate a culture of diversity and inclusion. We take affirmative steps to promote employment and advancement opportunities. The endless variety of perspectives, experiences, skills and talents that our employees invest in their work every day represent a significant part of our culture \u2013 and our success and reputation as a company.\n\nIndividuals are encouraged to apply for positions because of the characteristics that make them unique.\n\nEOE, including disability/veteran\n\nReturn to Search Result",
			"To get the best candidate experience, please consider applying for a maximum of 3 roles within 12 months to ensure you are not duplicating efforts.\n\nJob Category Software Engineering\n\nJob Details\n\nSalesforce Inc. seeks Software Engineer in Seattle, WA:\n\nJob Duties : Formulate, implement, and evaluate algorithms for platform and application. Create code for front-end development. Work closely with Quality Engineering, Product Management, and Technical Operations to develop, test, and deploy highly useful, high quality software. Analyze, design and develop test cases and implement automated test suites. Resolve complex technical issues and drive innovation that improves salesforce. Telecommuting is an option. Some travel to Salesforce\u2019s offices is required. \u02c6Above address additionally encompasses the following Salesforce locations in the Seattle area: 1621 North 34th Street, Seattle, WA 98103, 744 N. 34th St. Seattle, WA 98103, 1000 N. Northlake Way, Seattle, WA 98103, and 400 Urban Plaza, Suite 700 Kirkland, WA 98033. The permanent position may be offered at any of these locations in the Seattle area.\n\nMinimum Requirements : Master\u2019s degree (or its foreign degree equivalent) in Computer Science, Engineering (any field), or a related quantitative discipline.\n\nA related technical degree required (Computer Science, Engineering (any field).\n\nSpecial Skill Requirements : (1) Java; (2) C++; (3) C; (4) HTML; (5) JavaScript; (6) SQL; (7) R; (8) Python; (9); MongoDB (10) NoSQL; (11) Golang; (12) XML; (13) PostreSQL; (14) C#; (15) Splunk; (16) Google API. Any suitable combination of education, training and/or experience is acceptable. Education, experience and criminal background checks will be conducted. Telecommuting is an option. Some travel to Salesforce\u2019s office is required.\n\nSalary : $156,030.00 - $168,700.00 per annum\n\nCertain roles may be eligible for incentive compensation, equity, and benefits. More details about company benefits can be found at the following link: https://www.salesforcebenefits.com .\n\nSubmit a resume using the apply button on this posting or by email at: onlinejobpostings@salesforce.com at Job #21-1264. Salesforce is an Equal Opportunity &amp; Affirmative Action Employer. Education, experience and criminal background checks will be conducted.\n\n#LI-DNI\n\nAccommodations\n\nIf you require assistance due to a disability applying for open positions please submit a request via this Accommodations Request Form .\n\nPosting Statement\n\nAt Salesforce we believe that the business of business is to improve the state of our world. Each of us has a responsibility to drive Equality in our communities and workplaces. We are committed to creating a workforce that reflects society through inclusive programs and initiatives such as equal pay, employee resource groups, inclusive benefits, and more. Learn more about Equality at Salesforce and explore our benefits.\n\nSalesforce.com and Salesforce.org are Equal Employment Opportunity and Affirmative Action Employers. Qualified applicants will receive consideration for employment without regard to race, color, religion, sex, sexual orientation, gender perception or identity, national origin, age, marital status, protected veteran status, or disability status. Salesforce.com and Salesforce.org do not accept unsolicited headhunter and agency resumes. Salesforce.com and Salesforce.org will not pay any third-party agency or company that does not have a signed agreement with Salesforce.com or Salesforce.org .\n\nSalesforce welcomes all.\n\nMore details about our company benefits can be found at the following link: https://www.getsalesforcebenefits.com/\n\nFor Washington-based roles, the base salary hiring range for this position is $156,030 to $168,700.\n\nCompensation offered will be determined by factors such as location, level, job-related knowledge, skills, and experience. Certain roles may be eligible for incentive compensation, equity, benefits. More details about our company benefits can be found at the following link: https://www.salesforcebenefits.com.\nReturn to Search Result",
			"About Sound Physicians:\n\nHeadquartered in Tacoma, WA, Sound Physicians is a physician-founded and led, national, multi-specialty medical group made up of more than 1,000 business colleagues and 4,000 physicians, APPs, CRNAs, and nurses practicing in 400-plus hospitals across 45 states. Founded in 2001, and with specialties in emergency and hospital medicine, critical care, anesthesia, and telemedicine, Sound has a reputation for innovating and leading through an ever-changing healthcare landscape \u2014 with patients at the center of the universe.\n\nAbout the Role:\n\nSound Physicians\u2019 Information Systems group is currently seeking an experienced healthcare HL7 Interface Analyst to help implement data integration interfaces with our partner hospitals, billing partners and other affiliates. This position requires excellent communication, technical and project management skills.\n\nEssential Duties and Responsibilities:\n\nIn this position you will be engaged in analyzing and evaluating hospital data systems to create detailed integration specifications and solutions. This will include identifying communications protocols, data mapping, cleaning, validation rules, etc. It will also require coordinating and conducting specification reviews, interface testing, and interface implementation project management.\n\nThe ideal candidate will have significant experience in HL7 interfaces and interface engines such as Mirth. Expertise with NextGen Health Data Hub, is highly desirable.\n\nSpecial Knowledge, Skills, Abilities, Training, or Special Licenses/Certifications Needed to perform this job:\n\nMS SQL Server Database, SSIS, and TSQL\n\nExperience with communication protocols (HTTP, TCP/IP, MLLP, Web Services, FTP)\n\nExperience with Javascript or other scripting/programming languages is a plus\n\nSolid understanding and knowledge of data processing/ETL, data modeling, systems analysis, software systems implementation, and project management\n\nExperience with HL7 and other healthcare data exchange formats\n\nExperience with CCLF data structures is a plus\n\nExperience with NextGen Mirth Connect and HDH is a plus\n\nEducation and Experience:\n\nEducation\n\nFour year college degree in health care management information systems or related field, or equivalent experience\n\nExperience\n\n3+ years experience with data integration and ETL solutions with significant involvement in healthcare\n\nOther details:\n\nSitting at desk for up to eight hours (w/breaks)\n\nWorking on computer for up to eight hours (w/breaks)\n\nThis job description reflects the present requirements of the position. As duties and responsibilities change and develop, the job description will be reviewed and subject to amendment. #SoundBC #ZR\n\nIf you require alternative methods of application or screening, you must approach the employer directly to request this as Indeed is not responsible for the employer's application process.Return to Search Result",
			"Have you ever wondered what it would be like to help protect over a billion users across the planet? Are you excited about cybersecurity? Do you want to join a team that will move the needle on security problems? If so, read on! The\n\nMicrosoft Security Response Center (MSRC) team's mission is to protect our customers from the perils and attacks they face as they engage in the online world. The team\u2019s charter is to protect Microsoft 365, the world\u2019s largest productivity service and its principal data store. We continually take inputs from bug bounty, internal penetration test and external customer feedback to keep our customer's data secure. We are tasked with keeping up and exceeding the pace of innovation that is happening around the world.\n\nThe Substrate Green Team is responsible for building security strategy, writing prototype and proof-of-concept code, working with teams to evangelize secure patterns, and driving architectural changes into the product to improve security outcomes at the scale of M365.\n\nWe are looking for committed Software Engineers to join us. Interested? Come talk to us!\n\nResponsibilities\n\nThis is a great opportunity for you to help us build security features. Below are some of the responsibilities on this role, come join us on this exciting journey to build an innovative product.\n\nImprove application security maturity at scale by designing, implementing, and building security solutions.\n\nPartner with product managers and senior security leaders to ensure security maturity work is being prioritized and addressed across Microsoft 365 services.\n\nBuilding prototypes and proof-of-concept code, working alongside the engineering teams to provide advice on secure design and implementation.\n\nProviding design guidance and security reviews to engineering teams and improve security maturity\n\nQualifications\n\nRequired Qualifications\n\nBachelor's Degree in Computer Science, or related technical discipline with proven experience coding in languages including, but not limited to, C, C++, C#, Java, JavaScript, or Python\n\nOR equivalent experience.\n\nExperience with Distributed Services.\n\nOther Requirements\n\nAbility to meet Microsoft, customer and/or government security screening requirements are required for this role. These requirements include, but are not limited to, the following specialized security screenings:\n\nMicrosoft Cloud Background Check: This position will be required to pass the Microsoft Cloud background check upon hire/transfer and every two years thereafter.\n\nPreferred Qualifications\n\nExperience building and shipping production grade software or services.\n\nExperience in conducting threat model assessment of infrastructure and services.\n\nHave Integrity, ingenuity, results-orientation, self-motivation, and resourcefulness in a fast-paced competitive environment.\n\nHave a deep desire to work collaboratively, solve problems with groups, find win/win solutions and celebrate successes.\n\nUnderstanding of data structures, algorithms, and distributed systems\n\nSoftware Engineering IC2 - The typical base pay range for this role across the U.S. is USD $76,400 - $151,800 per year. There is a different range applicable to specific work locations, within the San Francisco Bay area and New York City metropolitan area, and the base pay range for this role in those locations is USD $100,300 - $165,400 per year.\n\nCertain roles may be eligible for benefits and other compensation. Find additional benefits and pay information here: https://careers.microsoft.com/us/en/us-corporate-pay\n\n#MSRC\n\n#MSFTSecurity\n\nMicrosoft is an equal opportunity employer. Consistent with applicable law, all qualified applicants will receive consideration for employment without regard to age, ancestry, citizenship, color, family or medical care leave, gender identity or expression, genetic information, immigration status, marital status, medical condition, national origin, physical or mental disability, political affiliation, protected veteran or military status, race, ethnicity, religion, sex (including pregnancy), sexual orientation, or any other characteristic protected by applicable local laws, regulations and ordinances. If you need assistance and/or a reasonable accommodation due to a disability during the application process, read more about requesting accommodations.\nReturn to Search Result",
			"JOB SUMMARY\n\nYou will be building scalable systems and shipping features in a complex environment, where one must contend with challenges such as modernizing legacy applications and managing technical debt.\n\nROLES AND RESPONSIBILTIES\n\nDesign, develop, and deploy applications that can handle high request volumes with high reliability and low latency\n\nCollaborate with product managers to build product requirements against business objectives and drive teams through the complete software development lifecycle\n\nEnvision system features and functionality, create detailed design documentation, and decide on tradeoffs between technical and design approaches.\n\nIdentify any technical issues that arise and follow up with root-cause analysis and resolution\n\nIdentify key application metrics, build necessary dashboards for monitoring performance, and add necessary logging for real-time debugging\n\nReview code, support continuous improvement, and investigate alternatives\n\nUtilize CI/CD tools to support system integration and deployment\n\nMentor other engineers to help build a high-performing engineering culture\n\nQUALIFICATIONS\n\n9+ years of experience in the technology industry, and a B.S. in Computer Science or equivalent\n\nProficiency in one or more modern programming languages (e.g. Java, Ruby, Python, Golang) and common data structures / algorithms\n\nAbility to design systems of large complexity\n\nAbility to act at tech lead for projects end-to-end\n\nStrong communication skills. You must be able to work with cross-functional partners to gather requirements and explain outcomes\n\nStrong product sense. You must be able to align your work with business objectives and make appropriate tradeoffs\n\nLearning mentality. You must be able to pick up new skills as needed and demonstrate a curiosity about new technologies\n\nHIGHLY PREFERRED\n\nEngineering experience at high-tech firms (e.g. Amazon, Meta, DoorDash, Twilio)\n\nExperience architecting and building large-scale systems in an agile development environment\n\nExperience working alongside technical product managers to drive projects and flesh out product requirements\n\nWe expect the starting salary to be around $205,000 with annual bonus. The actual salary will be determined based on years of relevant work experience The Hertz Corporation operates the Hertz, Dollar Car Rental, Thrifty Car Rental brands in approximately 9,700 corporate and franchisee locations throughout North America, Europe, The Caribbean, Latin America, Africa, the Middle East, Asia, Australia and New Zealand. The Hertz Corporation is one of the largest worldwide airport general use vehicle rental companies, and the Hertz brand is one of the most recognized in the world.\n\nUS EEO STATEMENT\n\nAt Hertz, we champion and celebrate a culture of diversity and inclusion. We take affirmative steps to promote employment and advancement opportunities. The endless variety of perspectives, experiences, skills and talents that our employees invest in their work every day represent a significant part of our culture \u2013 and our success and reputation as a company.\n\nIndividuals are encouraged to apply for positions because of the characteristics that make them unique.\n\nEOE, including disability/veteran\n\nReturn to Search Result",
			"About Traverse\n\nTraverse is an identity resolution company helping marketers go beyond their active list, and engage in-market consumers within the email channel. It\u2019s no secret that email is a highly effective communication tool for marketers to reach their active subscribers. Our aspirations for email are much bigger.\n\nWe enable marketers to reach people via email whom they currently have no means to do so, including:\n\nReal-time identity resolution for anonymous website visitors\n\nFormer customers who are in-market again for their products\n\nIdentifying new customers who are in-market for products across the web\n\nFounded by the same team that started and sold LeadSpend to Experian.\n\nAbout the Position\n\nThe Traverse team is looking for a software engineer to help grow and maintain our existing products, and innovate into new areas. At its core, this position will revolve around working as part of our core development team to build out our evolving product offerings. We are a small and agile company, and put a high premium on the ability to work independently to achieve a goal.\n\nWe each wear many hats, and this role is no exception. Depending on the experience of the candidate, this role may expand to include additional responsibilities such as managing a development team, administering our stack in production, and maintaining our product roadmap and associated backlog.\n\nThe position will be located in Seattle, but full-time remote will be considered for the right candidate. Salary will range from $65,000 to $100,000 depending on experience.\n\nAs a future Software Engineer at Traverse, you are:\n\nWell organized and self-motivated\n\nAn excellent developer, able to write efficient and clean code and maintain tests\n\nAble to work both independently and as part of a team\n\nA critical thinker, able to understand how technologies fit together and identify issues\n\nResponsibilities may include:\n\nDeveloping code for Traverse\u2019s core products and ensuring all code is well tested\n\nInterpreting user stories into technical needs and acceptance criteria\n\nReviewing pull requests and merging to our main code branch\n\nMonitoring the platform production deploys\n\nContributing to deployment infrastructure (Jenkins and various automation)\n\nQualifications:\n\nBachelor\u2019s degree in Computer Science or a related field\n\nExcellent technical written and verbal communication skills\n\nExcellent understanding of JavaScript, NodeJS, and Git\n\nExperience building RESTful APIs, especially in Express and related frameworks\n\nExperience in software architecture and design, especially with web applications and distributed systems\n\nExperience working with data on a large scale, and an understanding the challenges it presents\n\nExperience with network infrastructure, especially in AWS\n\nConcrete Skills:\n\nNode.js. Experience with Node Streams, Express.js, and Promises required.\n\nAWS. Experience with Cloudformation, DynamoDb, Cloudwatch, SQS, and SWF desired.\n\nSQL. Experience with AWS RDS, MySql, and/or PrestoDb desired.\n\nBash. Familiar with manipulating files using pipes and unix tools such as grep, awk, and compression utilities.\n\nJenkins. Experience managing a continuous delivery pipeline with automated tests and deployments. Experience with other CI platforms may be considered.\n\nGit. Experience working within a Github organization, multiple repositories and pull requests. Other version control software experience may be considered.\n\nThis position is open to all candidates that meet the minimum qualifications. Traverse values diverse perspectives and life experiences. Applicants will be considered regardless of race, color, creed, national origin, ancestry, sex, marital status, disability, religious or political affiliation, age, sexual orientation, medical condition, or pregnancy. Traverse encourages people of all backgrounds to apply, including people of color, immigrants, refugees, women, LGBTQ, people with disabilities, veterans, and those with diverse life experiences. If you have questions, please contact sam@traversedata.com.\nReturn to Search Result",
			"Requirements:\n\nComing soon with more details on this job posting.\n\nThank you for being patient.\n\nNice to have but not necessary:\n\nComing soon\n\nPERKS &amp; BENEFITS\n\nHealth Insurance\n\nDental Insurance\n\nVision Insurance\n\nFlexible Spending Account\n\n401(K) Retirement Plan\n\nBasic Term Life Insurance\n\nOn top of everything, Enjoy bottomless snacks and refreshments as well as a great team-working environment.Return to Search Result",
			"Title::Software Engineer\nJob Summary\nPlay a part in the next revolution in human-computer interaction. Build groundbreaking technology for large scale systems, spoken language, big data, and artificial intelligence. The AI/ML - Machine Translation team is looking for exceptional Software Engineers passionate about delighting customer\u2019s experience, building and improving the Machine Learning Automation and Infrastructure.\nDescription\nYou will be a part of a team that's responsible for a wide variety of language technologies related development activities. Your focus will be on developing the model automation pipeline which is highly scalable, robust and efficient. The role will be part of the model automation team to deal with large quantities of data, apply the state-of-the-art methods in deep learning to tackle real world problems, create the production quality models at scale and set up ML CI/CD pipelines. You should therefore be passionate about creating phenomenal products that are used by millions of people. You\u2019re expected to be a team player who thrives in a fast paced environment with rapidly changing priorities.\nQualifications:\n\nExcellent coding skills in the one of the following languages , e.g. Python, bash scripting, java, C/C++ etc.\n\n3+ years working experience in big data/Spark/MapReduce, large distributed system, cloud computing etc\n\nKnowledge in ML technologies or toolkits such as NLP, MT, ASR, pyTorch, TensorFlow is a big plus\n\nExcellent communication and problem-solving skill\n\nFast learner and strong motivation on growing and learning new technologies\n\nEducation\nB.S. or M.S. in Computer Science or related field\nJob Type: Contract\nPay: $70.00 - $78.00 per hour\nSchedule:\n\n8 hour shift\n\nMonday to Friday\n\nWork Location: In personIf you require alternative methods of application or screening, you must approach the employer directly to request this as Indeed is not responsible for the employer's application process.Return to Search Result",
			"Job Title: Embedded Software Engineer\nJob Location: Redmond, WA\nJob Type: 12 Months Contract\nSummary:\n\nThe research team is looking for an experienced Embedded Software Engineer to develop firmware for a custom SoC.\n\nJob Responsibilities:\n\nDevelop firmware to interface to an NVMe device over PCIe\n\nOptimize data paths to maximize throughput to memory\n\nDevelop firmware to integrate custom image sensors with an MCU\n\nTest the developed firmware with the hardware\n\nDocument designs and performance analysis\n\nMinimum Qualifications:\n\n10+ years experience in Firmware or Embedded Software Development in C/C++\n\n2+ years experience developing drivers for NVMe\n\n2+ years experience developing drivers and bringing up PCIe on new ICs\n\nExperience with low power substates on PCIe 3.0 or greater\n\nExperience with Zephyr OS, Embedded Linux or other RTOS\n\nAbility to work autonomously with little or no supervision\n\nAbility to work in a dynamic, high-paced environment where job duties may change frequently\n\nPreferred Qualifications:\n\nLow power optimization of embedded systems\n\nFamiliarity with MIPI C-PHY and image sensors\n\nFamiliarity with I3C, TDM, I2S\n\nFamiliarity with DSPs\n\nFamiliarity with file systems\n\nStrong technical writing skills\n\nEducation/Experience:\n\nBachelor's degree in computer science, software engineering or relevant field required.\n\n#ENG1\nJob Type: Contract\nPay: $108.00 - $113.00 per hour\nBenefits:\n\nDental insurance\n\nHealth insurance\n\nReferral program\n\nVision insurance\n\nSchedule:\n\n8 hour shift\n\nDay shift\n\nMonday to Friday\n\nAbility to commute/relocate:\n\nRedmond, WA 98052: Reliably commute or planning to relocate before starting work (Required)\n\nExperience:\n\nFirmware or Embedded Software Development in C/C++: 10 years (Required)\n\nNVMe drivers development: 2 years (Required)\n\ndeveloping drivers and bringing up PCIe on new ICs: 2 years (Required)\n\nWork Location: In personIf you require alternative methods of application or screening, you must approach the employer directly to request this as Indeed is not responsible for the employer's application process.Return to Search Result",
			"Are you interested in building products used by more than 3 billion people? Do you like shipping code at a rapid pace? Facebook is seeking an experienced Front End Engineer that is passionate about building mobile and desktop web applications. This position is full-time.\n\nSoftware Engineer, Front End Responsibilities:\n\nImplement the features and user interfaces of Facebook products like News Feed\n\nArchitect efficient and reusable front-end systems that drive complex web applications\n\nCollaborate with Product Designers, Product Managers, and Software Engineers to deliver compelling user-facing products\n\nIdentify and resolve performance and scalability issues\n\nMinimum Qualifications:\n\n6+ years of JavaScript experience, including concepts like asynchronous programming, closures, types, and ES6\n\nBachelor's degree in Computer Science, Computer Engineering, relevant technical field, or equivalent practical experience.\n\n6+ years of HTML/CSS experience, including concepts like layout, specificity, cross browser compatibility, and accessibility\n\n6+ years experience with browser APIs and optimizing front end performance\n\nPreferred Qualifications:\n\nExperience with React\n\nBS/MS in Computer Science or a related technical field\n\nMeta is proud to be an Equal Employment Opportunity and Affirmative Action employer. We do not discriminate based upon race, religion, color, national origin, sex (including pregnancy, childbirth, reproductive health decisions, or related medical conditions), sexual orientation, gender identity, gender expression, age, status as a protected veteran, status as an individual with a disability, genetic information, political views or activity, or other applicable legally protected characteristics. You may view our Equal Employment Opportunity notice here. We also consider qualified applicants with criminal histories, consistent with applicable federal, state and local law. We may use your information to maintain the safety and security of Meta, its employees, and others as required or permitted by law. You may view Meta's Pay Transparency Policy, Equal Employment Opportunity is the Law notice, and Notice to Applicants for Employment and Employees by clicking on their corresponding links. Additionally, Meta participates in the E-Verify program in certain locations, as required by law\n\nReturn to Search Result",
			"TikTok is the leading destination for short-form mobile video. Our mission is to inspire creativity and bring joy. TikTok has global offices including Los Angeles, New York, London, Paris, Berlin, Dubai, Singapore, Jakarta, Seoul and Tokyo.\n\nWhy Join Us \nAt TikTok, our people are humble, intelligent, compassionate and creative. We create to inspire - for you, for us, and for more than 1 billion users on our platform. We lead with curiosity and aim for the highest, never shying away from taking calculated risks and embracing ambiguity as it comes. Here, the opportunities are limitless for those who dare to pursue bold ideas that exist just beyond the boundary of possibility. Join us and make impact happen with a career at TikTok.\n\nTeam Introduction \nEnterprise Solution RD is in charge of developing industrial, commercialized, enterprise-level solutions and products, to meet business requirements in various scenarios, such as Network Infrastructure Construction, System and Application Management, Large-scale Asset Management, Front-desk Service, Audio/Video Broadcasting Service, Server/Conference Room Intelligent Operation, Enterprise Administration, etc. Taking advantage of cutting-edge big data and AI technologies, we are aiming at building a more automated and intelligent enterprise solution infrastructure.\n\nResponsibilities:\n\nDevelop, improve, and maintain web solutions.\n\nImplement new UI components with a focus on performance and scalability.\n\nDesign and drive front-end infrastructure.\n\nQualifications\n\nBachelor or higher degree in Computer Science, Computer Engineering, Information Systems, Math etc.\n\nFamiliar with HTML/CSS, JavaScript(ES6).\n\nProven capabilities with web framework like ReactJS/NodeJS.\n\nExperience with UI/UX design and strong abilities to work with others to improve products.\n\nExperience with SQL/NoSQL Database.\n\nSelf-motivated, intense eagerness to learn, ready to dive deep into complex problems, good at communication, and great team work spirit.\n\nTikTok is committed to creating an inclusive space where employees are valued for their skills, experiences, and unique perspectives. Our platform connects people from across the globe and so does our workplace. At TikTok, our mission is to inspire creativity and bring joy. To achieve that goal, we are committed to celebrating our diverse voices and to creating an environment that reflects the many communities we reach. We are passionate about this and hope you are too.\n\nTikTok is committed to providing reasonable accommodations in our recruitment processes for candidates with disabilities, pregnancy, sincerely held religious beliefs or other reasons protected by applicable laws. If you need assistance or a reasonable accommodation, please reach out to us at usrc@tiktok.com. \nJob Information \nThe base salary range for this position in the selected city is $129200 - $194750 annually.\n\n\u200b\n\nCompensation may vary outside of this range depending on a number of factors, including a candidate\u2019s qualifications, skills, competencies and experience, and location. Base pay is one part of the Total Package that is provided to compensate and recognize employees for their work, and this role may be eligible for additional discretionary bonuses/incentives, and restricted stock units.\n\n\u200b\n\nAt ByteDance/TikTok our benefits are designed to convey company culture and values, to create an efficient and inspiring work environment, and to support ByteDancers to give their best in both work and life. We offer the following benefits to eligible employees:\n\n\u200b\n\nWe cover 100% premium coverage for employee medical insurance, approximately 75% premium coverage for dependents and offer a Health Savings Account(HSA) with a company match. As well as Dental, Vision, Short/Long term Disability, Basic Life, Voluntary Life and AD&amp;D insurance plans. In addition to Flexible Spending Account(FSA) Options like Health Care, Limited Purpose and Dependent Care.\n\n\u200b\n\nOur time off and leave plans are: 10 paid holidays per year plus 17 days of Paid Personal Time Off(PPTO) (prorated upon hire and increased by tenure) and 10 paid sick days per year as well as 12 weeks of paid Parental leave and 8 weeks of paid Supplemental Disability.\n\n\u200b\n\nWe also provide generous benefits like mental and emotional health benefits through our EAP and Lyra. A 401K company match, gym and cellphone service reimbursements. The Company reserves the right to modify or change these benefits programs at any time, with or without notice.Return to Search Result",
			"Benefits:\n\nAs a UW employee, you will enjoy generous benefits and work/life programs. For a complete description of our benefits for this position, please visit our website, click here.\n\nAs a UW employee, you have a unique opportunity to change lives on our campuses, in our state and around the world. UW employees offer their boundless energy, creative problem solving skills and dedication to build stronger minds and a healthier world.\n\nUW faculty and staff also enjoy outstanding benefits, professional growth opportunities and unique resources in an environment noted for diversity, intellectual excitement, artistic pursuits and natural beauty.\n\nThe Legacy Survey of Space and Time (LSST), which will be carried out by the Vera C. Rubin Observatory, is the flagship ground-based astronomical survey of the 2020s. With an estimated start date in 2024, LSST will generate the deepest-ever, multi-color, 10-year-long movie of the southern sky, detecting 30 billion stars and galaxies and amassing 100 PB of imaging and catalog data. This is part of a trend of ever-larger and more complex astronomical imaging surveys: science is at an inflection point where the volume of data and the software infrastructure we use to analyze it can fundamentally change our understanding of the universe. The scientific reach of the LSST will be extraordinary, addressing questions such as: how did the Solar System form; what governs the birth and death of stars; how does dark matter sculpt the shape of our Galaxy; will an asteroid devastate the Earth in the next century; what is the nature of the dark energy that drives the expansion of our Universe?\n\nThe software team that you will be part of will begin by developing software for direct and immediate scientific application to data from existing surveys, scaling up to the data volume and complexity of LSST in 3 years. As a Software Engineer, you will work with full-stack engineering teams at the University of Washington and Carnegie Mellon University. You will develop cloud-based and HPC software platforms built on JupyterHub that will enable the analysis of time series and static data from the LSST. You will work with astronomers and scientists to integrate their analysis code into these scalable analysis frameworks utilizing tools such as Spark and Dask. Development will be undertaken in an agile/Scrum environment to deliver high quality software. It will incorporate software best practices such as peer code review, to produce secure, testable, maintainable, and extensible code. The duties for this position include the following:\n\nDesign and Implement Applications (60%):\n\nDesign and implement applications/systems that offer a wide range of functionalities to the research\n\nContribute to other deliverables as designed by LINCC leadership.   Collaborate with research design (20%):\n\nCollaborate with researchers in the design, planning, and implementation software that enriches research productivity and reliability.\n\nBuild understanding of research activities through regular engagements.\n\nAnalyze Business Processes/Procedures and Define/Document Customer Requirements   Problem Resolution/Project Tasks (15%):\n\nPerform analysis and troubleshooting for application issues and process challenges\n\nResponsible for the successful completion of assigned project tasks with minimum supervision.   Other Duties (5%)\n\nProvide weekly status reports to the management or as required. Information should be accurate, timely, and pertinent.\n\nShare in 24/7 on-call duties with other team members as required.\n\nParticipate in all aspects of improving the team, including education/training of other team members and contributing to process/communication improvement initiatives.\n\nWork with manager to set professional goals for career development.   Minimum Requirements:\n\nA bachelors degree in Computer Science, Electrical Engineering, or related field.\n\nA minimum of 3 years of experience in software engineering.\n\nProgramming experience with at least one modern language such as Python, Java, C++ including object-oriented design.\n\nExperience cultivating positive and productive professional relationships with individuals from diverse social, cultural, and political contexts and ability to build rapport quickly.   Desired:\n\nExperience with software infrastructure, cloud deployment, high performance computing, and scalable architectures.\n\nExcellent written and oral communication skills and excellent problem-solving skills   Application Process:  The application process for UW positions may include completion of a variety of online assessments to obtain additional information that will be used in the evaluation process. These assessments may include Work Authorization, Cover Letter and/or others. Any assessments that you need to complete will appear on your screen as soon as you select \u201cApply to this position\u201d. Once you begin an assessment, it must be completed at that time; if you do not complete the assessment you will be prompted to do so the next time you access your \u201cMy Jobs\u201d page. If you select to take it later, it will appear on your \"My Jobs\" page to take when you are ready. Please note that your application will not be reviewed, and you will not be considered for this position until all required assessments have been completed.\n\nCommitted to attracting and retaining a diverse staff, the University of Washington will honor your experiences, perspectives and unique identity. Together, our community strives to create and maintain working and learning environments that are inclusive, equitable and welcoming.\n\nThe University of Washington is an affirmative action and equal opportunity employer. All qualified applicants will receive consideration for employment without regard to race, color, religion, sex, sexual orientation, gender identity, gender expression, national origin, age, protected veteran or disabled status, or genetic information.\n\nTo request disability accommodation in the application process, contact the Disability Services Office at 206-543-6450 or dso@uw.edu.\n\nApplicants considered for this position will be required to disclose if they are the subject of any substantiated findings or current investigations related to sexual misconduct at their current employment and past employment. Disclosure is required under Washington state law.\n\nReturn to Search Result",
			"Changing the world through digital experiences is what Adobe\u2019s all about. We give everyone\u2014from emerging artists to global brands\u2014everything they need to design and deliver exceptional digital experiences! We\u2019re passionate about empowering people to create beautiful and powerful images, videos, and apps, and transform how companies interact with customers across every screen.\n\nWe\u2019re on a mission to hire the very best and are committed to creating exceptional employee experiences where everyone is respected and has access to equal opportunity. We realize that new ideas can come from everywhere in the organization, and we know the next big idea could be yours!\n\nWho we are \nAt Marketo ( an Adobe company ) we are growing the world\u2019s leading engagement platform that empowers marketers to deliver the authentic experiences customers desire at scale. Our team is fueled with a passion for innovation, growth, and a dedication to making the Marketer successful. We hire multifaceted, hardworking, and innovative individuals who thrive in fast-paced environments. \nThe Opportunity \nAre you ready to collaborate with the world\u2019s largest technology companies? Do you enjoy diving into existing codebase s and learning what makes them tick ? Can you think creatively and find unique ways to solve problems?\n\nIf so, we\u2019d love to hear from you!\n\nMarketo is seeking a Software Development Engineer to join our Customer Engineering Team (CET) . We \u2019 re a team of creative problem - solvers with a passion for helping our customers achieve their business goals. As advocates for some of our largest customers, we are in a unique position to both develop our own solutions and assist other component teams in delivering quality features across the platform to support our highest-scale needs .\n\nWork with highly-available data streams, RESTful APIs and both internal and external interfaces that support and empower our users . Learn to anticipate our customer\u2019s needs through a suite of powerful monitoring tools and the support of your peers . Participate in cross-cutting platform investigations and find ways to unlock new levels of performance.\n\nWhile c urrently remote , t his position will move to a hybrid , in - office position as Adobe forms its future work vision. The core team is in Portland, OR while other associated teams are in Seattle, WA, and San Jose, CA . \nWhat you\u2019ll do\n\nCollaborate and solution with some of our biggest customers\n\nWork with data streams and APIs to provide enhanced automation capabilities\n\nBuild tools to alleviate support bottlenecks\n\nProactively monitor for improvement opportunities\n\nEnhance scalability and performance across the platform \nWhat you have\n\n5 + years working i n SaaS platforms &amp; technologies\n\nExperience planning and implementing architecture for new services or components.\n\nStrong grasp of data and system performance and tuning for KPIs\n\nAn emphasis on back-end development (Java or PHP preferred)\n\nExpertise working with SQL and NoSQL data stores ( MySQL, Postgres , Mon g oDB)\n\nSolid understanding of Docker or other container orchestration systems\n\nExcellent communication skills and an eagerness to collaborate! \nBonus Points\n\nExperience in consulting and/or customer-facing roles\n\nExpertise building RESTful APIs and microservices\n\nUnderstanding of Scrum / Agile Methodologies\n\nExperience working with extremely large data sets\n\nAffinity for APM and monitoring tools (New Relic, Wavefront, Vivid Cortex)\n\nBachelor\u2019s Degree in Computer Science or related discipline \nOur compensation reflects the cost of labor across several U.S. geographic markets, and we pay differently based on those defined markets. The U.S. pay range for this position\u202fis $101,500 -- $194,300 annually. Pay\u202fwithin this range varies by work location\u202fand may also depend on job-related knowledge, skills,\u202fand experience. Your recruiter can share more about the specific salary range for the job location during the hiring process.\n\nAt Adobe, for sales roles starting salaries are expressed as total target compensation (TTC = base + commission), and short-term incentives are in the form of sales commission plans. Non-sales roles starting salaries are expressed as base salary and short-term incentives are in the form of the Annual Incentive Plan (AIP).\n\nIn addition, certain roles may be eligible for long-term incentives in the form of a new hire equity award.\n\nAdobe is proud to be an Equal Employment Opportunity and affirmative action employer. We do not discriminate based on gender, race or color, ethnicity or national origin, age, disability, religion, sexual orientation, gender identity or expression, veteran status, or any other applicable characteristics protected by law. Learn more.\n\nAdobe aims to make Adobe.com accessible to any and all users. If you have a disability or special need that requires accommodation to navigate our website or complete the application process, email accommodations@adobe.com or call (408) 536-3015.\n\nAdobe values a free and open marketplace for all employees and has policies in place to ensure that we do not enter into illegal agreements with other companies to not recruit or hire each other\u2019s employees.Return to Search Result",
			"To get the best candidate experience, please consider applying for a maximum of 3 roles within 12 months to ensure you are not duplicating efforts.\n\nJob Category Software Engineering\n\nJob Details\n\nSalesforce Inc. seeks Senior Software Engineer in Seattle, WA:\n\nJob Duties : Design and implement new capabilities to clean, combine, and reshape data. Build a state-of-the-art front end utilizing the full capabilities of React, Redux, and Typescript. Dive into Java and C++ backends to connect different parts of the Tableau Prep product. Drive and take full ownership of the end-to-end quality of the code deployed to Production. Promote code quality by writing clean, readable, maintainable, modular, and efficient code. Resolve customer bugs and support issues in a timely manner. Telecommuting is an option. Some travel to Salesforce offices may be required.\n\nMinimum Requirements : Master\u2019s degree (or its foreign degree equivalent) in Computer Science, Engineering (any field), or a related quantitative discipline, and two (2) years of experience in the field of software engineering/program analysis or two (2) years of experience in the job offered OR Bachelor\u2019s degree (or its foreign degree equivalent) in Computer Science, Engineering (any field), or a related quantitative discipline, and five (5) years of progressively responsible experience in the field of software engineering/program analysis or five (5) years of experience in the job offered.\n\nA related technical degree required (Computer Science, Engineering (any field)).\n\nSpecial Skill Requirements : (1) Java (2 years); (2) REST (1 year); (3) JavaScript (2 years); (4) HTML (1 year); (5) SQL (1 year); (6) jQuery (1 year); (7) ASP.NET (1 year); (8) MVC (2 years); (9) AWS (2 years); (10) Electron (3 years); and (11) Typescript (3 years). Any suitable combination of education, training and/or experience is acceptable. Education, experience and criminal background checks will be conducted. Telecommuting is an option. Some travel to Salesforce offices may be required.\n\nCertain roles may be eligible for incentive compensation, equity, and benefits. More details about company benefits can be found at the following link: https://www.salesforcebenefits.com .\n\nSubmit a resume using the apply button on this posting or by email at: onlinejobpostings@salesforce.com at Job # 21-13589. Salesforce is an Equal Opportunity &amp; Affirmative Action Employer. Education, experience and criminal background checks will be conducted.\n\n#LI-DNI\n\nAccommodations\n\nIf you require assistance due to a disability applying for open positions please submit a request via this Accommodations Request Form .\n\nPosting Statement\n\nAt Salesforce we believe that the business of business is to improve the state of our world. Each of us has a responsibility to drive Equality in our communities and workplaces. We are committed to creating a workforce that reflects society through inclusive programs and initiatives such as equal pay, employee resource groups, inclusive benefits, and more. Learn more about Equality at Salesforce and explore our benefits.\n\nSalesforce.com and Salesforce.org are Equal Employment Opportunity and Affirmative Action Employers. Qualified applicants will receive consideration for employment without regard to race, color, religion, sex, sexual orientation, gender perception or identity, national origin, age, marital status, protected veteran status, or disability status. Salesforce.com and Salesforce.org do not accept unsolicited headhunter and agency resumes. Salesforce.com and Salesforce.org will not pay any third-party agency or company that does not have a signed agreement with Salesforce.com or Salesforce.org .\n\nSalesforce welcomes all.\n\nMore details about our company benefits can be found at the following link: https://www.getsalesforcebenefits.com/\n\nFor Washington-based roles, the base salary hiring range for this position is $168,709 to $203,490.\n\nCompensation offered will be determined by factors such as location, level, job-related knowledge, skills, and experience. Certain roles may be eligible for incentive compensation, equity, benefits. More details about our company benefits can be found at the following link: https://www.salesforcebenefits.com.\nReturn to Search Result",
			"Want to build new features and improve existing products that more than a billion people around the world use? Are you interested in working on highly impactful technical challenges to help the world be more open and connected? Want to solve unique, large-scale, highly complex technical problems? Our development cycle is extremely fast, and we've built tools to keep it that way. It's common to write code and have it running live on the site just hours later. We push code to the site continuously and have small teams that build products that are touched by millions of people around the world. If you work for us, you will be able to make an impact immediately.Facebook is seeking Software Engineers to join our engineering team. You can help build the next-generation of systems behind Facebook's products, create web applications that reach millions of people, build high volume servers and be a part of a team that\u2019s working to help people connect with each other around the globe.This position is full-time and there are minimal travel requirements.\n\nSoftware Engineer, Machine Learning Responsibilities:\n\nDevelop a strong understanding of relevant product area, codebase, and/or systems\n\nDemonstrate proficiency in data analysis, programming and software engineering\n\nProduce high quality code with good test coverage, using modern abstractions and frameworks\n\nWork independently, use available resources to get unblocked, and complete tasks on-schedule by exercising strong judgement and problem solving skills\n\nMaster Facebook\u2019s development standards from developing to releasing code in order to take on tasks and projects with increasing levels of complexity\n\nActively seek and give feedback in alignment with Facebook\u2019s Performance Philosophy\n\nMinimum Qualifications:\n\nExperience coding in an industry-standard language (e.g. Java, Python, C++, JavaScript)\n\nCurrently has, or is in the process of obtaining a Bachelor's degree in Computer Science, Computer Engineering, relevant technical field, or equivalent practical experience. Degree must be completed prior to joining Meta.\n\nMust obtain work authorization in country of employment at the time of hire, and maintain ongoing work authorization during employment\n\nPreferred Qualifications:\n\nDemonstrated software engineering experience from previous internship, work experience, coding competitions, or publications\n\nCurrently has, or is in the process of obtaining, a Bachelors or Masters degree in Computer Science or a related field\n\nMeta is proud to be an Equal Employment Opportunity and Affirmative Action employer. We do not discriminate based upon race, religion, color, national origin, sex (including pregnancy, childbirth, reproductive health decisions, or related medical conditions), sexual orientation, gender identity, gender expression, age, status as a protected veteran, status as an individual with a disability, genetic information, political views or activity, or other applicable legally protected characteristics. You may view our Equal Employment Opportunity notice here. We also consider qualified applicants with criminal histories, consistent with applicable federal, state and local law. We may use your information to maintain the safety and security of Meta, its employees, and others as required or permitted by law. You may view Meta's Pay Transparency Policy, Equal Employment Opportunity is the Law notice, and Notice to Applicants for Employment and Employees by clicking on their corresponding links. Additionally, Meta participates in the E-Verify program in certain locations, as required by law\n\nReturn to Search Result"
		]

		for detail in details:

			text      = self.nlp ( detail )

			sentences = list ( text.sents )


			for index, sentence in enumerate ( sentences ):

				print ( f' >> sentence [ {index} ]:', sentence )


		#####################
		##  WRITE CONTENT  ##

		with open ( file, 'w+' ) as writer:

			bar = '-' * 58

			writer.write ( f'\n\n<{bar}>\n\n'.join ( details ) )

	def pipeline ( self ):

		# print ( ' >> self.job_offers', self.job_offers )

		for site in self.job_offers:

			if self.job_offers [ site ] is not None:

				for offer in self.job_offers [ site ]:

					# print ( ' >> offer:', offer [ 'details' ] )

					# texts = ["This is a text", "These are lots of texts", "..."]
					# - docs = [nlp(text) for text in texts]
					# + docs = list(nlp.pipe(texts))


					documents = list ( self.nlp.pipe ( offer [ 'details' ] ) )

					print ( ' >> documents:', documents )
