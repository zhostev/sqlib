// components/Evaluation/EvaluationResults.js
import React from 'react';

const EvaluationResults = ({ results }) => {
  return (
    <div className="evaluation-results">
      <h3>Evaluation Results</h3>
      {/* Render results as a list or table */}
      <ul>
        {results.map((result, index) => (
          <li key={index}>{result.metricName}: {result.value}</li>
        ))}
      </ul>

      {/* Optionally, you can add more sophisticated rendering of the results here */}

      <style jsx>{`
        .evaluation-results {
          margin-bottom: 20px;
        }
        ul {
          list-style-type: none;
          padding: 0;
        }
        li {
          margin-bottom: 0.5rem;
        }
      `}</style>
    </div>
  );
};

export default EvaluationResults;