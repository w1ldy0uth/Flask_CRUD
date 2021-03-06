import random
import sqlite3
import string

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
app.config['SECRET_KEY'] = key


def get_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


def get_post(id: int):
    connection = get_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    connection.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    connection = get_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post_body = get_post(post_id)
    return render_template('post.html', post=post_body)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Enter some text in "Title" field')
        else:
            connection = get_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id: int):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Enter some text in "Title" field')
        else:
            connection = get_connection()
            connection.execute('UPDATE posts SET title = ?, content = ?' ' WHERE id = ?', (title, content, id))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    connection = get_connection()
    connection.execute('DELETE FROM posts WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
