import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

// ✅ Register components before using them
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    axios.get('https://ai-pcra.onrender.com/api/reviews')  // ✅ Use full URL for production
      .then(res => setReviews(res.data))
      .catch(err => console.error(err));
  }, []);

  const chartData = {
    labels: reviews.map(r => r.file),
    datasets: [{
      label: 'Issues Found',
      data: reviews.map(r => r.issues_count),
      backgroundColor: 'rgba(75, 192, 192, 0.6)'
    }]
  };

  return (
    <div>
      <h1>Code Review Analytics</h1>
      <Bar data={chartData} />
    </div>
  );
}

export default App;
