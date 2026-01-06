import { PredictionResult } from '../types';

interface PredictionTableProps {
  result: PredictionResult | null;
}

const getCategoryIcon = (category: string): string => {
  const icons: { [key: string]: string } = {
    'Tone': '💧',
    'Color': '🎨',
    'Blackhead': '🔍'
  };
  return icons[category] || '📊';
};

const getConfidenceClass = (confidence: number): string => {
  if (confidence >= 80) return 'confidence-high';
  if (confidence >= 60) return 'confidence-medium';
  return 'confidence-low';
};

export const PredictionTable: React.FC<PredictionTableProps> = ({ result }) => {
  if (!result) {
    return (
      <div className="prediction-table empty">
        <span style={{ fontSize: '4rem', marginBottom: '1rem' }}>📊</span>
        <span>No predictions yet</span>
        <span style={{ fontSize: '0.875rem', opacity: 0.6 }}>Results will appear here</span>
      </div>
    );
  }

  const rows = [
    { category: 'Tone', data: result.tone },
    { category: 'Color', data: result.color },
    { category: 'Blackhead', data: result.blackhead }
  ];

  return (
    <div className="prediction-table">
      <h3>Analysis Results</h3>
      {rows.map(({ category, data }) => {
        // Sort probabilities by value in descending order
        const sortedProbs = Object.entries(data.probs)
          .map(([label, prob]) => ({ label, prob: prob * 100 }))
          .sort((a, b) => b.prob - a.prob);

        return (
          <div key={category} className="category-section">
            <div className="category-header">
              <span className="category-icon">{getCategoryIcon(category)}</span>
              <span className="category-name">{category}</span>
              <span className="top-prediction">{data.top_class}</span>
            </div>
            <div className="probabilities-list">
              {sortedProbs.map(({ label, prob }) => (
                <div key={label} className="probability-item">
                  <div className="probability-label">
                    <span className={label === data.top_class ? 'label-highlight' : ''}>
                      {label}
                    </span>
                    <span className={`probability-value ${getConfidenceClass(prob)}`}>
                      {prob.toFixed(1)}%
                    </span>
                  </div>
                  <div className="probability-bar-container">
                    <div 
                      className={`probability-bar ${getConfidenceClass(prob)}`}
                      style={{ width: `${prob}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};
