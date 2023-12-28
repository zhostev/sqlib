// components/ConfigEditor/ConfigEditor.js
import React, { useState, useEffect } from 'react';
import { fetchConfig, saveConfig } from '../../utils/api';
import ConfigForm from './ConfigForm';

const ConfigEditor = () => {
  const [configData, setConfigData] = useState(null);

  useEffect(() => {
    const loadConfig = async () => {
      try {
        const data = await fetchConfig();
        setConfigData(data);
      } catch (error) {
        console.error('Error loading config:', error);
        // Handle error appropriately
      }
    };

    loadConfig();
  }, []);

  const handleSave = async (updatedConfig) => {
    try {
      await saveConfig(updatedConfig);
      alert('Config saved successfully!');
    } catch (error) {
      console.error('Error saving config:', error);
      // Handle error appropriately
    }
  };

  return (
    <div>
      {configData ? (
        <ConfigForm configData={configData} onSave={handleSave} />
      ) : (
        <p>Loading configuration...</p>
      )}
    </div>
  );
};

export default ConfigEditor;