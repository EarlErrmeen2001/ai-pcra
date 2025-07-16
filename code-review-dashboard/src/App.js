import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState('');

  const baseURL =
    process.env.NODE_ENV === 'development'
      ? 'http://localhost:8000'
      : 'https://ai-pcra.onrender.com';

  useEffect(() => {
    axios.get(`${baseURL}/api/reviews`)
      .then((response) => {
        setReviews(response.data);
      })
      .catch((err) => {
        setError('Failed to load reviews');
        console.error(err);
      });
  }, []);

  return (
    <div>
      <h1>AI Code Review Dashboard</h1>
      {error && <p>{error}</p>}
      {reviews.map((review, index) => (
        <div key={index}>
          <h3>{review.filename}</h3>
          <pre>{review.code}</pre>
          <ul>
            {review.issues.map((issue, i) => (
              <li key={i}>Line {issue.line}: {issue.issue}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default App;
