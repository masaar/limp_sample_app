from limp.base_module import BaseModule
from limp.classes import ATTR, PERM, ATTR_MOD
from limp.config import Config


class Album(BaseModule):
	'''Album module provides data type and controller for albums feature. It allows admins to create albums by passing `name`, `desc` and `photos` attrs in doc. Albums are accessible by all with `read` method.'''

	collection = 'albums'
	attrs = {
		'user': ATTR.ID(),
		'code': ATTR.COUNTER(pattern='A$__values:0-$__counters.album_counter', values=[
			lambda skip_events, env, query, doc: 42
		]),
		'name': ATTR.LOCALE(),
		'desc': ATTR.LOCALE(),
		'photos': ATTR.LIST(
			list=[
				ATTR.TYPED_DICT(
					dict={'desc': ATTR.LOCALE(), 'file': ATTR.FILE(types=['image/*'])}
				)
			]
		),
		'create_time': ATTR.DATETIME(),
	}
	diff = True
	defaults = {
		'desc': ATTR_MOD(
			condition=lambda skip_events, env, query, doc, scope: 'desc'
			not in doc.keys()
			or not doc['desc'],
			default=lambda skip_events, env, query, doc, scope: {
				Config.locale: doc['name'][Config.locale]
			},
		),
		'photos:0.desc': ATTR_MOD(
			condition=lambda skip_events, env, query, doc, scope: 'desc'
			not in scope.keys()
			or not scope['desc'],
			default=lambda skip_events, env, query, doc, scope: {Config.locale: ''},
		),
	}
	methods = {
		'read': {'permissions': [PERM(privilege='*')]},
		'create': {'permissions': [PERM(privilege='create')]},
		'update': {
			'permissions': [
				PERM(privilege='admin'),
				PERM(
					privilege='update',
					query_mod={'user': '$__user'},
					doc_mod={'user': None},
				),
			],
			'query_args': {'_id': ATTR.ID()},
		},
		'delete': {
			'permissions': [PERM(privilege='delete')],
			'query_args': {'_id': ATTR.ID()},
		},
		'retrieve_file': {'permissions': [PERM(privilege='*')], 'get_method': True},
	}