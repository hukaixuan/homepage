# coding:utf-8
from flask import request, g
from ...models import db, Post, User, Label, Comment
from ...decorators import json, collection, etag
from . import api
from ... import auth


@api.route('/posts/<int:post_id>/comments', methods=['GET'])
@etag
@json
# @collection(Comment)
def get_comments(post_id):
    post = Post.query.get(post_id)
    return {comment.id: comment.export_data() for comment in post.comments}


@api.route('/posts/<int:post_id>/comments/<int:id>', methods=['GET'])
@etag
@json
def get_comment(post_id, id):
    return Comment.query.get_or_404(id)


@api.route('/posts/<int:post_id>/comments', methods=['POST'])
# @auth.login_required
@json
def new_comment(post_id):
    comment = Comment().import_data(request.get_json(force=True))
    comment.user_id = g.user.id
    comment.post_id = post_id
    db.session.add(comment)
    db.session.commit()
    return {}, 201, {'Location': comment.get_url()}


@api.route('/posts/<int:post_id>/comments/<int:id>', methods=['PUT'])
# @auth.login_required
@json
def edit_comment(post_id, id):
    comment = Comment.query.get_or_404(id)
    if comment.user_id != g.user.id:
        return {"error":"Forbidden"}, 403
    comment.import_data(request.get_json(force=True))
    comment.post_id=post_id
    db.session.add(comment)
    db.session.commit()
    return {}


@api.route('/posts/<int:post_id>/comments/<int:id>', methods=['DELETE'])
# @auth.login_required
@json
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if comment.user_id != g.user.id:
        return {"error":"Forbidden"}, 403
    db.session.delete(comment)
    db.session.commit()
    return {}


# GET      api/v1.0/posts/[post_id]/comments    获取id为post_id的post的comments
# GET      api/v1.0/posts/<int:post_id>/comments/[comment_id]  获取id为comment_id的comment
# POST    api/v1.0/posts/[post_id]/comments   评论id为post_id 的post
# PUT      api/v1.0/posts/<int:post_id>/comments/[comment_id]  修改id为comment_id的comment
# DELETE   api/v1.0/posts/<int:post_id>/comments/[comment_id]  删除id为comment_id的comment













