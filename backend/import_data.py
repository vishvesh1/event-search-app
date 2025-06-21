# import_data.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DB_NAME')]
collection = db['logs']

DATA_DIR = 'data'

for filename in os.listdir(DATA_DIR):
    if filename.endswith('.log'):
        with open(os.path.join(DATA_DIR, filename), 'r') as f:
            for line in f:
                event = line.strip().split()
                if len(event) < 15:
                    continue
                
                collection.insert_one({
                    'srcaddr': event[4],
                    'dstaddr': event[5],
                    'starttime': int(event[11]),
                    'endtime': int(event[12]),
                    'action': event[13],
                    'log_status': event[14],
                    'file': filename
                })