import settings, twython


def get_twython_instance(api):
    """ Initialize an instance of Twython with variables needed """
    print "Connecting to Twitter API..."
    return twython.Twython(
                    api['CONSUMER_KEY'],
                    api['CONSUMER_SECRET'],
                    api['ACCESS_TOKEN'],
                    api['ACCESS_TOKEN_SECRET']
                    )

def is_bot(username):
    """ Determine if the post was made by a bot """
    username = username.replace("0", 'o').lower()
    if 'bot' in username:
        return True

    return False

def search(twitter, criteria, filters, num_posts, res_type):
    """ Search on twitter for RT contests

    @param twitter: Twython instance to use
    @param critera: Phrase to search for
    @param filters: Filters to use during search
    @param num_posts: Number of posts to return
    @param res_type: Result type ['mixed', 'popular', 'recent']
    @return collection of Tweets

    https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    """
    print "Searching for '" + criteria + "'"
    print "\tFilters: " + filters
    print "\tNumber of posts: " + `num_posts`
    print "\tResult Type: " + res_type
    return twitter.search(q=criteria + ' ' + filters, count=num_posts, result_type=res_type, lang='en') #change to recent


def enter_contest(twitter, tweets, contest_rules):
    COMMENT_POST = lambda x: "@" + x + " I want to Win!"

    for data in tweets:
        post_id_str = data['id_str']
        post_id = data['id']
        user_id_str = data['user']['id_str']
        user_screen_name = data['user']['screen_name']
        if is_bot(user_screen_name):
            continue

        try:
            retweeted = False
            for word in contest_rules['RETWEET']:
                if word in data['text'].replace('#', '').split(' '):
                    # Retweet to enter
                    twitter.retweet(id=post_id_str)
                    print "Retweeted post "
                    print "\tPost ID: " + post_id_str
                    print "\tUsername: " + user_id_str
                    print "\tTweet: " + data['text'].replace("\n", '')
                    retweeted = True
                    break

            if not retweeted:
                continue
        except twython.TwythonError:
            # Already retweeted this
            continue

        followed = favorited = commented = False
        for word in data['text'].split(' '):
            if word in contest_rules['FOLLOW']:
                twitter.create_friendship(screen_name=user_screen_name)
                followed = True
            if word in contest_rules['FAVORITE']:
                twitter.create_favorite(id=post_id_str)
                favorited = True
            if word in contest_rules['COMMENT']:
                twitter.update_status(status=COMMENT_POST(user_screen_name), in_reply_to_status_id=post_id)
                commented = True

        print "\tFollowed: " + `followed`
        print "\tFavorited: " + `favorited`
        print "\tCommented: " + `commented`

if __name__ == '__main__':
    twitter = get_twython_instance(settings.API)

    for criteria in settings.SEARCH['CRITERIA']:
        response = search(twitter, criteria, settings.SEARCH['FILTERS'], 5, 'recent')
        enter_contest(twitter, response['statuses'], settings.CONTEST_RULES)
