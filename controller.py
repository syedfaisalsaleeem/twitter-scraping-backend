from utility import data_attributes_list
import snscrape.modules.twitter as sntwitter
import pandas as pd
from _mongodb import MongoDBPython

class Controller():
    def __init__(self, *args):
        self.key_phrases = args[0]
        self.start_date = args[1]
        self.end_date = args[2]
        self.db = args[3]

    def twitter_crawler(self):
        key_phrases = self.key_phrases
        start_date = self.start_date
        end_date = self.end_date
        
        # Get the tweets
        tweets_list2 = []
        data = {'key_phrase': '','data':tweets_list2 ,'start_date': None, 'end_date': None}

        for key_phrase in key_phrases:
            data['key_phrase'] = key_phrase
            data['start_date'] = start_date
            data['end_date'] = end_date
            count = 0
            insert = 0 
            id_to_update = None
            csv_filename = f'{key_phrase}-{start_date}_{end_date}.csv'
            # Using TwitterSearchScraper to scrape data and append tweets to list
            for i, tweet in enumerate(sntwitter.
                                    TwitterSearchScraper(f'{key_phrase} since:{start_date} until:{end_date}').get_items()):
                if count > 500:
                    print('Updating Data')
                    count = 0
                    print(f'Latest Stored Tweet Date: {tweet.date}')
                    data['data'] = tweets_list2
                    # Insert data into MongoDB
                    if insert == 0 :
                        insert = 1
                        id_to_update = MongoDBPython(self.db).insert_data(data)
                        tweets_df2 = pd.DataFrame(
                        tweets_list2, columns=data_attributes_list)
                        tweets_df2.to_csv(str(id_to_update)+'.csv')
                    else:
                        MongoDBPython(self.db).update_data(id_to_update,tweets_list2)
                        tweets_df2 = pd.DataFrame(
                        tweets_list2, columns=data_attributes_list)
                        tweets_df2.to_csv(str(id_to_update)+'.csv')

                    # break
                print(f'{len(tweets_list2)} tweets scrapped for "{key_phrase}". Tweet Date: {tweet.date}')
                count += 1
                values = [str(tweet.url), str(tweet.date), str(tweet.content), str(tweet.renderedContent), str(tweet.id), str(tweet.user.username),
                                    str(tweet.user.id), str(tweet.user.displayname), str(tweet.user.description), str(tweet.user.rawDescription),
                                    str(tweet.user.descriptionUrls), str(tweet.user.verified), str(tweet.user.created),
                                    str(tweet.user.followersCount), str(tweet.user.friendsCount), str(tweet.user.statusesCount),
                                    str(tweet.user.favouritesCount), str(tweet.user.listedCount), str(tweet.user.mediaCount),
                                    str(tweet.user.location), str(tweet.user.protected), str(tweet.user.linkUrl), str(tweet.user.linkTcourl),
                                    str(tweet.user.profileImageUrl), str(tweet.user.profileBannerUrl), str(tweet.user.label), str(tweet.user),
                                    str(tweet.replyCount), str(tweet.retweetCount), str(tweet.likeCount), str(tweet.quoteCount),
                                    str(tweet.conversationId), str(tweet.lang), str(tweet.source), str(tweet.sourceUrl), str(tweet.sourceLabel),
                                    str(tweet.outlinks), str(tweet.tcooutlinks), str(tweet.media), str(tweet.retweetedTweet), str(tweet.quotedTweet),
                                    str(tweet.mentionedUsers), str(tweet.coordinates), str(tweet.place), str(tweet.hashtags), str(tweet.cashtags)]
                items = {i:y for i,y in zip(data_attributes_list, values)}
                tweets_list2.append(dict(items))

            # Insert data into MongoDB
            id_to_update = MongoDBPython(self.db).insert_data(data)
            tweets_df2 = pd.DataFrame(
            tweets_list2, columns=data_attributes_list)
            tweets_df2.to_csv(str(id_to_update)+'.csv')

    def start(self):
        try:
            self.twitter_crawler()
            return "sucessfull",200
        except Exception as e:
            return str(e),500

class Controller2():
    def get_twitter(self,db):
        self.db = db
        try:
            return  MongoDBPython(self.db).get_all_twitter_key_phrases()
        except Exception as e:
            return str(e),500
        
    def get_specific_keyphrase(self, db, id):
        self.db = db
        try:
            return  MongoDBPython(self.db).get_specific_keyphrasedata(id)
        except Exception as e:
            return str(e),500

