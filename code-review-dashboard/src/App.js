// 🚀 AI-PCRA TEAM 👨‍💻👩‍💻🧠💻
// ===================================
// 🔬 AI-Powered Code Review Assistant
// 🧑‍💻 Lead Dev: Alameen Idris Muhammad
// 👥 Team: Collaborating to catch bugs 🐛,
//          review code intelligently 🐍,
//          and deliver with confidence 🎯
// -----------------------------------
// 💻 React Frontend + FastAPI Backend
// 📦 Hosted on Render
// 🌍 Smart UI for smarter reviews!

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [reviews, setReviews] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const fetchReviews = async () => {
    try {
      const response = await axios.get('/api/reviews');
      setReviews(response.data);
    } catch (err) {
      console.error('Error fetching reviews:', err);
      setError('Failed to load reviews.');
    }
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setError('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a Python file to upload.');
      return;
    }

    if (!selectedFile.name.endsWith('.py')) {
      setError('Only .py files are allowed.');
      return;
    }

    const reader = new FileReader();
    reader.onload = async () => {
      const code = reader.result;
      try {
        setUploading(true);
        await axios.post('/webhook', {
          filename: selectedFile.name,
          code,
        });
        setSelectedFile(null);
        fetchReviews(); // refresh list
      } catch (err) {
        console.error('Upload error:', err);
        setError('Upload failed. Try again.');
      } finally {
        setUploading(false);
      }
    };
    reader.readAsText(selectedFile);
  };

  return (
    <div className="app-container">
      <header>
        <h1>🔍 Capital City University AI Powered Code Review Assistant</h1>
        <p className="subtitle">Results from analyzed code submissions</p>
      </header>

      <div className="upload-section">
        <input type="file" accept=".py" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={uploading}>
          {uploading ? 'Uploading...' : 'Upload and Analyze'}
        </button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>

      <div className="reviews-container">
        {reviews.length === 0 && <p>No reviews found yet.</p>}
        {reviews.map((review, idx) => (
          <div key={idx} className="review-card">
            <h2>{review.filename}</h2>
            {review.issues.length === 0 ? (
              <p className="no-issues">✅ No issues found</p>
            ) : (
              <ul>
                {review.issues.map((issue, i) => (
                  <li key={i}>
                    Line {issue.line}: {issue.issue}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
