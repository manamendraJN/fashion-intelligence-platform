import React from 'react';
import { Ruler } from 'lucide-react';

const MeasurementsDisplay = ({ measurements }) => {
  if (!measurements) return null;

  const measurementEntries = Object.entries(measurements);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
      <div className="flex items-center gap-3 mb-6">
        <div className="bg-blue-600 p-2.5 rounded-lg">
          <Ruler className="w-5 h-5 text-white" />
        </div>
        <h2 className="text-xl font-semibold text-gray-900">
          Body Measurements
        </h2>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {measurementEntries.map(([key, data]) => (
          <div 
            key={key} 
            className=" from-blue-50 to-indigo-50 p-4 rounded-lg border border-blue-100 hover:border-blue-200 hover:shadow-sm transition-all"
          >
            <p className="text-xs text-gray-600 uppercase tracking-wide font-medium mb-1.5">
              {key.replace(/-/g, ' ')}
            </p>
            <p className="text-2xl font-bold text-blue-700">
              {data.display || `${data.value?.toFixed(1)} cm`}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MeasurementsDisplay;