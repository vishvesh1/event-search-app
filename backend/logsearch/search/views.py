import time
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import logging
import json

# Configure logging
logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'logsearch')

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['logs']
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {str(e)}")
    collection = None

@csrf_exempt
def search(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

    try:
        start_time = time.time()
        
        # --- MODIFICATION START ---
        # Dynamically build a list of filters based on provided data.
        filters = []

        # 1. Handle the 'query' parameter
        query_str = data.get('query', '').strip()
        if query_str:
            if '=' in query_str:
                field, value = query_str.split('=', 1)
                allowed_fields = {'srcaddr', 'dstaddr', 'action', 'log_status'}
                if field.strip() in allowed_fields:
                    filters.append({field.strip(): value.strip()})
                else:
                    return JsonResponse({'error': f'Invalid search field: {field}'}, status=400)
            else:
                # If no field is specified, search across multiple fields using a case-insensitive regex.
                search_filter = {
                    "$or": [
                        {"srcaddr": {"$regex": query_str, "$options": "i"}},
                        {"dstaddr": {"$regex": query_str, "$options": "i"}},
                        {"action": {"$regex": query_str, "$options": "i"}},
                    ]
                }
                filters.append(search_filter)

        # 2. Handle 'start' and 'end' time parameters
        start_epoch_str = data.get('start')
        end_epoch_str = data.get('end')
        
        time_filter = {}
        if start_epoch_str:
            # Logs that end at or after the start time
            time_filter.setdefault('endtime', {})['$gte'] = int(start_epoch_str)
        if end_epoch_str:
            # Logs that start at or before the end time
            time_filter.setdefault('starttime', {})['$lte'] = int(end_epoch_str)
        
        if time_filter:
            filters.append(time_filter)

        # 3. Check if any filters were created
        if not filters:
            return JsonResponse({'error': 'Please provide at least one search field (query or time range).'}, status=400)
        
        # 4. Combine all filters using $and
        mongo_query = {"$and": filters}
        
        # --- MODIFICATION END ---

        # Execute query
        if collection is None:
            raise Exception("Database connection not established")
        
        results = list(collection.find(mongo_query, {'_id': 0}).limit(1000))
        
        search_time = round(time.time() - start_time, 2)
        logger.info(f"Search completed in {search_time}s: {len(results)} results for query: {mongo_query}")
        
        return JsonResponse({
            'results': results,
            'search_time': search_time
        })

    except ValueError:
        logger.error("Invalid integer value for start/end time")
        return JsonResponse({'error': 'Start and end times must be valid integers'}, status=400)
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)