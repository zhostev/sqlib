// pages/models.js
import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import axios from 'axios';
import ModelTraining from '../components/ModelManagement/ModelTraining';
import TrainingStatus from '../components/ModelManagement/TrainingStatus';

export default function ModelsPage() {
  const [trainingStatus, setTrainingStatus] = useState('Idle'); // Idle, Training, Completed, Error

  useEffect(() => {
    // 你可以在这里添加代码来获取模型的初始训练状态
    const fetchTrainingStatus = async () => {
      try {
        const response = await axios.get('/api/model/status');
        setTrainingStatus(response.data.status);
      } catch (error) {
        console.error('Failed to fetch training status:', error);
        setTrainingStatus('Error');
      }
    };

    fetchTrainingStatus();
  }, []);

  const handleTrainModel = async () => {
    setTrainingStatus('Training');
    try {
      await axios.post('/api/model/train');
      setTrainingStatus('Completed');
    } catch (error) {
      console.error('Failed to start model training:', error);
      setTrainingStatus('Error');
    }
  };

  return (
    <div>
      <Head>
        <title>Model Management</title>
      </Head>

      <main>
        <h1>Model Management</h1>
        <ModelTraining onTrain={handleTrainModel} />
        <TrainingStatus status={trainingStatus} />
      </main>

      <style jsx>{`
        main {
          padding: 1rem;
        }
      `}</style>
    </div>
  );
}