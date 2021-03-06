import datetime
from .store_data import StoreData
import snscrape.modules.twitter as sntwitter
from application.app.cronjob.controllers.cronjob_controller import CronJobController
from pymongo import MongoClient

class CronJobTwitterScrapingController():
    def __init__(self, key_phrases, start_date, end_date, method, breaking=False, db=None):
        self.key_phrases = key_phrases
        self.start_date = start_date
        self.end_date = end_date
        self.method = method
        self.breaking = breaking
        self.db = db


    def get_date(self):
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now() - datetime.timedelta(hours=168)
        return str(start_date), str(end_date)

    def twitter_crawler(self):
        cronjob_controller = CronJobController(self.db)
        start_date,end_date = self.get_date()
        all_ids = []
        keyphrases = []
        for values in cronjob_controller.get_all_cronjob_key_phrases(method="cronjob"):
            all_ids.append(values.get('_id'))
            keyphrases.append(values.get('key_phrase'))
            
        # Get the tweets
        for insert_id,key_phrase in zip(all_ids,keyphrases):
            tweets_list2 = []
            # store_data key represents the data needs to be stored in csv or not
            store = StoreData(start_date, end_date, method=self.method, keyword=key_phrase, store_data=True)
            # update the status of the key_phrase to running
            cronjob_controller.update_status(insert_id,"processing")
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
                s3_path = store.store_csv_s3()
                store.delete_store_csv()
                print('files upload in s3')
                # Update the status of the data in mongodb
                cronjob_controller.update_location(insert_id,"completed",s3_path)
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
        res = CronJobTwitterScrapingController(key_phrases=['freekick','futsol','cricket'], start_date='2021-06-01', end_date="2021-06-02", method='scraped', breaking=True, db=db_twitter).start()
        if res[1] == 200:
            print("test case passed")
        else:
            print(res)
    except Exception as e:
        print(e)
        print('test case failed')

# test_twitter_controller()