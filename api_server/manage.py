# coding:utf-8
from flask import Flask, g
from flask_script import Manager, Server, Shell
from app import create_app
from app.models import db
import os
# from app.models import User, Post, Label

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def createdb(testdata=False):
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        if testdata:
            pass
            # classes = ['Algebra', 'Literature', 'Chemistry', 'Spanish',
            #            'Game Development', 'History', 'Music', 'Psychology',
            #            'Science', 'Photography', 'Drama', 'Business',
            #            'Python Programming']
            # for name in classes:
            #     c = Class(name=name)
            #     db.session.add(c)

            # u = User(username='miguel', password='python')
            # db.session.add(u)

            # db.session.commit()

# @manager.command
# def adduser(username):
#     """Register a new user."""
#     from getpass import getpass
#     password = getpass()
#     password2 = getpass(prompt='Confirm: ')
#     if password != password2:
#         import sys
#         sys.exit('Error: passwords do not match.')
#     db.create_all()
#     user = User(username=username, password=password)
#     db.session.add(user)
#     db.session.commit()
#     print('User {0} was registered successfully.'.format(username))


# @manager.command
# def test():
#     from subprocess import call
#     call(['nosetests', '-v',
#           '--with-coverage', '--cover-package=api', '--cover-branches',
#           '--cover-erase', '--cover-html', '--cover-html-dir=cover'])



def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('runserver', Server(use_debugger=True))
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

