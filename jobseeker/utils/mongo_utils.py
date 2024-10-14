from mongoengine import connect

def connect_mongodb():
    db_host = "mongodb+srv://nikhithtest:test_1234@nikimongo.913qf.mongodb.net/sample_mflix"
    db_name = "sample_mflix"
    db_alias = "sample_mflix"
    kwargs = {}
    connect(db=db_name, host=db_host, alias=db_alias, **kwargs)
    print("DB connected")