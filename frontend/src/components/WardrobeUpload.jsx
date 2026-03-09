import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, CheckCircle2, Plus } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../lib/utils';

export function WardrobeUpload({ onUploadComplete }) {
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress]       = useState(0);
  const [isComplete, setIsComplete]   = useState(false);
  const [count, setCount]             = useState(0);
  const [total, setTotal]             = useState(0);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (!acceptedFiles.length) return;
    setIsUploading(true);
    setProgress(0);
    setTotal(acceptedFiles.length);
    setCount(0);

    let done = 0;
    const results = [];

    for (const file of acceptedFiles) {
      const fd = new FormData();
      fd.append('image', file);
      try {
        const res  = await fetch('http://localhost:5000/api/predict/clothing-type', { method: 'POST', body: fd });
        const data = await res.json();
        results.push(data);
      } catch (e) {
        results.push({ success: false, error: e.message });
      }
      done++;
      setCount(done);
      setProgress(Math.round((done / acceptedFiles.length) * 100));
    }

    setIsUploading(false);
    setIsComplete(true);
    setTimeout(() => {
      onUploadComplete(results);
      setIsComplete(false);
      setProgress(0);
    }, 1600);
  }, [onUploadComplete]);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpeg', '.jpg', '.png', '.webp'] },
    multiple: true,
    disabled: isUploading,
    noClick: true,
  });

  return (
    <div {...getRootProps()} className="relative">
      <input {...getInputProps()} />

      {/* Drag-over glow border */}
      <AnimatePresence>
        {isDragActive && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute -inset-1 rounded-2xl border-2 border-dashed border-[#8B5A5A] bg-[#8B5A5A]/5 z-10 flex items-center justify-center pointer-events-none"
          >
            <span className="text-[#8B5A5A] text-sm font-medium">Drop to add</span>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence mode="wait">

        {/* ── Uploading state ── */}
        {isUploading && (
          <motion.div
            key="uploading"
            initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
            className="flex items-center gap-3 bg-white border border-[#E5E0D8] rounded-xl px-4 py-3 shadow-sm"
          >
            {/* Mini ring */}
            <div className="relative w-9 h-9 flex-shrink-0">
              <svg className="w-full h-full -rotate-90">
                <circle cx="18" cy="18" r="15" stroke="#EDE8E0" strokeWidth="3" fill="none" />
                <circle cx="18" cy="18" r="15" stroke="#8B5A5A" strokeWidth="3" fill="none"
                  strokeDasharray="94.25"
                  strokeDashoffset={94.25 - (94.25 * progress) / 100}
                  className="transition-all duration-100 ease-linear"
                />
              </svg>
              <span className="absolute inset-0 flex items-center justify-center text-[9px] font-bold text-[#8B5A5A]">{progress}%</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-[#2C2C2C]">{count} of {total} uploaded</p>
              <p className="text-[11px] text-[#A8A098]">Analyzing with AI…</p>
            </div>
          </motion.div>
        )}

        {/* ── Complete state ── */}
        {!isUploading && isComplete && (
          <motion.div
            key="complete"
            initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}
            className="flex items-center gap-3 bg-white border border-green-200 rounded-xl px-4 py-3 shadow-sm"
          >
            <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
              <CheckCircle2 className="w-4 h-4 text-green-600" />
            </div>
            <p className="text-xs font-semibold text-green-700">{total} item{total !== 1 ? 's' : ''} added to wardrobe!</p>
          </motion.div>
        )}

        {/* ── Idle state ── */}
        {!isUploading && !isComplete && (
          <motion.div
            key="idle"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="flex items-center gap-3 bg-white border border-[#E5E0D8] rounded-xl px-4 py-3 shadow-sm"
          >
            <div className="w-8 h-8 rounded-full bg-[#F0EBE4] flex items-center justify-center flex-shrink-0">
              <Upload className="w-3.5 h-3.5 text-[#8B5A5A]" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-[#2C2C2C] leading-tight">Add to wardrobe</p>
              <p className="text-[10px] text-[#B0A098]">JPG · PNG · WEBP · drag anywhere</p>
            </div>
            <button
              onClick={open}
              className="flex-shrink-0 inline-flex items-center gap-1.5 px-4 py-2 bg-[#2C2C2C] hover:bg-black text-white text-xs font-semibold rounded-full transition-all active:scale-95 shadow"
            >
              <Plus className="w-3 h-3" /> Upload
            </button>
          </motion.div>
        )}

      </AnimatePresence>

      {/* Phase steps */}
      <div className="flex items-center justify-end gap-2 mt-2 pr-1">
        {['Visual Extraction', 'Event Scoring', 'Style Profile'].map((label, i) => (
          <React.Fragment key={label}>
            <div className="flex items-center gap-1">
              <span className="w-4 h-4 rounded-full bg-[#E8E4DE] text-[#8B5A5A] text-[9px] font-bold flex items-center justify-center">{i + 1}</span>
              <span className="text-[10px] text-[#A8A098]">{label}</span>
            </div>
            {i < 2 && <span className="w-3 h-px bg-[#DDD5CA]" />}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}