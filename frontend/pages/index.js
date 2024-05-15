import React from 'react';
import DataLoader from '../components/DataLoader';
import ModelTrain from '../components/ModelTrain';
import ModelInference from '../components/ModelInference';
import Evaluation from '../components/Evaluation';

const Home = () => (
  <div>
    <DataLoader />
    <ModelTrain />
    <ModelInference />
    <Evaluation />
  </div>
);

export default Home;