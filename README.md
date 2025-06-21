# Event Search Application

A full-stack event search application with a Django backend, MongoDB database, and React frontend. This app enables users to search log events using various filters such as source/destination addresses, action type, log status, and time ranges.

## Features

- Search log events by:
  - Source/Destination IP address
  - Action (e.g., `REJECT`, `ACCEPT`)
  - Log status (e.g., `OK`, `ERROR`)
- Filter results by time range using epoch timestamps
- View detailed event information
- Fast search performance powered by MongoDB indexing
- Responsive UI with intuitive query examples
- Detailed API documentation

## Prerequisites

Before getting started, ensure you have the following installed:

- Python 3.10+
- Node.js 18+
- MongoDB (local or remote)
- Basic terminal/command line knowledge

## Installation

### 1. Clone the Repository

git clone https://github.com/vishvesh1/event-search-app.git 
cd event-search-app

### 2. Configure Environment Variables

Create the following environment files:

#### backend/.env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=logsearch
DEBUG=True

> Replace mongodb://localhost:27017/ with your MongoDB connection string if using a remote instance.

## Run the Application

### Backend Setup

1. Install dependencies:
cd backend
pip install -r requirements.txt

2. Start the Django development server:
python manage.py runserver

The backend will be available at: http://localhost:8000

3. Import sample data:
python import_data.py

### Frontend Setup

1. Install dependencies:
cd frontend
npm install

2. Start the React development server:
npm run dev

The frontend will be available at: http://localhost:5173

## Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/search

## Project Structure

event-search-app/
├── backend/          # Django backend
│   ├── data/         # Log files
│   ├── logsearch/    # Django project
│   ├── search/       # Django app
│   ├── .env          # Environment variables
│   ├── requirements.txt
│   ├── manage.py
│   └── import_data.py
├── frontend/         # React frontend
│   ├── public/
│   ├── src/
│   ├── .env          # Environment variables
│   ├── package.json
│   └── ...
└── README.md

## API Documentation

### Search Endpoint

POST /api/search

Request Body:
{
  "query": "REJECT",
  "start": 1725812977,
  "end": 1725820193
}

Parameters:

| Parameter | Description |
|----------|-------------|
| `query`  | Search term (e.g., `"REJECT"`, `"srcaddr=192.168.1.1"`) |
| `start`  | Start time in epoch seconds |
| `end`    | End time in epoch seconds |

Response Example:
{
  "results": [
    {
      "srcaddr": "55.219.212.124",
      "dstaddr": "253.78.203.167",
      "starttime": 1725845058,
      "endtime": 1725851695,
      "action": "REJECT",
      "log_status": "OK",
      "file": "data.log"
    }
  ],
  "search_time": 0.04
}

## Usage Instructions

1. Open the app at: http://localhost:5173
2. Enter a search query using one of these formats:
   - action=REJECT
   - log_status=OK
   - srcaddr=92.23.242.42
   - dstaddr=204.98.197.54
3. Optionally specify a time range in epoch seconds
4. Click "Search" to view results
5. Results are displayed in cards with full details

## Query Examples

Try clicking on any of these sample queries:

- srcaddr=92.23.242.42
- action=REJECT
- log_status=OK
- dstaddr=204.98.197.54

## Troubleshooting

### Common Issues

MongoDB Connection Issues:
Ensure MongoDB is running locally or update the MONGO_URI in .env to point to your correct MongoDB instance.

Frontend Not Connecting to Backend:
Make sure both the frontend and backend servers are running and check the VITE_API_URL in frontend/.env.

Import Data Fails:
Run this inside the backend directory:
python import_data.py

Ensure MongoDB is running before importing.

## License

MIT License – see LICENSE for details.
