import datetime


data_attributes_list = ['url', 'date', 'content', 'renderedContent', 'id',
                               'user.username', 'user.id', 'user.displayname', 'user.description',
                               'user.rawDescription', 'user.descriptionUrls', 'user.verified', 'user.created',
                               'user.followersCount', 'user.friendsCount', 'user.statusesCount',
                               'user.favouritesCount', 'user.listedCount', 'user.mediaCount', 'user.location',
                               'user.protected', 'user.linkUrl', 'user.linkTcourl', 'user.profileImageUrl',
                               'user.profileBannerUrl', 'user.label', 'user', 'replyCount', 'retweetCount',
                               'likeCount', 'quoteCount', 'conversationId', 'lang', 'source', 'sourceUrl',
                               'sourceLabel', 'outlinks', 'tcooutlinks', 'media', 'retweetedTweet',
                               'quotedTweet', 'mentionedUsers', 'coordinates', 'place', 'hashtags', 'cashtags']

def get_today_date():
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    return str(year), str(month), str(day)

def calculate_timestamp():
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    return str(ts)

def test_case_fortodays_date():
    x,y,z = get_today_date()
    if x != None and y != None and z != None:
        print(x,y,z)
        return "test case passed"
    else:
        return "test case failed"

def test_case_for_calculate_timestamp():
    x = calculate_timestamp()
    if x != None:
        print(x)
        return "test case passed"
    else:
        return "test case failed"
    
def message(status, message):
    response_object = {"status": status, "message": message}
    return response_object

def internal_err_resp():
    err = message(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500

def err_resp(msg, reason, code):
    err = message(False, msg)
    err["error_reason"] = reason
    return err, code