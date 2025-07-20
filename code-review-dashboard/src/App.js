import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch("/api/reviews")
      .then((res) => res.json())
      .then((data) => setReviews(data))
      .catch((err) => console.error("Error fetching reviews:", err));
  }, []);

  // Find max issues for scaling bars
  const maxIssues = Math.max(...reviews.map((r) => r.issues), 1);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 Code Review Analytics</h1>
      </header>

      <main className="review-list">
        {reviews.map((review, index) => (
          <div key={index} className="review-card">
            <h3>{review.filename}</h3>
            <div className="issue-bar-container">
              <div
                className="issue-bar"
                style={{ width: `${(review.issues / maxIssues) * 100}%` }}
              ></div>
              <span className="issue-count">🛠 {review.issues} issues</span>
            </div>
          </div>
        ))}
      </main>
    </div>
  );
}

export default App;
