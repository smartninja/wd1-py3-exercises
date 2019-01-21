import os


def get_mongo_db(url=None):
    # url should be in this form: "mongodb://<username>:<password>@<host_server>.mlab.com:<port>/<db_name>"
    heroku = os.environ.get("DYNO")
    azure = os.environ.get("APPSETTING_WEBSITE_SITE_NAME")
    gae = os.environ.get("GAE_APPLICATION")

    if heroku or azure or gae:  # heroku, azure or gae
        if heroku and not url:
            url = os.environ.get("MONGODB_URI")
        elif azure and not url:
            url = os.environ.get("APPSETTING_MONGOURL")

        from pymongo import MongoClient
        client = MongoClient(url)
        db_name = url.replace("mongodb://").split("/")[1]
        return client[db_name]
    else:  # localhost
        from tinymongo import TinyMongoClient
        client = TinyMongoClient("database")
        return client.my_db
