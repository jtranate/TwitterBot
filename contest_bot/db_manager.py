
import sqlite3


# TODO: Mount database
class DbManager(object):
    """ DbManger holds the SQLlite3 instance and custom operations"""

    # Maximum number allowed to follow based on certain Twitter rules
    MAX_FOLLOW = 2000

    # Number of people to unfollow if we reach our maximum number of people to follow
    NUM_UNFOLLOW = 5

    def __init__(self, database, following):
        """ Initialize the database

        @param database: The path to the database
        @param following: A list of user id's to clean up our database
        """
        self.cursor = sqlite3.connect(database)

        print("Updating Database with current people you are following...")

        # Get all Users id's in the database
        db_ids = self.cursor.execute("SELECT user_id from following").fetchall()
        db_ids = {str(i[0]) for i in db_ids}

        following = {str(i) for i in following}

        # Delete the id's in the database we no longer are following
        delete_ids = db_ids - following
        conditions = " OR user_id=".join(delete_ids)
        if len(conditions) > 0:
            self.cursor.execute("DELETE FROM following WHERE user_id=" + conditions)

        # Add the id's we are currently following
        add_ids = following - db_ids
        conditions = ""
        last = add_ids.pop()
        for id in add_ids:
            conditions += "(%s), " % id
        conditions += "(%s)" % last
        if len(conditions) > 0:
            self.cursor.execute("INSERT INTO following (user_id) VALUES " + conditions)


        self.num_following = self.cursor.execute("SELECT COUNT(*) FROM following").fetchone()[0]
        self.cursor.execute("DELETE FROM following ORDER BY date_added ASC LIMIT " + str(self.NUM_UNFOLLOW))
        print("Update Complete.")
        print("You are following %d accounts" % self.num_following)


    def upsert_user(user_id):
        """ Upsert the user into the database

        @param user_id: User Id to insert or update the timestamp of
        @return list of user_id's to delete
        """
        delete = []


        self.cursor.execute("INSERT OR REPLACE INTO following (user_id) VALUES(" + user_id + ")")
        self.num_following += 1

        # If we are following more than 2000 people, we want to unfollow some people
        if self.num_following >= DbManger.MAX_FOLLOW:
            criteria = " FROM following ORDER BY date_added ASC LIMIT " + str(self.NUM_UNFOLLOW)
            result = self.cursor.execute("SELECT user_id " + criteria)
            self.cursor.execute("DELETE " + criteria)
            delete = [row[0] for row in result]
            self.num_following -= NUM_UNFOLLOW


        return delete
