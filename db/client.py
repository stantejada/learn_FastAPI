from pymongo import MongoClient

#base de dato local
#db_client = MongoClient().local

#base de dato remota
db_client = MongoClient(
    "mongodb+srv://stanleytejadaj:Tejada1994.@cluster0.8vgyv46.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").user_crud
