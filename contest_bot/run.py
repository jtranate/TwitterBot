import twython, os, sys, shutil, time, json, re, random, requests, html

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
    if username in settings.IGNORE_USERS:
        return True

    username = username.replace("0", 'o').lower()
    for user in settings.IGNORE_USERS:
        if user in username:
            return True

    return False

def get_contests(twitter, criteria, last_id, res_type):
    """ Search on twitter for RT contests

    @param twitter: Twython instance to use
    @param critera: Phrase to search for
    @param last_id: Latest Id we saw
    @param res_type: Type of result we would like to see
    @return collection of Tweets

    https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    """
    filters = settings.SEARCH['FILTERS']
    num_posts = settings.SEARCH['NUM_POSTS']
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

    return twitter.search(q=criteria + ' ' + filters,
                            count=num_posts,
                            result_type=res_type,
                            lang='en',
                            max_id = last_id)


def enter_contests(twitter, db, tweets):
    """ Enter contests contest

    @param twitter: Twython instance to use
    @param db: DbManager instance
    @param tweets: Tweets to look through and enter in
    """
    COMMENT_POST = lambda x: "@" + x + " I want to Win!. Pick me @" + settings.API['TWITTER_HANDLE']

    last_id = 1
    for data in tweets:
        post_id_str = data['id_str']
        post_id = data['id']
        user_id_str = data['user']['id_str']
        user_screen_name = data['user']['screen_name']
        text = data['text'].lower()
        if is_bot(user_screen_name):
            continue

        retweeted = False
        try:
            for word in settings.CONTEST_RULES['RETWEET']:
                if word in text.replace('#', '').split(' '):
                    valid = False
                    for rule in settings.CONTEST_RULES['RULES']:
                        if rule in text:
                            valid = True
                    if not valid: break

                    # Make sure user is not a bot...
                    timeline = twitter.get_user_timeline(user_id=user_id_str, count=5, exclude_replies="True")
                    bot_checker = 0
                    for post in timeline:
                        bot_text = post['text'].lower().replace('#','')
                        bot_hit = False
                        for txt in settings.CONTEST_RULES['RETWEET']:
                            if txt in bot_text:
                                bot_hit = True
                                break
                        if not txt:
                            for txt in settings.CONTEST_RULES['BOT']:
                                if txt in bot_text:
                                    bot_hit = True
                                    break
                        if bot_hit:
                            bot_checker += 1
                    if bot_checker >= 4:
                        break;

                    # Not a bot, now we can retweet
                    twitter.retweet(id=post_id_str)
                    retweeted = True
                    last_id = max(last_id, post_id)
                    break

            if not retweeted:
                continue
        except twython.TwythonError:
            # Already retweeted this
            continue

        followed = favorited = commented = False
        for word in text.split(' '):
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

        if retweeted:
            if bool(random.getrandbits(1)):
                if post_random(twitter):
                    logger.info("Posting random tweet")

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



    return last_id



def unfollow_users(twitter, user_ids):
    """ Unfollow users on twitter

    @param twitter: Twython instance to use
    @param user_ids: list of user id's to unfollow
    """
    for user_id in user_ids:
        twitter.destroy_friendship(user_id=user_id)

def construct_path(path):
    """ Correctly configure a path """
    if path[-1] != '/':
        path += '/'
    return path


def post_random(twitter):
    """ Post a random text to your account """
    clean_html = lambda txt: re.sub(re.compile('<.*?>'), '', txt)

    response = requests.get(url=settings.QUOTE_API)
    data = response.json()[0]
    author = data['title']
    text = html.unescape( data['content'][:280-len(author)-5] )
    twitter_post = clean_html(text) + " - " + author
    try:
        twitter.update_status(status=twitter_post)
    except:
        # Can't have duplicate statuses, so just skip it
        return False
    return True

if __name__ == '__main__':

    # Get path where database and settings are installed
    CONFIG_PATH = construct_path(sys.argv[1])
    APP_PATH = construct_path(sys.argv[2])

    # Install settings if not yet installed
    if not os.path.exists(CONFIG_PATH + 'bot_settings.py'):
        shutil.move(os.path.join(APP_PATH, 'settings.py'), CONFIG_PATH + 'bot_settings.py')
    sys.path.insert(0, CONFIG_PATH)


    # Set up logger
    LOG_PATH = os.path.join(CONFIG_PATH, 'logs/')
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    import logger
    logger.setup(LOG_PATH)


    import bot_settings as settings
    from db_manager import DbManager

    # Create twitter instance
    twitter = get_twython_instance(settings.API)

    # Initialize the Database
    following = twitter.get_friends_ids(screen_name = settings.API['TWITTER_HANDLE'])['ids']
    db = DbManager(following, CONFIG_PATH)
    unfollow_users(twitter, db.delete_user_check())

    last_id = 1
    while(1):
        logger.info("Searching...")
        for criteria in settings.SEARCH['CRITERIA']:
            for res_type in settings.SEARCH['RESULT_TYPE']:
                response = get_contests(twitter, criteria, last_id, res_type)
                post_id = enter_contests(twitter, db, response['statuses'])
                last_id = max(last_id, post_id)
        logger.info("Searching Complete...")
        logger.info("Waiting for next interation...")
        time.sleep(settings.WAIT_TIME * 60)
