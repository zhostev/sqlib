// components/ConfigEditor/ConfigForm.js
import React, { useState } from 'react';

const ConfigForm = ({ configData, onSave }) => {
  const [formData, setFormData] = useState(configData);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSave(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Iterate over formData keys and generate input fields */}
      {Object.keys(formData).map((key) => (
        <div key={key}>
          <label htmlFor={key}>{key}</label>
          <input
            type="text"
            id={key}
            name={key}
            value={formData[key]}
            onChange={handleChange}
          />
        </div>
      ))}
      <button type="submit">Save Configuration</button>
    </form>
  );
};

export default ConfigForm;