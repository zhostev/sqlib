// components/DataManagement/DataInitiator.js
import React from 'react';
import { Button } from 'element-react';

const DataInitiator = ({ onStart }) => {
  return (
    <div className="data-initiator">
      <Button type="primary" onClick={onStart}>Initiate Data Process</Button>

      {/* Optionally, you can add more information or controls related to the data initiation process here */}

      <style jsx>{`
        .data-initiator {
          margin-bottom: 20px;
        }
      `}</style>
    </div>
  );
};

export default DataInitiator;