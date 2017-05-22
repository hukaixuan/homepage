# coding:utf-8
from flask import request, g
from ...models import db, User
from ...decorators import json, collection, etag
from . import api
from ... import auth


# 获取所有用户
@api.route('/users', methods=['GET'])
# @auth.login_required
@etag
@json
@collection(User)
def get_users():
    return User.query

# 根据id获取单个用户
@api.route('/users/<int:id>', methods=['GET'])
@etag
@json
def get_user(id):
    return User.query.get_or_404(id)


# 注册新用户
@api.route('/users', methods=['POST'])
@json
def new_user():
    user = User().import_data(request.get_json(force=True))
    db.session.add(user)
    db.session.commit()
    return {}, 201, {'Location': user.get_url()}


# @api.route('/users/<int:id>/registrations/', methods=['POST'])
# @json
# def new_user_registration(id):
#     user = User.query.get_or_404(id)
#     data = request.get_json(force=True)
#     data['user_url'] = user.get_url()
#     reg = Registration().import_data(data)
#     db.session.add(reg)
#     db.session.commit()
#     return {}, 201, {'Location': reg.get_url()}

# 编辑用户信息
@api.route('/users/<int:id>', methods=['PUT'])
@auth.login_required
@json
def edit_user(id):
    user = User.query.get_or_404(id)
    if user.id != g.user.id:
        return {"error":"Forbidden"}, 403
    user.import_data(request.get_json(force=True))
    db.session.add(user)
    db.session.commit()
    return {}

# 删除用户
@api.route('/users/<int:id>', methods=['DELETE'])
@auth.login_required
@json
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id != g.user.id:
        return {"error":"Frobidden"}, 403
    db.session.delete(user)
    db.session.commit()
    return {}
