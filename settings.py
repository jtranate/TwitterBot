
# API Key Information


SEARCH = {
    'CRITERIA' : ['retweet to win', 'rt to win'],
    'FILTERS': '-filter:retweets AND -filter:replies'
}

# RULES to see if we need to Follow, Favorite, or Comment a post to win
CONTEST_RULES = {
    'RETWEET': {"Retweet", "RT", "rt", 'Rt', 'retweet', 'RETWEET'},
    'FOLLOW' : {'follow', 'Follow', 'FOLLOW'},
    'FAVORITE' : {'Fav', 'favorite', 'FAVORITE', 'Favorite', 'favourite', 'FAVOURITE', 'Favourite'},
    'COMMENT' : {'comment', 'COMMENT', 'Comment'},
}
