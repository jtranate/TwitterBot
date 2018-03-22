import twython




SEARCH = ['retweet to win', 'rt to win']
FOLLOW = {'follow', 'Follow', 'FOLLOW'}
FAVORITE = {'Fav', 'favorite', 'FAVORITE', 'Favorite'}
COMMENT = {'comment', 'COMMENT', 'Comment'}

COMMENT_POST = lambda x: "@" + x + " I want to Win!"

twitter = twython.Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
# until = YYYY-MM-DD; already has a 7 day limit
#since_id = returns results with id greater than specified id
response = twitter.search(q=SEARCH[0] + "-filter:retweets AND -filter:replies", count=5, result_type='popular') #change to recent
# print response['statuses']
for data in response['statuses']:
    print data['id_str'] + " - " + data['user']['id_str'] + " - " + data['text']
    # twitter.retweet(id=data['id_str'])

    for word in data['text'].split(' '):
        if word in FOLLOW:
            twitter.create_friendship(screen_name=data['user']['screen_name'])['following']
        if word in FAVORITE:
            twython.create_favorite(id=data['id_str'])
        if word in COMMENT:
            twython.update_status(status=COMMENT_POST(data['user']['id']), in_reply_to_status_id=data['id'])
