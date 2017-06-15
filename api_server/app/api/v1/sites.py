# coding:utf-8
from flask import request, g
from ...models import db, Post, User, Label, Site
from ...decorators import json, collection, etag
from . import api
from ... import auth


@api.route('/sites', methods=['GET'])
@etag
@json
@collection(Site)
def get_sites():
    # return Site.query
    return Site.query

@api.route('/users/<int:user_id>/sites', methods=['GET'])
@json
def get_sites_by_user(user_id):
    user = User.query.get_or_404(user_id)
    return {site.id: site.export_data() for site in user.sites}


@api.route('/sites/<int:id>', methods=['GET'])
@etag
@json
def get_site(id):
    return Site.query.get_or_404(id)


@api.route('/sites', methods=['POST'])
# @auth.login_required
@json
def new_site():
    site = Site().import_data(request.get_json(force=True))
    site.user_id = g.user.id
    db.session.add(site)
    db.session.commit()
    return {}, 201, {'Location': site.get_url()}


@api.route('/sites/<int:id>', methods=['PUT'])
# @auth.login_required
@json
def edit_site(id):
    site = Site.query.get_or_404(id)
    if site.user_id != g.user.id:
        return {"error":"Forbidden"}, 403
    site.import_data(request.get_json(force=True))
    db.session.add(site)
    db.session.commit()
    return {}


@api.route('/sites/<int:id>', methods=['DELETE'])
# @auth.login_required
@json
def delete_site(id):
    site = Site.query.get_or_404(id)
    if site.user_id != g.user.id:
        return {"error":"Forbidden"}, 403
    db.session.delete(site)
    db.session.commit()
    return {}

# GET      api/v1.0/sites
# GET      api/v1.0/sites/[site_id]
# GET      api/v1.0/users/[user_id]/sites
# POST     api/v1.0/sites
# PUT      api/v1.0/lables/[site_id]
# DELETE   api/v1.0/sites/[site_id]














