// pages/data.js
import { useState, useEffect } from 'react';
import Head from 'next/head';
import axios from 'axios';
import { Button } from 'element-react';

export default function DataPage() {
  const [dataStatus, setDataStatus] = useState('Idle'); // Idle, Processing, Completed, Error
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // 获取数据初始化的历史记录
    const fetchDataHistory = async () => {
      try {
        const response = await axios.get('/api/data/history');
        setHistory(response.data);
      } catch (error) {
        console.error('Failed to fetch data history:', error);
      }
    };

    fetchDataHistory();
  }, []);

  const initiateDataProcess = async () => {
    setDataStatus('Processing');
    try {
      const response = await axios.post('/api/data/initiate');
      setDataStatus('Completed');
      // 更新历史记录
      setHistory(prevHistory => [...prevHistory, response.data]);
    } catch (error) {
      console.error('Failed to initiate data process:', error);
      setDataStatus('Error');
    }
  };

  return (
    <div>
      <Head>
        <title>Data Management</title>
      </Head>

      <main>
        <h1>Data Management</h1>
        <div>
          <Button type="primary" onClick={initiateDataProcess} disabled={dataStatus === 'Processing'}>
            {dataStatus === 'Processing' ? 'Processing...' : 'Initiate Data Process'}
          </Button>
        </div>
        <div>
          <h2>Current Status: {dataStatus}</h2>
        </div>
        <div>
          <h2>History</h2>
          <ul>
            {history.map((entry, index) => (
              <li key={index}>{entry}</li> // 假设历史记录条目是字符串
            ))}
          </ul>
        </div>
      </main>

      <style jsx>{`
        main {
          padding: 1rem;
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
}