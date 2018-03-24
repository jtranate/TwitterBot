
# API Key Information
API = {
    'CONSUMER_KEY': '',
    'CONSUMER_SECRET': '',
    'ACCESS_TOKEN': '',
    'ACCESS_TOKEN_SECRET': '',
    'TWITTER_HANDLE': ''
}

SEARCH = {
    'CRITERIA' : ['retweet to win', 'rt to win'],
    'FILTERS': '-filter:retweets AND -filter:replies',
    'RESULT_TYPE': 'recent', #['popular', 'recent', 'mixed']
    'NUM_POSTS': 40
}

# RULES to see if we need to Follow, Favorite, or Comment a post to win
CONTEST_RULES = {
    'RETWEET': {"Retweet", "RT", "rt", 'Rt', 'retweet', 'RETWEET'},
    'RULES': ['to enter', 'to win'], # Words that must show if we want to enter (helps filter out)
    'BOT': ['enter', 'win', 'sweepstakes'],
    'FOLLOW' : {'follow', 'Follow', 'FOLLOW'},
    'FAVORITE' : {'Fav', 'favorite', 'FAVORITE', 'Favorite', 'favourite', 'FAVOURITE', 'Favourite'},
    'COMMENT' : {'comment', 'COMMENT', 'Comment'},
}

# Maximum number allowed to follow based on certain Twitter rules
MAX_FOLLOW = 2000

# Database Information
# Number of people to unfollow if we reach our maximum number of people to follow
NUM_UNFOLLOW = 10

# Table name which holds the id's
TABLE = 'following'

# Path Filename of SQLITE3 Database
FILENAME = 'TwitterbotDB'

# names in username to ignore
IGNORE_USERS = ['bot', 'lvbroadcasting', 'ilove70315673', 'retweeejt', 'a_yush3']

# Minutes to wait before running again
WAIT_TIME = 1
