// components/DataManagement/DataStatus.js
import React from 'react';

const DataStatus = ({ status }) => {
  return (
    <div className="data-status">
      <p>Current Data Status: <strong>{status}</strong></p>

      {/* Optionally, you can add more details about the data status here */}

      <style jsx>{`
        .data-status {
          margin-bottom: 20px;
          padding: 10px;
          background-color: #f3f3f3;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
};

export default DataStatus;