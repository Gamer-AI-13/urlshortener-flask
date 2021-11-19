import datetime
import pymongo

class urlall:
    
    def __init__(self, uri, database_name):
        self._client = pymongo.MongoClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users      
    def new_url(self, shurl, url, views):
        return dict(
            shurl = shurl,
            url = url,
            views = views,
            join_date = datetime.date.today().isoformat()
        )  
    def add_url(self, shurl, url):
         user = self.new_url(shurl, url, 0)
         self.col.insert_one(user)
    def is_surl_exist(self, shurl):
         user = self.col.find_one({'shurl': shurl})
         print(user)
         return True if user else False
    #async def total_users_count(self):
        #count = await self.col.count_documents({})
        #return count
    def get_info(self, shurl):
         user = self.col.find_one({'shurl': shurl})
         print (user)
         return user
    def delete_url(self, shurl):
         self.col.delete_one({'shurl': shurl})