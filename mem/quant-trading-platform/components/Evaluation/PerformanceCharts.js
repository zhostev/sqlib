// components/Evaluation/PerformanceCharts.js
import React from 'react';
import ReactECharts from 'echarts-for-react'; // Make sure to install echarts and echarts-for-react

const PerformanceCharts = ({ data }) => {
  // This is a placeholder for chart options
  const getChartOptions = (data) => {
    return {
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: data.map(d => d.x)
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: data.map(d => d.y),
          type: 'line'
        }
      ]
    };
  };

  return (
    <div className="performance-charts">
      <ReactECharts option={getChartOptions(data)} />

      {/* Optionally, you can add more charts or customize the existing one further here */}

      <style jsx>{`
        .performance-charts {
          margin-bottom: 20px;
        }
      `}</style>
    </div>
  );
};

export default PerformanceCharts;