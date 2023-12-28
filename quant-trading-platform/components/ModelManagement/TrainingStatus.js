// components/ModelManagement/TrainingStatus.js
import React from 'react';

const TrainingStatus = ({ status }) => {
  return (
    <div className="training-status">
      <p>Training Status: <strong>{status}</strong></p>

      {/* Optionally, you can add more details or visual indicators of training status here */}

      <style jsx>{`
        .training-status {
          margin-bottom: 20px;
          padding: 10px;
          background-color: #f3f3f3;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
};

export default TrainingStatus;