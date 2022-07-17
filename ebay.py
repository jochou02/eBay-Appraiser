import os
import datetime
import sys
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

from dotenv import load_dotenv
load_dotenv()
API_KEY=os.getenv('api_key')

class Ebay_21(object):
    def __init__(self, API_KEY, input):
        self.api_key = API_KEY
        self.input = input

    def fetch(self):
        try:
            api = Connection(appid=self.api_key, config_file=None)
            response = api.execute('findItemsAdvanced', {'keywords': 'legos'})
            
            assert(response.reply.ack == 'Success')
            assert(type(response.reply.timestamp) == datetime.datetime)
            assert(type(response.reply.searchResult.item) == list)

            for item in response.reply.searchResult.item:
                print(f'Title: {item.title}, Price: {item.sellingStatus.currentPrice.value}')
                print(f'Condition: {item.condition.conditionDisplayName}')
                print(f'Buy it now available: {item.listingInfo.buyItNowAvailable}')
                print(f'Watchers: {item.listingInfo.watchCount}\n')

            item = response.reply.searchResult.item[0]
            assert(type(item.listingInfo.endTime) == datetime.datetime)
            assert(type(response.dict()) == dict)

        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    def parse(self):
        pass

# main driver

if __name__ == '__main__':
    input = sys.argv[1]
    e = Ebay_21(API_KEY, input)
    e.fetch()
    e.parse()