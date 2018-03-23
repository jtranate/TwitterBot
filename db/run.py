""" Simple script to create the database and table if it does not exist """

import sqlite3


PATH = '../'
FILENAME = 'Twitterbot'

if __name__ == '__main__':
    print("Ensuring Database is setup...")

    conn = sqlite3.connect(PATH + FILENAME + '.sqlite3')
    # conn.execute("DROP TABLE following")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS following(
            user_id BIGINT PRIMARY KEY,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()

    print("Database setup Complete")
