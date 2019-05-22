from base_module import BaseModule
from event import Event
from config import Config

from bson import ObjectId

import re

class Blog(BaseModule):
	collection = 'blogs'
	attrs = {
		'user':'id',
		'status':('scheduled', 'draft', 'pending', 'rejected', 'published'),
		'title':'locale',
		'subtitle':'locale',
		'permalink':'str',
		'content':'locale',
		'tags':['str'],
		'cat':'id',
		'access':'access',
		'create_time':'time'
	}
	diff = True
	optional_attrs = ['subtitle', 'tags', 'permalink', 'access']
	extns = {
		'user':['user', ['*']],
		'cat':['blog_cat', ['*']]
	}
	methods = {
		'read':{
			'permissions':[['read', {}, {}], ['*', {}, {}]]
		},
		'create':{
			'permissions':[['admin', {}, {}], ['create', {}, {}]]
		},
		'update':{
			'permissions':[['admin', {}, {}], ['update', {'user':'$__user'}, {'user':None}]],
			'query_args':['!_id']
		},
		'delete':{
			'permissions':[['admin', {}, {}], ['delete', {'user':'$__user'}, {}]],
			'query_args':['!_id']
		}
	}

	def pre_create(self, env, session, query, doc):
		blog_cat_results = self.modules['blog_cat'].methods['read'](skip_events=[Event.__PERM__], env=env, session=session, query={'_id':{'val':doc['cat']}})
		if not blog_cat_results.args.count:
			return {
				'status':400,
				'msg':'Invalid BlogCat.',
				'args':{'code':'LIMP-SIMPLE-APP_INVALID_CAT'}
			}
		if 'subtitle' not in doc.keys(): doc['subtitle'] = {locale:'' for locale in Config.locales}
		if 'permalink' not in doc.keys(): doc['permalink'] = re.sub(r'\s+', '-', re.sub(r'[^\s\-\w]', '', doc['title'][Config.locale]))
		if 'tags' not in doc.keys(): doc['tags'] = []
		return (env, session, query, doc)


class BlogCat(BaseModule):
	collection = 'blogs_cats'
	attrs = {
		'user':'id',
		'title':'locale',
		'desc':'locale'
	}
	diff = True
	methods = {
		'read':{
			'permissions':[['*', {}, {}]]
		},
		'create':{
			'permissions':[['create', {}, {'user':'$__user'}]]
		},
		'update':{
			'permissions':[['update', {}, {}]],
			'query_args':['!_id']
		},
		'delete':{
			'permissions':[['delete', {}, {}]],
			'query_args':['!_id']
		}
	}