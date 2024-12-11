from pymongo import MongoClient
uri = "mongodb+srv://get_experts:getexperts214@pranabcluster.amvf9fu.mongodb.net/?retryWrites=true&w=majority&appName=PranabCluster"


client = MongoClient(uri)


db_experts = client['experts_db']
collection = db_experts['experts']



