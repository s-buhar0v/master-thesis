import pymongo

client = pymongo.MongoClient("")
db = client['social-networks']
collection = db.posts


print(collection)

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
}

post_id = collection.insert_one(post).inserted_id

print(post_id)