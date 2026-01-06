interface ImagePreviewProps {
  preview: string | null;
  alt?: string;
}

export const ImagePreview: React.FC<ImagePreviewProps> = ({ preview, alt = 'Uploaded image' }) => {
  if (!preview) {
    return (
      <div className="image-preview empty">
        <span style={{ fontSize: '4rem' }}>🖼️</span>
        <span>No image selected</span>
        <span style={{ fontSize: '0.875rem', opacity: 0.6 }}>Upload an image to get started</span>
      </div>
    );
  }

  return (
    <div className="image-preview">
      <img src={preview} alt={alt} />
    </div>
  );
};
