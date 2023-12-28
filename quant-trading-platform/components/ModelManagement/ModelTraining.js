// components/ModelManagement/ModelTraining.js
import React from 'react';
import { Button } from 'element-react';

const ModelTraining = ({ onTrain }) => {
  return (
    <div className="model-training">
      <Button type="success" onClick={onTrain}>Start Model Training</Button>

      {/* Optionally, you can add more controls or information related to the model training here */}

      <style jsx>{`
        .model-training {
          margin-bottom: 20px;
        }
      `}</style>
    </div>
  );
};

export default ModelTraining;