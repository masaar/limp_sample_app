from base_module import BaseModule
from event import Event
from config import Config

from bson import ObjectId

import re

class Blog(BaseModule):
	collection = 'blogs'
	attrs = {
		'user':'id',
		'status':('draft', 'pending', 'rejected', 'published'),
		'title':'locale',
		'subtitle':'locale',
		'permalink':'str',
		'content':'locale',
		'tags':['str'],
		'cat':'id',
		'access':'access',
		'create_time':'datetime'
	}
	diff = True
	defaults = {'tags':[]}
	unique_attrs = ['permalink']
	extns = {
		'user':['user', ['name', 'bio']],
		'cat':['blog_cat', ['*']]
	}
	methods = {
		'read':{
			'permissions':[['read', {}, {}], ['*', {'status':'published', 'access':'$__access'}, {}]]
		},
		'create':{
			'permissions':[['admin', {}, {}], ['create', {}, {}]]
		},
		'update':{
			'permissions':[['admin', {}, {}], ['update', {'user':'$__user'}, {'user':None}]],
			'query_args':['_id']
		},
		'delete':{
			'permissions':[['admin', {}, {}], ['delete', {'user':'$__user'}, {}]],
			'query_args':['_id']
		}
	}

	def pre_create(self, skip_events, env, session, query, doc):
		blog_cat_results = self.modules['blog_cat'].read(skip_events=[Event.__PERM__], env=env, session=session, query=[[{'_id':doc['cat']}]])
		if not blog_cat_results.args.count:
			return {
				'status':400,
				'msg':'Invalid BlogCat.',
				'args':{'code':'LIMP-SIMPLE-APP_INVALID_CAT'}
			}
		if 'subtitle' not in doc.keys(): doc['subtitle'] = {locale:'' for locale in Config.locales}
		if 'permalink' not in doc.keys(): doc['permalink'] = re.sub(r'\s+', '-', re.sub(r'[^\s\-\w]', '', doc['title'][Config.locale]))
		if 'access' not in doc.keys():
			doc['access'] = {
				'anon':True,
				'users':[],
				'groups':[]
			}
		return (skip_events, env, session, query, doc)


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
			'permissions':[['read', {}, {}], ['*', {'$attrs':['title', 'desc']}, {}]]
		},
		'create':{
			'permissions':[['create', {}, {}]]
		},
		'update':{
			'permissions':[['update', {}, {}]],
			'query_args':['_id']
		},
		'delete':{
			'permissions':[['delete', {}, {}]],
			'query_args':['_id']
		}
	}