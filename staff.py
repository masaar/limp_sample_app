from base_module import BaseModule
from event import Event

from bson import binary

class Staff(BaseModule):
	collection = 'staff'
	attrs = {
		'user':'id',
		'photo':'file',
		'name':'locale',
		'jobtitle':'locale',
		'bio':'locale',
		'create_time':'create_time',
		'diff':'diff'
	}
	extns = {
		'user':['user', ['*']]
	}
	methods = {
		'read':{
			'permissions':[['admin', {}, {}], ['read', {}, {}]]
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
		'retrieve_photo': {
			'permissions': [['*', {}, {}]],
			'query_args': ['!_id', '!var'],
			'get_method': True
		}
	}

	def pre_create(self, session, query, doc):
		doc['photo'] = doc['photo'][0]
		return (session, query, doc)
	
	def retrieve_photo(self, skip_events=[], env={}, session=None, query={}, doc={}):
		del query['var']
		results = self.methods['read'](skip_events=[Event.__PERM__, Event.__ON__], session=session, query=query)
		if not results['args']['count']:
			return {
				'status': 404
			}
		staff = results['args']['docs'][0]
		if not staff.photo:
			return {
				'status': 404
			}
		return {
			'status': 291,
			'msg': staff.photo['content'],
			'args': {
				'name': staff.photo['name'],
				'type': staff.photo['type'],
				'size': staff.photo['size']
			}
		}