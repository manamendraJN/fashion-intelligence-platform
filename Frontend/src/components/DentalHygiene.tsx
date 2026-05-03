import { useState } from 'react';
import './DentalHygiene.css';
import { analyzeDental } from '../api';

export const DentalHygiene = () => {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [prompt, setPrompt] = useState(
    "Analyze the teeth and gums in this photo for plaque, tartar, staining, gum inflammation, alignment concerns, and enamel wear. Provide a concise summary and 3-5 specific hygiene recommendations."
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
      setError('Please upload a clear teeth photo');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const resp = await analyzeDental(image, prompt);
      setResult(resp.recommendation);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to analyze dental hygiene');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="care-page">
      <header className="care-header">
        <h1>🦷 Dental Hygiene Analysis</h1>
        <p className="care-subtitle">Upload a mouth/teeth photo to get AI-powered hygiene insights and tips.</p>
      </header>

      <div className="hair-container">
        <div className="hair-upload-section">
          <div className="upload-card">
            <input type="file" accept="image/*" id="dental-upload" className="file-input" onChange={onChange} />
            <label htmlFor="dental-upload" className="upload-label">
              {preview ? (
                <img src={preview} alt="Dental preview" className="preview-image" />
              ) : (
                <>
                  <div className="upload-icon">📷</div>
                  <div className="upload-text">Click to upload dental photo</div>
                  <div className="upload-hint">JPG, PNG, or WEBP</div>
                </>
              )}
            </label>
          </div>

          <div className="prompt-section">
            <label htmlFor="dental-prompt" className="prompt-label">Custom Prompt (Optional)</label>
            <textarea id="dental-prompt" className="prompt-textarea" rows={4} value={prompt} onChange={(e) => setPrompt(e.target.value)} />
          </div>

          <button className="generate-button" onClick={onAnalyze} disabled={!image || loading}>
            {loading ? '🔎 Analyzing...' : '🔎 Analyze Dental Hygiene'}
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
              <p>Upload a clear photo of your teeth and click analyze.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
