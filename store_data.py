import pandas as pd
from utility import calculate_timestamp, data_attributes_list, get_today_date
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

class StoreData():
    def __init__(self,start_date, end_date, method, keyword) -> None:
        self.start_date = str(start_date).replace('-','_')
        self.end_date = str(end_date).replace('-','_')
        self.method = method
        self.keyword = keyword
        self.year,self.month,self.day = get_today_date()
        self.csv_file = f'{self.start_date}-{self.end_date}-{calculate_timestamp()}.csv'

    def store_csv(self,data):
        
        tweets_df2 = pd.DataFrame(
            data, columns=data_attributes_list)
        tweets_df2.to_csv(self.csv_file)

    def store_csv_s3(self):
        # Upload csv file to S3
        s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        s3_storagepath = f'twitter/raw-files/{self.keyword}/{self.method}/{self.year}/{self.month}/{self.day}/{self.csv_file}'
        s3.upload_file(self.csv_file, 'nacci-datalake', s3_storagepath)


