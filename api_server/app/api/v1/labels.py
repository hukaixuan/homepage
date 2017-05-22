# coding:utf-8
from flask import request, g
from ...models import db, Post, User, Label
from ...decorators import json, collection, etag
from . import api
from ... import auth


@api.route('/labels', methods=['GET'])
@etag
@json
@collection(Label)
def get_labels():
    return Label.query


@api.route('/labels/<int:id>', methods=['GET'])
@etag
@json
def get_label(id):
    return Label.query.get_or_404(id)


@api.route('/labels', methods=['POST'])
@auth.login_required
@json
def new_label():
    label = Label().import_data(request.get_json(force=True))
    label.user_id = g.user.id
    db.session.add(label)
    db.session.commit()
    return {}, 201, {'Location': label.get_url()}


@api.route('/labels/<int:id>', methods=['PUT'])
@auth.login_required
@json
def edit_label(id):
    label = Label.query.get_or_404(id)
    if label.user_id != g.user.id:
        return {"error":"Forbidden"}, 403
    label.import_data(request.get_json(force=True))
    db.session.add(label)
    db.session.commit()
    return {}


@api.route('/labels/<int:id>', methods=['DELETE'])
@auth.login_required
@json
def delete_label(id):
    label = Label.query.get_or_404(id)
    if label.user_id != g.user.id:
        return {"error":"Forbidden"}, 403
    db.session.delete(label)
    db.session.commit()
    return {}

# GET      api/v1.0/labels
# GET      api/v1.0/labels/[label_id]
# POST    api/v1.0/labels
# PUT      api/v1.0/lables/[label_id]
# DELETE   api/v1.0/labels/[label_id]














