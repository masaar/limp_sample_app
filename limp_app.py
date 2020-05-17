from limp.classes import APP_CONFIG, PACKAGE_CONFIG, ATTR

config = APP_CONFIG(
	name='limp_sample_app',
	version='0.0.2',
	# Use this App Config Attr to determine which env to use based on value of environment variable ENV
	env='$__env.ENV',
	envs={
		'dev_local':PACKAGE_CONFIG(
			debug=True,
			data_server='mongodb://localhost'
		),
		'dev_server':PACKAGE_CONFIG(
			debug=True,
			# Use this Config Attr to emulate test mode. Read more on Test Workflow on LIMP Docs.
			emulate_test=True,
			data_server='mongodb://admin:admin@mongodb',
			# Use this Config Attr to determine port on which app is served based on value of environment variable PORT. Any Config Attr can be set at root level
			port='$__env.PORT',
			# You can use data_name Config Attr for custom data_name per env
			# data_name='limp_data'
		),
		'prod':PACKAGE_CONFIG(
			# Use this App Config Attr to set debug mode based on existence of environment variable DEBUG
			debug='$__env.DEBUG',
			data_server='mongodb://admin:admin@prod',
			# Use this App Config Attr to force use of SSL connection
			data_ssl=True,
		)
	},

	# define name of the database for your app
	data_name='limp_data',
	# Define app locales in the form of language_COUNTRY
	locales=['ar_AE', 'en_AE'],
	# Define app default locale, which is the required value for LOCALE Attr Type
	locale='ar_AE',
	# Define user attrs, these are the app-specific attrs every User doc should have. You need to at least define one attr which should be later defined in 'user_auth_attrs'
	user_attrs={
		'email':ATTR.EMAIL(),
		# '...': ATTR....()
	},
	# Define which attrs of 'user_attrs' should be used to use for 'Session.auth' calls. This means, the attrs defined in this list are unique and should have a corresponding hash
	user_auth_attrs=['email'],
	# Set ADMIN doc values. This is the default ADMIN doc value that will be created to allow you to authenticate and manage the data
	admin_doc={
		'email':'admin@app.limp.masaar.com',
		# '...':'...'
	},
	# Define ADMIN password that will be used to generate the hashes
	admin_password='S0mE_V3Ry_STR0nG_P@SsW0rD',
	# Define ANON token. This token is used as salt across LIMP framework so it is very good idea to change it from default token
	# anon_token= '__ANON_TOKEN_f00000000000000000000012',
	# Define default privileges any authenticated user is having
	# default_privileges={
	# 	'module_name': ['privilege1', 'privilege2', ..., 'privilege0'],
	# }
	# Learn more about Config Attrs on LIMP Docs.
)