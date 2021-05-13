'''Python script to write the precomputed nearby pincode data to a MongoDB'''

import os
import json
from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_URI'])
# After the last '/' is the database name
db = client[os.environ['MONGO_URI'].rpartition('/')[2]]
collection = db['nearby_pincodes']

# Get the data in next format
with open('nearby_pincodes.json') as file:
    file_data = json.load(file)

# Data is expected in key:value pair, make every such entry as one document
for key, value in file_data.items():
    new_value = { 'key': int(key), 'value': value }
    collection.insert_one(new_value)

# Aids in faster operation when doing 'find' later on
collection.create_index('key')
