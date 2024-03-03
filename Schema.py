import pymongo
from pymongo import MongoClient
# Replace <your_cluster_uri> with your MongoDB Atlas cluster URI
client = MongoClient("mongodb+srv://akkuluri66:Mahesh%404444@cluster0.lrkegak.mongodb.net/Ecommers")
# Accessing the database
db = client.my_database

# Accessing collections
prompts_collection = db.prompts
tags_collection = db.tags
companies_collection = db.companies
llm_engines_collection = db.llm_engines
files_collection = db.files

# Inserting documents into collections
prompt_doc = {"prompt_text": "Your prompt text here", "tags": ["tag1", "tag2"], "id": "1"}
prompts_collection.insert_one(prompt_doc)

tag_doc = {"tag_name": "Tag1", "id": "1"}
tags_collection.insert_one(tag_doc)

# Querying documents
query = {"tag_name": "Tag1"}
result = tags_collection.find(query)
for doc in result:
    print(doc)

# Updating documents
query = {"tag_name": "Tag1"}
new_values = {"$set": {"tag_name": "New Tag Name"}}
tags_collection.update_one(query, new_values)

# Deleting documents
query = {"tag_name": "New Tag Name"}
tags_collection.delete_one(query)