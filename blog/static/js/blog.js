var load_posts = function(data){
	"use strict";

	var author = data['author'],
		category = data['category'],
		query = data['query'],
		load_url = data['load_url'],
		load_flag = data['load_flag'],
		$button = $('#post-load-button'),
		offset = $button.data('offset'),
		new_offset = offset + 3;

	$button.data('offset', new_offset);

	$.ajax({
			url: load_url,
		data: {
			offset: new_offset,
			category: category,
			author: author,
			query: query
		}

		})
		.done(function(data) {
			var load_flag = data['load_flag'],
				posts = data['posts'],
				$post_container = $('.posts'),
				template = Handlebars.compile( $('#post_tpl').html());
			if (!load_flag) {
				$button.hide();
			}
			if (posts) {
				for (var i=0; i<posts.length; i++) {
					$post_container.append(template(posts[i]));
				}
			}
		})
		.fail(function(e) {
			console.log('fail', e);
		})
};