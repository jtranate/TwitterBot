
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
    'RESULT_TYPE': ['recent', 'popular'], #['popular', 'recent', 'mixed']
    'NUM_POSTS': 70 # Number of posts to get when searching
}

# RULES to see if we need to Follow, Favorite, or Comment a post to win
CONTEST_RULES = {
    'RETWEET': {"retweet", "rt"},
    'RULES': ['to enter', 'to win'], # Words that must show if we want to enter (helps filter out)
    'BOT': ['enter', 'win', 'sweepstakes'],
    'FOLLOW' : {'follow'},
    'FAVORITE' : {'fav', 'favorite', 'favourite'},
    'COMMENT' : {'comment'},
}

# Maximum number allowed to follow based on certain Twitter rules
MAX_FOLLOW = 2000

# Number of people to unfollow if we reach our maximum number of people to follow
NUM_UNFOLLOW = 10

# Table name which holds the id's
TABLE = 'following'

# Filename of SQLITE3 Database
FILENAME = 'TwitterbotDB'

# names in username to ignore
IGNORE_USERS = ['bot', 'lvbroadcasting', 'ilove70315673', 'retweeejt', 'a_yush3', 'solodmhub', 'jerice50', 'feryooit', 'kogilligan']

# Minutes to wait before running again
WAIT_TIME = 30

# Random Quote API to post randomly
QUOTE_API = 'http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1'

# Log to Console; If False, will log to a file instead
LOG_TO_CONSOLE = True
