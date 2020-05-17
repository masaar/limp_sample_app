from limp.test import TEST, STEP
from limp.classes import ATTR
from limp.enums import Event

auth_as_admin = TEST(
	[
		STEP.AUTH(
			var='email',
			val='admin@app.limp.masaar.com',
			hash='emailadmin@app.limp.masaar.comS0mE_V3Ry_STR0nG_P@SsW0rD__ANON_TOKEN_f00000000000000000000012',
		)
	]
)

create_blog_cat = TEST(
	[
		STEP.TEST(test='auth_as_admin'),
		STEP.CALL(
			module='blog_cat',
			method='create',
			doc={'title': ATTR.LOCALE(), 'desc': ATTR.LOCALE()},
		),
		STEP.SIGNOUT(),
		STEP.CALL(
			module='blog_cat',
			method='read',
			acceptance={'status': 200, 'args.count': 1},
		),
	]
)

create_blog_post = TEST(
	[
		STEP.TEST(test='create_blog_cat'),
		STEP.TEST(test='auth_as_admin'),
		STEP.CALL(
			module='blog',
			method='create',
			doc={
				'status': 'published',
				'title': ATTR.LOCALE(),
				'content': ATTR.LOCALE(),
				'tags': ATTR.LIST(list=[ATTR.STR()]),
				'cat': '$__steps:0.steps:1.results.args.docs:0._id',
			},
		),
		STEP.CALL(
			module='blog',
			method='create',
			doc={
				'status': 'draft',
				'title': ATTR.LOCALE(),
				'content': ATTR.LOCALE(),
				'tags': ATTR.LIST(list=[ATTR.STR()]),
				'cat': '$__steps:0.steps:1.results.args.docs:0._id',
			},
		),
		STEP.CALL(
			module='blog', method='read', acceptance={'status': 200, 'args.count': 2}
		),
		STEP.SIGNOUT(),
		STEP.CALL(
			module='blog', method='read', acceptance={'status': 200, 'args.count': 1}
		),
	]
)

update_blog_post_tags = TEST(
	[
		STEP.TEST(test='create_blog_post'),
		STEP.TEST(test='auth_as_admin'),
		STEP.CALL(
			module='blog',
			method='update',
			query=[{'_id': '$__steps:0.steps:2.results.args.docs:0._id'}],
			doc={'user': 'f00000000000000000000099', 'tags': {'$append': 'my_tag'}},
		),
		STEP.SIGNOUT(),
		STEP.CALL(
			module='blog',
			method='read',
			query=[{'_id': '$__steps:0.steps:2.results.args.docs:0._id'}],
			acceptance={
				'status': 200,
				'args.docs:0.tags': lambda results, call_results: call_results[
					'results'
				]
				.args.docs[0]
				.tags
				if 'my_tag' in call_results['results'].args.docs[0].tags
				else None,
			},
		),
	]
)

create_album = TEST(
	[
		STEP.TEST(test='auth_as_admin'),
		STEP.CALL(
			module='album',
			method='create',
			doc={
				'name': ATTR.LOCALE(),
				'photos': [
					{
						'desc': {'ar_AE': 'some description here'},
						'file': ATTR.FILE(types=['image/png', '*.png']),
					}
				],
			},
		),
		STEP.CALL(
			module='album', method='read', acceptance={'status': 200, 'args.count': 1}
		),
	]
)