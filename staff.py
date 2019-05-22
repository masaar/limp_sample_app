from base_module import BaseModule

class Staff(BaseModule):
	collection = 'staff'
	attrs = {
		'user':'id',
		'photo':'file',
		'name':'locale',
		'jobtitle':'locale',
		'bio':'locale',
		'create_time':'create_time'
	}
	diff = True
	extns = {
		'user':['user', ['*']]
	}
	methods = {
		'read':{
			'permissions':[['admin', {}, {}], ['*', {}, {}]]
		},
		'create':{
			'permissions':[['create', {}, {'user':'$__user'}]]
		},
		'update':{
			'permissions':[['admin', {}, {}], ['update', {'user':'$__user'}, {'user':None}]],
			'query_args':['!_id']
		},
		'delete':{
			'permissions':[['delete', {}, {}]],
			'query_args':['!_id']
		},
		'retrieve_file': {
			'permissions': [['*', {}, {}]],
			'query_args': ['!_id', '!var'],
			'get_method': True
		}
	}