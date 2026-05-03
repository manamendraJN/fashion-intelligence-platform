import { ChangeEvent } from 'react';

interface UploadCardProps {
  onImageSelect: (file: File) => void;
  loading: boolean;
}

export const UploadCard: React.FC<UploadCardProps> = ({ onImageSelect, loading }) => {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageSelect(file);
    }
  };

  return (
    <div className="upload-card">
      <h2>📸 Upload Your Image</h2>
      <div className="photo-guidelines">
        <h3>📋 Photo Guidelines</h3>
        <ul>
          <li>💡 Take photos in natural light</li>
          <li>🌟 Avoid strong shadows or overexposure</li>
          <li>🎨 Use a consistent background</li>
        </ul>
      </div>
      <input
        type="file"
        accept="image/*"
        onChange={handleChange}
        disabled={loading}
        id="file-upload"
      />
      <label htmlFor="file-upload" className="upload-label">
        {loading ? (
          <>⏳ Processing...</>
        ) : (
          <>📁 Choose Image</>
        )}
      </label>
      {loading && (
        <div className="loading-text">
          <div className="spinner"></div>
          Analyzing your image...
        </div>
      )}
    </div>
  );
};
