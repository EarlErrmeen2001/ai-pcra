import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [reviews, setReviews] = useState([]);
  const [file, setFile] = useState(null);

  const fetchReviews = async () => {
    try {
      const res = await axios.get("/api/reviews");
      setReviews(res.data);
    } catch (err) {
      console.error("Error fetching reviews:", err);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async () => {
      const code = reader.result;
      const filename = file.name;

      try {
        await axios.post("/webhook", { filename, code });
        fetchReviews(); // Refresh results
      } catch (err) {
        console.error("Upload failed:", err);
      }
    };

    reader.readAsText(file);
  };

  return (
    <div className="app-container">
      <header>
        <h1>🔍 Code Review Analytics</h1>
        <p className="subtitle">Results from analyzed code submissions</p>
      </header>

      <div className="upload-section">
        <input type="file" accept=".py" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload & Analyze</button>
      </div>

      <div className="reviews-container">
        {reviews.length === 0 ? (
          <p>No reviews found.</p>
        ) : (
          reviews.map((review, index) => (
            <div key={index} className="review-card">
              <h2>{review.filename}</h2>
              {review.issues.length === 0 ? (
                <p className="no-issues">No issues found!</p>
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
          ))
        )}
      </div>
    </div>
  );
}

export default App;
