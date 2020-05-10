from limp.classes import APP_CONFIG, PACKAGE_CONFIG

config = APP_CONFIG(
	name='limp_sample_app',
	version='0.0.0',
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
	}
)