import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      console.log(`Searching for: ${searchTerm}`);
      const response = await axios.get(`http://127.0.0.1:8000/api/search/${encodeURIComponent(searchTerm)}`);
      console.log('Response:', response.data);
      setResults(response.data.results);
    } catch (err) {
      console.error('Error details:', err);
      console.error('Error response:', err.response?.data);
      setError('Error searching for books. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sunshine Shelves</h1>
        <form onSubmit={handleSearch}>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search for a book..."
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>
      </header>

      <main>
        {error && <div className="error">{error}</div>}
        
        {results.length > 0 && (
          <div className="results">
            {results.map((result) => (
              <div key={result.library} className="library-result">
                <h2>{result.library.toUpperCase()}</h2>
                <p>Available Copies: {result.availableCopies}</p>
                <p>Total Copies: {result.ownedCopies}</p>
                <p>Estimated Wait: {result.estimatedWaitDays} days</p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 