import { useState } from 'react';
import { generateHairStyle } from '../api';
import './HairGeneration.css';

interface HairGenerationState {
  image: File | null;
  preview: string | null;
  loading: boolean;
  error: string | null;
  recommendation: string | null;
  prompt: string;
}

export const HairGeneration = () => {
  const [state, setState] = useState<HairGenerationState>({
    image: null,
    preview: null,
    loading: false,
    error: null,
    recommendation: null,
    prompt: 'Analyze this person\'s face shape, skin tone, and features. Suggest professional hairstyles that would suit them best, considering modern trends and face framing techniques.'
  });

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setState(prev => ({
        ...prev,
        image: file,
        preview: URL.createObjectURL(file),
        error: null,
        recommendation: null
      }));
    }
  };

  const handleGenerate = async () => {
    if (!state.image) {
      setState(prev => ({ ...prev, error: 'Please select an image first' }));
      return;
    }

    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const result = await generateHairStyle(state.image, state.prompt);
      setState(prev => ({
        ...prev,
        recommendation: result.recommendation,
        loading: false
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to generate hair recommendations',
        loading: false
      }));
    }
  };

  return (
    <div className="hair-generation">
      <div className="hair-header">
        <h1>💇 AI Hair Style Generator</h1>
        <p className="hair-subtitle">Get personalized hairstyle recommendations powered by Gemini AI</p>
      </div>

      <div className="hair-container">
        <div className="hair-upload-section">
          <div className="upload-card">
            <input
              type="file"
              id="hair-upload"
              accept="image/*"
              onChange={handleImageChange}
              className="file-input"
            />
            <label htmlFor="hair-upload" className="upload-label">
              {state.preview ? (
                <img src={state.preview} alt="Preview" className="preview-image" />
              ) : (
                <>
                  <div className="upload-icon">📷</div>
                  <div className="upload-text">Click to upload photo</div>
                  <div className="upload-hint">JPG, PNG, or WEBP</div>
                </>
              )}
            </label>
          </div>

          <div className="prompt-section">
            <label htmlFor="prompt" className="prompt-label">
              Custom Prompt (Optional)
            </label>
            <textarea
              id="prompt"
              value={state.prompt}
              onChange={(e) => setState(prev => ({ ...prev, prompt: e.target.value }))}
              className="prompt-textarea"
              rows={4}
              placeholder="Describe what kind of hairstyle recommendations you want..."
            />
          </div>

          <button
            onClick={handleGenerate}
            disabled={!state.image || state.loading}
            className="generate-button"
          >
            {state.loading ? '✨ Generating...' : '✨ Generate Recommendations'}
          </button>

          {state.error && (
            <div className="error-message">❌ {state.error}</div>
          )}
        </div>

        <div className="hair-result-section">
          {state.recommendation && (
            <div className="recommendation-card">
              <h2>🎨 AI Recommendations</h2>
              <div className="recommendation-content">
                {state.recommendation.split('\n').map((line, index) => (
                  line.trim() ? <p key={index}>{line}</p> : <br key={index} />
                ))}
              </div>
            </div>
          )}

          {!state.recommendation && !state.loading && (
            <div className="placeholder-card">
              <div className="placeholder-icon">🤖</div>
              <p>Upload a photo and click generate to get AI-powered hairstyle recommendations</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
