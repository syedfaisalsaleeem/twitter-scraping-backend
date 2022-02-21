import datetime
from store_data import StoreData
import snscrape.modules.twitter as sntwitter
from _mongodb import MongoDBPython
from pymongo import MongoClient
class Controller():
    def __init__(self, key_phrases, start_date, end_date, method, breaking=False, db=None):
        self.key_phrases = key_phrases
        self.start_date = start_date
        self.end_date = end_date
        self.method = method
        self.breaking = breaking
        self.db = db

    def twitter_crawler(self):
        key_phrases = self.key_phrases
        start_date = self.start_date
        end_date = self.end_date
        mongo_obj = MongoDBPython(self.db)
        today_date = str(datetime.date.today())
        insert_ids =[mongo_obj.insert_data({"key_phrase":key_phrase,"start_date":today_date,"status":"pending"})  for key_phrase in key_phrases ]
        # Get the tweets
        for insert_id,key_phrase in zip(insert_ids,key_phrases):
            tweets_list2 = []
            # store_data key represents the data needs to be stored in csv or not
            store = StoreData(start_date, end_date, method=self.method, keyword=key_phrase, store_data=True)
            # Using TwitterSearchScraper to scrape data and append tweets to list
            for i, tweet in enumerate(sntwitter.
                                    TwitterSearchScraper(f'{key_phrase} since:{start_date} until:{end_date}').get_items()):
                if self.breaking == True:
                        break

                print(f'{len(tweets_list2)} tweets scrapped for "{key_phrase}". Tweet Date: {tweet.date}')
                values = [tweet.url, tweet.date, tweet.content, tweet.renderedContent, tweet.id, tweet.user.username,
                             tweet.user.id, tweet.user.displayname, tweet.user.description, tweet.user.rawDescription,
                             tweet.user.descriptionUrls, tweet.user.verified, tweet.user.created,
                             tweet.user.followersCount, tweet.user.friendsCount, tweet.user.statusesCount,
                             tweet.user.favouritesCount, tweet.user.listedCount, tweet.user.mediaCount,
                             tweet.user.location, tweet.user.protected, tweet.user.linkUrl, tweet.user.linkTcourl,
                             tweet.user.profileImageUrl, tweet.user.profileBannerUrl, tweet.user.label, tweet.user,
                             tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount,
                             tweet.conversationId, tweet.lang, tweet.source, tweet.sourceUrl, tweet.sourceLabel,
                             tweet.outlinks, tweet.tcooutlinks, tweet.media, tweet.retweetedTweet, tweet.quotedTweet,
                             tweet.mentionedUsers, tweet.coordinates, tweet.place, tweet.hashtags, tweet.cashtags]
                tweets_list2.append(values)

            try:
                # Insert data into csv file
                store.store_csv(tweets_list2)
                store.store_csv_s3()
                print('files upload in s3')
                # Update the status of the data in mongodb
                mongo_obj.update_data(insert_id,"completed")
            except Exception as e:
                print(e)
                print('Error in storing data')

            del tweets_list2

        return "sucessfull",200


    def start(self):
        try:
            self.twitter_crawler()
            return "sucessfull",200
        except Exception as e:
            return str(e),500


def test_twitter_controller():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db_twitter = client['twitter']
        res = Controller(key_phrases=['freekick','futsol','cricket'], start_date='2021-06-01', end_date="2021-06-02", method='scraped', breaking=True, db=db_twitter).start()
        if res[1] == 200:
            print("test case passed")
        else:
            print(res)
    except Exception as e:
        print(e)
        print('test case failed')

# test_twitter_controller()