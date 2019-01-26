from base_module import BaseModule
from event import Event

from bson import binary

class Module(BaseModule):
	collection = 'modules'
	attrs = {
		'user':'id',
		'locale':'locale',
		'logo':'file',
		'attrs': 'attrs',
		'list':['str'],
		'create_time':'create_time',
		'diff':'diff'
	}
	optional_attrs = ['attrs', 'list']
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
		'retrieve_logo': {
			'permissions': [['*', {}, {}]],
			'query_args': ['!_id', '!var'],
			'get_method': True
		}
	}

	def pre_create(self, session, query, doc):
		doc['logo'] = doc['logo'][0]
		doc['logo']['content'] = binary.Binary(bytes(doc['logo']['content'].values()))
		return (session, query, doc)
	
	def retrieve_logo(self, skip_events=[], env={}, session=None, query={}, doc={}):
		del query['var']
		results = self.methods['read'](skip_events=[Event.__PERM__, Event.__ON__], session=session, query=query)
		if not results['args']['count']:
			return {
				'status': 404
			}
		module = results['args']['docs'][0]
		if not module.logo:
			return {
				'status': 404
			}
		return {
			'status': 291,
			'msg': module.logo['content'],
			'args': {
				'name': module.logo['name'],
				'type': module.logo['type'],
				'size': module.logo['size']
			}
		}