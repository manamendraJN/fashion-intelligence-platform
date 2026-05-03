import { useState } from 'react';
import './NailCare.css';
import { analyzeNails } from '../api';

export const NailCare = () => {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [prompt, setPrompt] = useState(
    "Analyze these nails for cleanliness, nail health, cuticle condition, discoloration, ridges, or damage. Provide a short summary and 3-5 actionable care recommendations."
  );

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) {
      setImage(f);
      setPreview(URL.createObjectURL(f));
      setError(null);
      setResult(null);
    }
  };

  const onAnalyze = async () => {
    if (!image) {
      setError('Please upload a clear nail photo');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const resp = await analyzeNails(image, prompt);
      setResult(resp.recommendation);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to analyze nails');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="care-page">
      <header className="care-header">
        <h1>💅 Nail Care Analysis</h1>
        <p className="care-subtitle">Upload a photo of your nails to get AI-powered analysis and tips.</p>
      </header>

      <div className="hair-container">
        <div className="hair-upload-section">
          <div className="upload-card">
            <input type="file" accept="image/*" id="nail-upload" className="file-input" onChange={onChange} />
            <label htmlFor="nail-upload" className="upload-label">
              {preview ? (
                <img src={preview} alt="Nail preview" className="preview-image" />
              ) : (
                <>
                  <div className="upload-icon">📷</div>
                  <div className="upload-text">Click to upload nail photo</div>
                  <div className="upload-hint">JPG, PNG, or WEBP</div>
                </>
              )}
            </label>
          </div>

          <div className="prompt-section">
            <label htmlFor="nail-prompt" className="prompt-label">Custom Prompt (Optional)</label>
            <textarea id="nail-prompt" className="prompt-textarea" rows={4} value={prompt} onChange={(e) => setPrompt(e.target.value)} />
          </div>

          <button className="generate-button" onClick={onAnalyze} disabled={!image || loading}>
            {loading ? '🔎 Analyzing...' : '🔎 Analyze Nails'}
          </button>

          {error && <div className="error-message">❌ {error}</div>}
        </div>

        <div className="hair-result-section">
          {result ? (
            <div className="recommendation-card">
              <h2>📝 Analysis & Recommendations</h2>
              <div className="recommendation-content">
                {result.split('\n').map((line, i) => (line.trim() ? <p key={i}>{line}</p> : <br key={i} />))}
              </div>
            </div>
          ) : (
            <div className="placeholder-card">
              <div className="placeholder-icon">🤖</div>
              <p>Upload a clear photo of your nails and click analyze.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
