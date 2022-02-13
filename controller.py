from store_data import StoreData
import snscrape.modules.twitter as sntwitter


class Controller():
    def __init__(self, key_phrases, start_date, end_date, method, breaking=False):
        self.key_phrases = key_phrases
        self.start_date = start_date
        self.end_date = end_date
        self.method = method
        self.breaking = breaking

    def twitter_crawler(self):
        key_phrases = self.key_phrases
        start_date = self.start_date
        end_date = self.end_date
        limit = 1000
        
        
        # Get the tweets
        tweets_list2 = []
        for key_phrase in key_phrases:
            count = 0
            data_inserted = False 
            store = StoreData(start_date, end_date, method=self.method, keyword=key_phrase)
            # Using TwitterSearchScraper to scrape data and append tweets to list
            for i, tweet in enumerate(sntwitter.
                                    TwitterSearchScraper(f'{key_phrase} since:{start_date} until:{end_date}').get_items()):
                if count > limit:
                    print('Updating Data')
                    count = 0
                    data_inserted = True
                    try:
                        # Insert data into csv file
                        store.store_csv(tweets_list2)
                        print(f'Latest Stored Tweet Date: {tweet.date}')
                        store.store_csv_s3()
                        print('files upload in s3')
                    except Exception as e:
                        print(e)
                        print('Error in storing data')
                    if self.breaking == True:
                        break

                print(f'{len(tweets_list2)} tweets scrapped for "{key_phrase}". Tweet Date: {tweet.date}')
                count += 1
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

            if data_inserted == False:
                # Insert data into csv file
                store.store_csv(tweets_list2)
                print(f'Latest Stored Tweet Date: {tweet.date}')
                # Upload csv file to S3
                store.store_csv_s3()
                print('files upload in s3')




    def start(self):
        try:
            self.twitter_crawler()
            return "sucessfull",200
        except Exception as e:
            return str(e),500
