import sqlite3

conn = sqlite3.connect('database.db')


with open('schema.sql') as db:
    conn.executescript(db.read())

cur = conn.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", ('1st Post', 'Content for the first post'))

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", ('2nd Post', 'Content for the second post'))

conn.commit()
conn.close()
