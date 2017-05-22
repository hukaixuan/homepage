# coding:utf-8
from flask import request, g
from ...models import db, Post, User, Label
from ...decorators import json, collection, etag
from . import api
from ... import auth


@api.route('/posts', methods=['GET'])
@etag
@json
@collection(Post)
def get_posts():
    return Post.query


@api.route('/posts/<int:id>', methods=['GET'])
@etag
@json
def get_post(id):
    return Post.query.get_or_404(id)


@api.route('/posts', methods=['POST'])
@auth.login_required
@json
def new_post():
    post = Post().import_data(request.get_json(force=True))
    post.user_id = g.user.id
    db.session.add(post)
    db.session.commit()
    return {}, 201, {'Location': post.get_url()}


@api.route('/posts/<int:id>', methods=['PUT'])
@auth.login_required
@json
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id != g.user.id:
        return {"error":"Forbidden"}, 403
    post.import_data(request.get_json(force=True))
    db.session.add(post)
    db.session.commit()
    return {}


@api.route('/posts/<int:id>', methods=['DELETE'])
@auth.login_required
@json
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id != g.user.id:
        return {"error":"Forbidden"}, 403
    db.session.delete(post)
    db.session.commit()
    return {}

@api.route('/users/<int:user_id>/posts', methods=['GET'])
@json
def get_posts_by_user(user_id):
    user = User.query.get_or_404(user_id)
    return {post.id: post.export_data() for post in user.posts}


@api.route('/labels/<int:label_id>/posts', methods=['GET'])
@json
def get_posts_by_label(label_id):
    label = Label.query.get_or_404(label_id)
    return {post.id: post.export_data() for post in label.posts}

# GET      api/v1.0/posts  √
# GET      api/v1.0/posts/[post_id]   √
# POST    api/v1.0/posts   √
# PUT      api/v1.0/posts/[post_id]  √
# DELETE      api/v1.0/posts/[post_id]  √
# GET      api/v1.0/users/[user_id]/posts
# GET      api/v1.0/labels/[label_id]/posts















