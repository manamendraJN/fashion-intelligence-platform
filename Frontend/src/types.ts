export interface ClassPrediction {
  top_class: string;
  probs: { [key: string]: number };
}

export interface PredictionResult {
  tone: ClassPrediction;
  color: ClassPrediction;
  blackhead: ClassPrediction;
}

export interface UploadState {
  image: File | null;
  preview: string | null;
  loading: boolean;
  error: string | null;
  result: PredictionResult | null;
}
