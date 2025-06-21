import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for React dev server

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@app.route('/api/search', methods=['POST'])
def search():
    start_time = time.time()
    data = request.json
    
    # Validate input
    if not all(k in data for k in ('query', 'start', 'end')):
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        query = data['query']
        start_epoch = int(data['start'])
        end_epoch = int(data['end'])
        results = []
        
        // Process all log files
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.log'):
                with open(os.path.join(DATA_DIR, filename), 'r') as f:
                    for line in f:
                        event = line.strip().split()
                        if len(event) < 15:
                            continue
                        
                        # Extract event fields
                        event_data = {
                            'srcaddr': event[4],
                            'dstaddr': event[5],
                            'starttime': int(event[11]),
                            'endtime': int(event[12]),
                            'action': event[13],
                            'log_status': event[14]
                        }
                        
                        # Check time range
                        if not (event_data['endtime'] >= start_epoch and 
                                event_data['starttime'] <= end_epoch):
                            continue
                        
                        # Process query
                        if '=' in query:
                            field, value = query.split('=', 1)
                            if field in event_data and event_data[field] == value:
                                results.append({
                                    'event': event_data,
                                    'file': filename
                                })
                        else:
                            if query == event_data['srcaddr'] or query == event_data['dstaddr']:
                                results.append({
                                    'event': event_data,
                                    'file': filename
                                })
        
        search_time = round(time.time() - start_time, 2)
        return jsonify({
            'results': results,
            'search_time': search_time
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(threaded=True, port=5000)