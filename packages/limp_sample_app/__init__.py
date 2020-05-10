# Ancora Imparo.
from limp.gateway import Gateway
from limp.utils import validate_attr
from limp.classes import PACKAGE_CONFIG, ATTR


config = PACKAGE_CONFIG(
	api_level='6.1',
	# Use sematic versioning for package version, so you keep package version and major corrosponding to API level, while minor is increamental per new version of the package, and reset it for new API level
	version='6.1.0',
	# Define package vars. This is shared storage across packages so you can have multiple packages communicating per specfic instructions defined here. You can also use this to define 'globals' dict which you can use across your modules
	# vars={
	# 	'globals':{
	# 		...
	# 	}
	# }
	# If you didn't define data_name at App Config (limp_app.py) then define it in app default package
	data_name='limp_data',
	# Define app locales in the form of country_LANGUAGE
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
