# Ancora Imparo.

from bson import ObjectId

def config():
	return {
		'envs':{
			'dev':{
				'data_server':'mongodb://localhost'
			},
			'prod':{
				'data_server':'mongodb://localhost'
			}
		},
		'data_name':'limp_data',
		'locales':['ar_AE', 'en_AE'],
		'locale':'ar_AE'
	}