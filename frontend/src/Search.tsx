/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

interface LogEvent {
  srcaddr: string;
  dstaddr: string;
  action: string;
  log_status: string;
  starttime: number;
  endtime: number;
  file: string;
}

const Search: React.FC = () => {
  const [query, setQuery] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [results, setResults] = useState<LogEvent[]>([]);
  const [searchTime, setSearchTime] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [queryExamples] = useState([
    'srcaddr=92.23.242.42',
    'action=REJECT',
    'log_status=OK',
    'dstaddr=204.98.197.54'
  ]);

  const handleSearch = async () => {
    if (!query.trim() && !start.trim() && !end.trim()) {
      setError('Please provide a search query or a time range.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResults([]);
    setSearchTime(null);

    try {
      const payload: { [key: string]: any } = {};
      if (query.trim()) payload.query = query.trim();
      if (start.trim()) payload.start = start.trim();
      if (end.trim()) payload.end = end.trim();

      const response = await axios.post<{
        results: LogEvent[];
        search_time: number;
      }>('http://localhost:8000/api/search', payload);

      setResults(response.data.results);
      setSearchTime(response.data.search_time);
    } catch (err: any) {
      console.error('Search error:', err);
      setError(err.response?.data?.error || 'Failed to fetch search results. Check server connection.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleClick = (example: string) => {
    setQuery(example);
  };

  const formatEpoch = (epoch: number) => {
    const date = new Date(epoch * 1000);
    return date.toLocaleString();
  };

  return (
    <main className="App">
      <h1 className="title">Event Search</h1>

      <div className="search-container">
        <form
          className="search-form"
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch();
          }}
        >
          <div className="form-group">
            <label htmlFor="query">Search Query:</label>
            <input
              id="query"
              type="text"
              placeholder="e.g., 92.23.242.42 or action=REJECT"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          
          <div className="time-range">
            <div className="form-group">
              <label htmlFor="start">Start Time (epoch):</label>
              <input
                id="start"
                type="number"
                value={start}
                onChange={(e) => setStart(e.target.value)}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="end">End Time (epoch):</label>
              <input
                id="end"
                type="number"
                value={end}
                onChange={(e) => setEnd(e.target.value)}
              />
            </div>
          </div>

          <button type="submit" disabled={isLoading}>
            {isLoading ? (
              <>
                <span className="spinner"></span> Searching...
              </>
            ) : (
              'Search'
            )}
          </button>
        </form>

        <div className="query-examples">
          <h3>Query Examples:</h3>
          <div className="example-buttons">
            {queryExamples.map((example, index) => (
              <button
                key={index}
                type="button"
                className="example-btn"
                onClick={() => handleExampleClick(example)}
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      </div>

      {error && <p className="error">{error}</p>}

      {searchTime !== null && (
        <div className="summary">
          Found <strong>{results.length}</strong> result(s) in <strong>{searchTime.toFixed(2)}s</strong>
        </div>
      )}

      <section className="results-grid">
        {results.map((result, index) => (
          <div key={index} className="event-card">
            <div className="event-header">
              <span className={`status-badge ${result.log_status === 'OK' ? 'success' : 'fail'}`}>
                {result.log_status}
              </span>
              <span className={`action-badge ${result.action === 'ACCEPT' ? 'accept' : 'reject'}`}>
                {result.action}
              </span>
            </div>
            
            <div className="event-details">
              {/* Source field */}
              <div className="detail-row">
                <span>Source:</span>
                <span className="src-addr">{result.srcaddr}</span>
              </div>
              
              {/* Destination field */}
              <div className="detail-row">
                <span>Destination:</span>
                <span className="dest-addr">{result.dstaddr}</span>
              </div>
              
              {/* Fixed: Action field */}
              <div className="detail-row">
                <span>Action:</span>
                <span>{result.action}</span>
              </div>
              
              {/* Fixed: Status field */}
              <div className="detail-row">
                <span>Status:</span>
                <span>{result.log_status}</span>
              </div>
              
              {/* Fixed: File field */}
              <div className="detail-row">
                <span>File:</span>
                <span>{result.file}</span>
              </div>
              
              {/* Fixed: Start time field */}
              <div className="detail-row">
                <span>Start:</span>
                <span>{formatEpoch(result.starttime)}</span>
              </div>
              
              {/* Fixed: End time field */}
              <div className="detail-row">
                <span>End:</span>
                <span>{formatEpoch(result.endtime)}</span>
              </div>
            </div>
          </div>
        ))}
        
        {results.length === 0 && searchTime !== null && !isLoading && (
          <div className="no-results">
            <p>No results found for your query.</p>
            <p>Try expanding your time range or using a different search term.</p>
          </div>
        )}
      </section>
    </main>
  );
};

export default Search;