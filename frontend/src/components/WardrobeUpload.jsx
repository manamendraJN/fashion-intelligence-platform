import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Loader2, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../lib/utils';

export function WardrobeUpload({ onUploadComplete }) {
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    setIsUploading(true);
    let currentProgress = 0;
    const interval = setInterval(() => {
      currentProgress += 5;
      setProgress(currentProgress);
      if (currentProgress >= 100) {
        clearInterval(interval);
        setIsUploading(false);
        setIsComplete(true);
        setTimeout(() => {
          onUploadComplete();
          setIsComplete(false);
          setProgress(0);
        }, 1000);
      }
    }, 100);
  }, [onUploadComplete]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpeg', '.jpg', '.png', '.webp'] },
    disabled: isUploading,
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={cn(
          'relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 cursor-pointer overflow-hidden',
          isDragActive
            ? 'border-[#8B5A5A] bg-[#8B5A5A]/5'
            : 'border-[#E5E0D8] hover:border-[#8B5A5A]/50 hover:bg-white',
          isUploading && 'pointer-events-none bg-white'
        )}
      >
        <input {...getInputProps()} />

        <AnimatePresence mode="wait">
          {isUploading ? (
            <motion.div
              key="uploading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-4"
            >
              <div className="relative w-16 h-16 mb-4">
                <svg className="w-full h-full transform -rotate-90">
                  <circle
                    cx="32"
                    cy="32"
                    r="28"
                    stroke="#E5E0D8"
                    strokeWidth="4"
                    fill="none"
                  />
                  <circle
                    cx="32"
                    cy="32"
                    r="28"
                    stroke="#8B5A5A"
                    strokeWidth="4"
                    fill="none"
                    strokeDasharray="175.93"
                    strokeDashoffset={175.93 - (175.93 * progress) / 100}
                    className="transition-all duration-100 ease-linear"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center text-xs font-medium text-[#8B5A5A]">
                  {progress}%
                </div>
              </div>
              <h3 className="font-serif text-xl text-[#2C2C2C] mb-1">
                Analyzing Wardrobe
              </h3>
              <p className="text-sm text-gray-500">
                Extracting features & learning patterns...
              </p>
            </motion.div>
          ) : isComplete ? (
            <motion.div
              key="complete"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex flex-col items-center justify-center py-4"
            >
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4 text-green-600">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <h3 className="font-serif text-xl text-[#2C2C2C] mb-1">
                Analysis Complete
              </h3>
              <p className="text-sm text-gray-500">
                Your wardrobe has been digitized.
              </p>
            </motion.div>
          ) : (
            <motion.div
              key="idle"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-4"
            >
              <div className="w-16 h-16 bg-[#FAF8F5] rounded-full flex items-center justify-center mb-4 text-[#8B5A5A]">
                <Upload className="w-8 h-8" />
              </div>
              <h3 className="font-serif text-xl text-[#2C2C2C] mb-2">
                {isDragActive ? 'Drop items here' : 'Upload your wardrobe'}
              </h3>
              <p className="text-sm text-gray-500 max-w-sm mx-auto mb-6">
                Drag and drop your clothing images here, or click to browse. Our
                AI will automatically categorize and analyze them.
              </p>
              <button className="px-6 py-2.5 bg-[#2C2C2C] text-white rounded-full text-sm font-medium hover:bg-black transition-colors shadow-lg shadow-gray-200">
                Select Files
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
        <div className="p-4 rounded-xl bg-white border border-[#E5E0D8]">
          <p className="text-xs font-semibold text-[#8B5A5A] uppercase tracking-wider mb-1">
            Phase 1
          </p>
          <p className="text-sm text-[#2C2C2C]">Visual Feature Extraction</p>
        </div>
        <div className="p-4 rounded-xl bg-white border border-[#E5E0D8]">
          <p className="text-xs font-semibold text-[#8B5A5A] uppercase tracking-wider mb-1">
            Phase 2
          </p>
          <p className="text-sm text-[#2C2C2C]">Event Suitability Scoring</p>
        </div>
        <div className="p-4 rounded-xl bg-white border border-[#E5E0D8]">
          <p className="text-xs font-semibold text-[#8B5A5A] uppercase tracking-wider mb-1">
            Phase 3
          </p>
          <p className="text-sm text-[#2C2C2C]">Personal Style Profile</p>
        </div>
      </div>
    </div>
  );
}
