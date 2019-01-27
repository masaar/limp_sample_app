from base_module import BaseModule
from event import Event
from utils import DictObj

from bson import ObjectId

class Blog(BaseModule):
	use_template = True
	template = 'content'
	collection = 'blogs'
	optional_attrs = ['subtitle', 'tags', 'permalink', 'access', 'expiry_time']
	extns = {
		'user':['user', ['*']],
		'cat':['blog_cat', ['*']]
	}

	def pre_create(self, session, query, doc):
		if doc['cat']:
			try:
				ObjectId(doc['cat'])
			except:
				return DictObj({
					'status':400,
					'msg':'Value for attr \'{}\' couldn\'t be converted to \'id\' from request on module \'{}_{}\'.'.format('cat', *self.__module__.replace('modules.', '').upper().split('.')),
					'args':{'code':'{}_{}_INVALID_ATTR'.format(*self.__module__.replace('modules.', '').upper().split('.'))}
				})
			blog_cat_results = self.modules['blog_cat'].methods['read'](skip_events=[Event.__PERM__], session=session, query={'_id':{'val':doc['cat']}})
		if not blog_cat_results.args.count:
			return DictObj({
				'status':400,
				'msg':'Value for attr \'{}\' is invalid from request on module \'{}_{}\'.'.format('cat', *self.__module__.replace('modules.', '').upper().split('.')),
				'args':{'code':'{}_{}_INVALID_CAT'.format(*self.__module__.replace('modules.', '').upper().split('.'))}
			})
		return (session, query, doc)

class BlogCat(BaseModule):
	use_template = True
	template = 'content_cat'
	collection = 'blogs_cats'
	extns = {
		'user':['user', ['*']]
	}