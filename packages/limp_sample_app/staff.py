from limp.base_module import BaseModule
from limp.classes import ATTR, PERM


class Staff(BaseModule):
	'''Staff module provides data type and controller for staff feature. It allows admins to create staff docs by passing `photo`, `name`, `jobtitle`, and `bio` attrs in doc. Staff docs are accessible by all with `read` method. Staff doc photo attr can be retrieved by all with `retrieve_file` GET method.'''

	collection = 'staff'
	attrs = {
		'user': ATTR.ID(),
		'photo': ATTR.FILE(),
		'name': ATTR.LOCALE(),
		'jobtitle': ATTR.LOCALE(),
		'bio': ATTR.LOCALE(),
		'create_time': ATTR.DATETIME(),
	}
	diff = True
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