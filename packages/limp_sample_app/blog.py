from limp.base_module import BaseModule
from limp.enums import Event
from limp.classes import ATTR, PERM, EXTN, ATTR_MOD, CACHE, ANALYTIC
from limp.config import Config

from bson import ObjectId

import re


class Blog(BaseModule):
	'''Blog module provides data type and controller for blog feature in conjunction with BlogCat module. It allows admins to create blog posts by passing `title`, `content`, `cat`, and `status` attrs in doc. Blog docs with status `published` are accessible by all with `read` method.'''

	collection = 'blogs'
	attrs = {
		'user': ATTR.ID(),
		'status': ATTR.LITERAL(literal=['draft', 'pending', 'rejected', 'published']),
		'title': ATTR.LOCALE(),
		'subtitle': ATTR.LOCALE(),
		'permalink': ATTR.STR(),
		'content': ATTR.LOCALE(),
		'tags': ATTR.LIST(list=[ATTR.STR()]),
		'cat': ATTR.ID(),
		'access': ATTR.ACCESS(),
		'create_time': ATTR.DATETIME(),
	}
	diff = True
	defaults = {
		'tags': [],
		'subtitle': ATTR_MOD(
			condition=lambda skip_events, env, query, doc, scope: 'subtitle'
			not in doc.keys()
			or not doc['subtitle'],
			default=lambda skip_events, env, query, doc, scope: {Config.locale: ''},
		),
		'permalink': ATTR_MOD(
			condition=lambda skip_events, env, query, doc, scope: 'permalink'
			not in doc.keys()
			or not doc['permalink'],
			default=lambda skip_events, env, query, doc, scope: re.sub(
				r'\s+', '-', re.sub(r'[^\s\-\w]', '', doc['title'][Config.locale])
			),
		),
		'access': {'anon': True, 'users': [], 'groups': []},
	}
	unique_attrs = ['permalink']
	extns = {
		'user': EXTN(module='user', attrs=['name']),
		'cat': EXTN(module='blog_cat'),
	}
	cache = [
		CACHE(
			condition=lambda skip_events, env, query: str(env['session']._id)
			== 'f00000000000000000000012'
		)
	]
	analytics = [
		ANALYTIC(
			condition=lambda skip_events, env, query, doc, method: method == 'read'
			and '_id' in query,
			doc=lambda skip_events, env, query, doc, method: {
				'event': 'BLOG_READ_ID',
				'subevent': query['_id'][0],
				'args': {'query': query._query},
				'score': 1,
			},
		),
		ANALYTIC(
			condition=lambda skip_events, env, query, doc, method: method == 'read'
			and 'cat' in query,
			doc=lambda skip_events, env, query, doc, method: {
				'event': 'BLOG_READ_CAT',
				'subevent': query['cat'][0],
				'args': {'query': query._query},
				'score': 0,
			},
		),
	]
	methods = {
		'read': {
			'permissions': [
				PERM(privilege='read'),
				PERM(
					privilege='*',
					query_mod={'status': 'published', 'access': '$__access'},
				),
			]
		},
		'create': {'permissions': [PERM(privilege='create')]},
		'update': {
			'permissions': [
				PERM(privilege='admin', doc_mod={'user': True}),
				PERM(privilege='update', query_mod={'user': '$__user'}),
			],
			'query_args': {'_id': ATTR.ID()},
		},
		'delete': {
			'permissions': [
				PERM(privilege='admin'),
				PERM(privilege='update', query_mod={'user': '$__user'}),
			],
			'query_args': {'_id': ATTR.ID()},
		},
	}

	async def pre_create(self, skip_events, env, query, doc, payload):
		blog_cat_results = await Config.modules['blog_cat'].read(
			skip_events=[Event.PERM], env=env, query=[{'_id': doc['cat']}]
		)
		if not blog_cat_results.args.count:
			return self.status(
				status=400,
				msg='Invalid BlogCat.',
				args={'code': 'LIMP-SIMPLE-APP_INVALID_CAT'},
			)
		return (skip_events, env, query, doc, payload)


class BlogCat(BaseModule):
	'''BlogCat module provides data type and controller for blog feature in conjunction with Blog module. It allows admins to create blog categories by passing `title`, and `desc` attrs in doc. Blogs categories are accessible by all with `read` method.'''

	collection = 'blogs_cats'
	attrs = {'user': ATTR.ID(), 'title': ATTR.LOCALE(), 'desc': ATTR.LOCALE()}
	diff = True
	methods = {
		'read': {
			'permissions': [
				PERM(privilege='read'),
				PERM(privilege='*', query_mod={'$attrs': ['title', 'desc']}),
			]
		},
		'create': {'permissions': [PERM(privilege='create')]},
		'update': {
			'permissions': [PERM(privilege='update')],
			'query_args': {'_id': ATTR.ID()},
		},
		'delete': {
			'permissions': [PERM(privilege='delete')],
			'query_args': {'_id': ATTR.ID()},
		},
	}