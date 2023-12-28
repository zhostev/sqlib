// pages/evaluation.js
import { useState, useEffect } from 'react';
import Head from 'next/head';
import axios from 'axios';
import EvaluationResults from '../components/Evaluation/EvaluationResults';
import PerformanceCharts from '../components/Evaluation/PerformanceCharts';

export default function EvaluationPage() {
  const [evaluationResults, setEvaluationResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 获取评估结果
    const fetchEvaluationResults = async () => {
      setLoading(true);
      try {
        const response = await axios.get('/api/evaluation/results');
        setEvaluationResults(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch evaluation results:', error);
        setLoading(false);
      }
    };

    fetchEvaluationResults();
  }, []);

  return (
    <div>
      <Head>
        <title>Evaluation Results</title>
      </Head>

      <main>
        <h1>Evaluation Results</h1>
        {loading ? (
          <p>Loading evaluation results...</p>
        ) : (
          <div>
            <EvaluationResults results={evaluationResults} />
            <PerformanceCharts data={evaluationResults} />
          </div>
        )}
      </main>

      <style jsx>{`
        main {
          padding: 1rem;
        }
      `}</style>
    </div>
  );
}