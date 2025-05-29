import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';

function App() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/reviews')
      .then(res => setReviews(res.data));
  }, []);

  return (
    <div>
      <h1>Code Review Analytics</h1>
      <Bar data={{
        labels: reviews.map(r => r.file),
        datasets: [{
          label: 'Issues Found',
          data: reviews.map(r => r.issues_count)
        }]
      }} />
    </div>
  );
}

export default App;
