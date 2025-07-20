import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    axios.get('/api/reviews')
      .then(res => {
        setReviews(res.data);
      })
      .catch(err => {
        console.error("Error fetching reviews:", err);
      });
  }, []);

  return (
    <div className="app-container">
      <header>
        <h1>🔍 Code Review Analytics</h1>
        <p className="subtitle">Insights from your submitted code</p>
      </header>

      <div className="reviews-container">
        {reviews.length === 0 ? (
          <p>No reviews yet.</p>
        ) : (
          reviews.map((review, idx) => (
            <div className="review-card" key={idx}>
              <h2>{review.filename}</h2>
              {review.issues && review.issues.length > 0 ? (
                <ul>
                  {review.issues.map((issue, index) => (
                    <li key={index}>{issue.issue}</li> // ✅ FIXED HERE
                  ))}
                </ul>
              ) : (
                <p className="no-issues">✅ No issues found!</p>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
