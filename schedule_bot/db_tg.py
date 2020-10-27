import sqlite3
import datetime


def db_table_create():
    conn = sqlite3.connect('../action_user.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   userid INT PRIMARY KEY,
                   name TEXT NOT NULL);""")
    cur.execute("""CREATE TABLE IF NOT EXISTS actions(
                   userid INT NOT NULL,
                   date TEXT NOT NULL,
                   action TEXT NOT NULL,
                   FOREIGN KEY (userid) REFERENCES users(userid));""")
    conn.commit()


def action2db(chat_id, username, action):
    conn = sqlite3.connect('../action_user.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM users WHERE userid = {chat_id}""")
    if len(cur.fetchall()) == 0:
        cur.execute(f"""INSERT INTO users
                        VALUES ({chat_id}, '{username}');""")
    cur.execute(f"""INSERT INTO actions
                    VALUES ({chat_id}, '{str(datetime.datetime.today().date())}', '{action}'); """)
    conn.commit()
