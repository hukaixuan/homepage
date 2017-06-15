# coding:utf-8 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from .helpers import args_from_url
from .errors import ValidationError
import time

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    pic = db.Column(db.String(128))
    describe = db.Column(db.String(128))
    token = db.Column(db.String(64), nullable=True, unique=True)
    
    @property
    def posts(self):
        return Post.query.filter_by(user_id=self.id).all()

    @property
    def sites(self):
        return Site.query.filter_by(user_id=self.id).all()

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

    def export_data(self):
        return {'self_url': self.get_url(),
                'username': self.username,
                'pic': self.pic,
                'describe': self.describe,
                'posts': [post.get_url() for post in self.posts],
                'sites': [site.get_url() for site in self.sites]
                }

    def import_data(self, data):
        try:
            self.username = data['username'] if data.get('username') else self.username
            self.pic = data['pic'] if data.get('pic') else self.pic
            self.describe = data['describe'] if data.get('describe') else self.describe
            if data.get('password'): self.password = data.get('password')
            # self.password = data.get('password') if data.get('password') else self.password
        except KeyError as e:
            raise ValidationError('Invalid class: missing ' + e.args[0])
        return self

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=24*60*60):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])


class Site(db.Model):
    __tablename__ = 'sites'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    url = db.Column(db.String(128))

    @property
    def user(self):
        return User.query.get(self.user_id)

    def get_url(self):
        return url_for('api.get_site', id=self.id, _external=True)

    def export_data(self):
        return {
                'self_url': self.get_url(),
                'user': self.user.get_url(),
                'name': self.name,
                'url': self.url
        }

    def import_data(self, data):
        try:
            self.user_id = data['user_id'] if data.get('user_id') else self.user_id
            self.name = data['name'] if data.get('name') else self.name
            self.url = data['url'] if data.get('url') else self.url
        except KeyError as e:
            raise ValidationError('Invalid class: missing ' + e.args[0])
        return self


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    site_id = db.Column(db.Integer)     # 通过爬虫爬取存储
    label_id = db.Column(db.Integer)
    title = db.Column(db.String(128))
    img = db.Column(db.TEXT)
    content = db.Column(db.TEXT)
    # likes = db.Column(db.Integer)   # 通过爬虫爬取存储
    post_time = db.Column(db.DateTime)  # 通过爬虫爬取存储
    origin_url = db.Column(db.String(128)) # 文章原网址，通过爬虫爬取存储
    state = db.Column(db.String(64))  # draft 草稿、publish 发布
    timestamp = db.Column(db.Integer, default=int(time.time()))
    
    @property
    def comments(self):
        return Comment.query.filter_by(post_id=self.id, parent_id=0).all()   #只选出一级评论（不是回复其他评论的评论）

    @property
    def author(self):
        return User.query.filter_by(id=self.user_id).first()

    @property
    def label(self):
        return Label.query.filter_by(id=self.label_id).first()

    @property
    def site(self):
        return Site.query.filter_by(id=self.site_id).first()

    def get_url(self):
        return url_for('api.get_post', id=self.id, _external=True)

    def export_data(self):
        return {
                    'id': self.id,
                    'self_url': self.get_url(),
                    'origin_url': self.origin_url,
                    'author': self.author.get_url(),
                    'site': self.site.get_url() if self.site else None,
                    'label': self.label.get_url() if self.label else None,
                    'label_name': self.label.name if self.label else None,
                    'title': self.title,
                    'img': self.img,
                    'content': self.content,
                    'post_time': self.post_time,
                    'state': self.state,
                    'timestamp': self.timestamp,
                    'comments':[
                        {comment.get_url():[reply.get_url() for reply in comment.replies]} for comment in self.comments
                        ]
                }

    def import_data(self, data):
        try:
            self.user_id = data['user_id'] if data.get('user_id') else self.user_id
            self.label_id = data['label_id'] if data.get('label_id') else self.label_id
            # self.site_id = data['site_id'] if data.get('site_id') else self.site_id
            self.title = data['title'] if data.get('title') else self.title
            self.content = data['content'] if data.get('content') else self.content
            self.state = data['state'] if data.get('state') else self.state
            # self.post_time = data['post_time'] if data.get('post_time') else self.post_time
            self.timestamp = data['timestamp'] if data.get('timestamp') else self.timestamp
        except KeyError as e:
            raise ValidationError('Invalid class: missing ' + e.args[0])
        return self


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, default=0)
    content = db.Column(db.TEXT)
    timestamp = db.Column(db.Integer, default=int(time.time()))
    
    @property
    def post(self):
        """该评论所属的POST"""
        return Post.query.filter_by(id=self.post_id).first()

    @property
    def replies(self):
        """回复该评论的评论"""
        return Comment.query.filter_by(parent_id=self.id).all()

    @property
    def author(self):
        return User.query.get(self.user_id)

    def get_url(self):
        return url_for('api.get_comment', post_id=self.post_id, id=self.id, _external=True)

    def export_data(self):
        return {
                    'id': self.id,
                    'self_url': self.get_url(),
                    'author': self.author.get_url(),
                    'post': self.post.get_url(),
                    'replies':[reply.get_url() for reply in self.replies],
                    'content': self.content,
                    'timestamp': self.timestamp,
                }

    def import_data(self, data):
        try:
            self.user_id = data['user_id'] if data.get('user_id') else self.user_id
            self.post_id = data['post_id'] if data.get('post_id') else self.post_id
            self.parent_id = data['parent_id'] if data.get('parent_id') else self.parent_id
            self.content = data['content'] if data.get('content') else self.content
            self.timestamp = data['timestamp'] if data.get('timestamp') else self.timestamp
        except KeyError as e:
            raise ValidationError('Invalid class: missing ' + e.args[0])
        return self


class Label(db.Model):
    __tablename__ = 'labels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    @property
    def posts(self):
        return Post.query.filter_by(label_id=self.id).all()

    def get_url(self):
        return url_for('api.get_label', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'self_url': self.get_url(),
            'name': self.name
        }

    def import_data(self, data):
        try:
            self.name = data['name'] if data.get('name') else self.name
        except KeyError as e:
            raise ValidationError('Invalid class: missing ' + e.args[0])
        return self



