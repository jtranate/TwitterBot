import twython, os, sys, shutil, time


def get_twython_instance(api):
    """ Initialize an instance of Twython with variables needed """

    logger.info( "Connecting to Twitter API...")
    return twython.Twython(
                    api['CONSUMER_KEY'],
                    api['CONSUMER_SECRET'],
                    api['ACCESS_TOKEN'],
                    api['ACCESS_TOKEN_SECRET']
                    )

def is_bot(username):
    """ Determine if the post was made by a bot """
    username = username.replace("0", 'o').lower()
    for user in settings.IGNORE_USERS:
        if user in username:
            return True

    return False

def get_contests(twitter, criteria):
    """ Search on twitter for RT contests

    @param twitter: Twython instance to use
    @param critera: Phrase to search for
    @return collection of Tweets

    https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    """
    filters = settings.SEARCH['FILTERS']
    num_posts = settings.SEARCH['NUM_POSTS']
    res_type = settings.SEARCH['RESULT_TYPE']
    logger.info("""
        \tSearching for '%s'
            \t\tFilters: %s
            \t\tNumber of posts: %d
            \t\tResult Type: %s
    """ % (criteria,
            filters,
            num_posts,
            res_type)
        )

    return twitter.search(q=criteria + ' ' + filters, count=num_posts, result_type=res_type, lang='en')


def enter_contest(twitter, db, tweets):
    """ Enter a contest

    @param twitter: Twython instance to use
    @param db: DbManager instance
    @param tweets: Tweets to look through and enter in
    """
    COMMENT_POST = lambda x: "@" + x + " I want to Win!. Pick me @" + settings.API['TWITTER_HANDLE']

    for data in tweets:
        post_id_str = data['id_str']
        post_id = data['id']
        user_id_str = data['user']['id_str']
        user_screen_name = data['user']['screen_name']
        if is_bot(user_screen_name):
            continue

        retweeted = False
        try:
            for word in settings.CONTEST_RULES['RETWEET']:
                if word in data['text'].replace('#', '').split(' '):
                    # Retweet to enter
                    twitter.retweet(id=post_id_str)
                    retweeted = True
                    break

            if not retweeted:
                continue
        except twython.TwythonError:
            # Already retweeted this
            continue

        followed = favorited = commented = False
        for word in data['text'].split(' '):
            if word in settings.CONTEST_RULES['FOLLOW']:

                # Delete users before creating the friendship
                unfollow = db.upsert_user(user_id_str)
                unfollow_users(twitter, unfollow)

                twitter.create_friendship(screen_name=user_screen_name, follow=True)
                followed = True
            if word in settings.CONTEST_RULES['FAVORITE']:
                twitter.create_favorite(id=post_id_str)
                favorited = True
            if word in settings.CONTEST_RULES['COMMENT']:
                twitter.update_status(status=COMMENT_POST(user_screen_name), in_reply_to_status_id=post_id)
                commented = True

        logger.info("""
            \tRetweeted Post:
                \t\tPost Id: %s
                \t\tUsername: %s
                \t\tFollowed: %r
                \t\tFavorited: %r
                \t\tCommented: %r
                \t\tTweet: %s
        """ % (post_id_str,
         user_id_str,
         followed,
         favorited,
         commented,
         data['text'].replace("\n",'')))


def unfollow_users(twitter, user_ids):
    """ Unfollow users on twitter

    @param twitter: Twython instance to use
    @param user_ids: list of user id's to unfollow
    """
    for user_id in user_ids:
        twitter.destroy_friendship(user_id=user_id)


if __name__ == '__main__':

    CURR_PATH = os.path.dirname(os.path.abspath(__file__))

    # Get path where database and settings are installed
    if sys.argv[1][-1] != '/':
        CONFIG_PATH = sys.argv[1] + '/'
    else:
        CONFIG_PATH = sys.argv[1]

    # Set up logger
    LOG_PATH = os.path.join(CONFIG_PATH, 'logs/')
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    import logger
    logger.setup(LOG_PATH)


    # Install settings if not yet installed
    if not os.path.exists(CONFIG_PATH + 'bot_settings.py'):
        shutil.move(os.path.join(CURR_PATH, 'settings.py'), CONFIG_PATH + 'bot_settings.py')
    sys.path.insert(0, CONFIG_PATH)


    import bot_settings as settings
    from db_manager import DbManager

    # Create twitter instance
    twitter = get_twython_instance(settings.API)

    # Initialize the Database
    following = twitter.get_friends_ids(screen_name = settings.API['TWITTER_HANDLE'])['ids']
    db = DbManager(following, CONFIG_PATH)
    unfollow_users(twitter, db.delete_user_check())

    
    for criteria in settings.SEARCH['CRITERIA']:
        response = get_contests(twitter, criteria)
        enter_contest(twitter, db, response['statuses'])
