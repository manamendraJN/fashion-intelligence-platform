import React from 'react';
import { Upload, X } from 'lucide-react';

const ImageUpload = ({ label, image, preview, onChange, onRemove }) => {
  const inputId = `upload-${label.toLowerCase().replace(' ', '-')}`;

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        {label}
      </label>
      
      <div className="relative border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-indigo-400 hover:bg-indigo-50/30 transition-all bg-white">
        {preview ? (
          <div className="relative">
            <img 
              src={preview} 
              alt={`${label} preview`} 
              className="max-h-64 mx-auto rounded-lg border border-gray-200"
            />
            <button
              type="button"
              onClick={onRemove}
              className="absolute -top-2 -right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors shadow-sm"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <>
            <div className="mb-3 inline-flex items-center justify-center w-16 h-16 rounded-full bg-indigo-100">
              <Upload className="w-8 h-8 text-indigo-600" />
            </div>
            <p className="text-sm text-gray-600 mb-1 font-medium">Click to upload or drag and drop</p>
            <p className="text-xs text-gray-500">PNG, JPG up to 10MB</p>
          </>
        )}
        
        <input
          type="file"
          accept="image/*"
          onChange={onChange}
          className="hidden"
          id={inputId}
        />
        
        {!preview && (
          <label
            htmlFor={inputId}
            className="mt-4 cursor-pointer bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors inline-block font-medium text-sm shadow-sm"
          >
            Choose File
          </label>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;