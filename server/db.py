import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
import csv


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def reset_db():
    db = get_db()

    with current_app.open_resource('scheme.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with open('ecogame/items.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            db.execute(
                'INSERT INTO items (name, price) VALUES (?, ?)',
                (row['name'], row['price'])
            )
    db.commit()


@click.command('reset-db')
@with_appcontext
def reset_db_command():
    reset_db()
    click.echo('Database is resetted.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(reset_db_command)