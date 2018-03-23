
import sqlite3, os


class DbManager(object):
    """ DbManger holds the SQLlite3 instance and custom operations"""

    # Maximum number allowed to follow based on certain Twitter rules
    MAX_FOLLOW = 40

    # Number of people to unfollow if we reach our maximum number of people to follow
    NUM_UNFOLLOW = 5

    # Table name which holds the id's
    TABLE = 'following'

    # Path and Filename of SQLITE3 Database
    PATH = '/config/'
    FILENAME = 'Twitterbot'

    def __init__(self, following):
        """ Initialize the database

        @param following: A list of user id's to clean up our database
        """

        print("Ensuring Database is setup...")

        database = self.PATH + self.FILENAME + '.sqlite3'

        conn = sqlite3.connect(database)
        conn.execute(" \
            CREATE TABLE IF NOT EXISTS " + self.TABLE + "( \
                user_id BIGINT PRIMARY KEY, \
                date_added DATETIME DEFAULT CURRENT_TIMESTAMP \
            )"
        )
        conn.close()

        print("Database setup Complete")

        self.cursor = sqlite3.connect(database)

        print("Following : " + str(self.cursor.execute("SELECT COUNT(*) FROM " + self.TABLE).fetchone()[0]) )
        print("Updating Database with current people you are following...")

        # Get all Users id's in the database
        db_ids = self.cursor.execute("SELECT user_id FROM " + self.TABLE).fetchall()
        db_ids = {str(i[0]) for i in db_ids}

        # Make following list into set
        following = {str(i) for i in following}

        # Delete the id's in the database we no longer are following
        delete_ids = db_ids - following
        conditions = " OR user_id=".join(delete_ids)
        if len(conditions) > 0:
            self.cursor.execute("DELETE FROM " + self.TABLE + " WHERE user_id=" + conditions)

        # Add the id's we are currently following
        add_ids = following - db_ids
        if len(add_ids) > 0:
            conditions = ""
            last = add_ids.pop()
            for id in add_ids:
                conditions += "(%s), " % id
            conditions += "(%s)" % last
            if len(conditions) > 0:
                self.cursor.execute("INSERT INTO " + self.TABLE + " (user_id) VALUES " + conditions)


        self.num_following = self.cursor.execute("SELECT COUNT(*) FROM " + self.TABLE).fetchone()[0]

        self.commit()
        print("Update Complete.")
        print("You are following %d accounts" % self.num_following)


    def upsert_user(self, user_id):
        """ Upsert the user into the database

        @param user_id: User Id to insert or update the timestamp of
        @return list of user_id's to delete
        """

        self.cursor.execute("INSERT OR REPLACE INTO " + self.TABLE + " (user_id) VALUES(" + user_id + ")")
        self.num_following += 1

        self.commit()
        return self.delete_user_check()

    def delete_user_check(self):
        """ Delete users if we are exceeding the amount of people we can follow

        @return list of user_id's that were deleted
        """
        delete = []
        # If we are following more than 2000 people, we want to unfollow some people
        if self.num_following >= self.MAX_FOLLOW:
            criteria = " FROM " + self.TABLE + " ORDER BY date_added ASC LIMIT " + str(self.NUM_UNFOLLOW)
            result = self.cursor.execute("SELECT user_id " + criteria)
            self.cursor.execute("DELETE " + criteria)
            delete = [row[0] for row in result]
            self.num_following -= self.NUM_UNFOLLOW

        self.commit()
        return delete

    def commit(self):
        """ Commit changes """
        self.cursor.commit()
