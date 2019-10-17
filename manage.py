#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : dengsc


from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from click import echo
from demo import create_app
from demo.extensions import db

app = create_app()

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {
        'app': app,
        'db': db
    }


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main(['tests', '-q'])
    return exit_code


@manager.command
def urlmap():
    """Prints out all routes"""
    echo('{:50s} {:40s} {}'.format('Endpoint', 'Methods', 'Route'))
    for route in app.url_map.iter_rules():
        methods = ','.join(route.methods)
        echo(f'{route.endpoint:50s} {methods:40s} {route}')


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
