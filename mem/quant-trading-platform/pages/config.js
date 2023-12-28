// pages/config.js
import { useState, useEffect } from 'react';
import Head from 'next/head';
import ConfigForm from '../components/ConfigEditor/ConfigForm';
import axios from 'axios';

export default function ConfigPage() {
  const [configData, setConfigData] = useState(null);
  const [schema, setSchema] = useState(null);

  useEffect(() => {
    // 加载配置的 JSON Schema
    const fetchSchema = async () => {
      try {
        const response = await axios.get('/api/schema/config');
        setSchema(response.data);
      } catch (error) {
        console.error('Failed to fetch config schema:', error);
      }
    };

    // 加载当前配置
    const fetchConfig = async () => {
      try {
        const response = await axios.get('/api/config');
        setConfigData(response.data);
      } catch (error) {
        console.error('Failed to fetch config:', error);
      }
    };

    fetchSchema();
    fetchConfig();
  }, []);

  const handleSave = async (updatedConfig) => {
    try {
      // 保存更新后的配置
      await axios.post('/api/config', updatedConfig);
      alert('Config saved successfully!');
    } catch (error) {
      console.error('Failed to save config:', error);
      alert('Failed to save config.');
    }
  };

  return (
    <div>
      <Head>
        <title>Configuration Management</title>
      </Head>

      <main>
        <h1>Configuration Management</h1>
        {schema && configData ? (
          <ConfigForm schema={schema} formData={configData} onSave={handleSave} />
        ) : (
          <p>Loading configuration...</p>
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