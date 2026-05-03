# Troubleshooting - Frontend Not Showing

## Quick Checklist

### 1. Start Backend with API Key
```powershell
# Set API key (IMPORTANT!)
$env:GEMINI_API_KEY="2vNDU9nTXcRgxm0fl5W33NVQ8qOVMjE71tWiLAdcHG7yUtmjkQI1FPSLDBrPJbYv"

# Navigate to Backend
cd C:\Users\yasit\OneDrive\Desktop\Grooming\Backend

# Start backend
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### 2. Start Frontend (In a NEW terminal)
```powershell
# Navigate to Frontend
cd C:\Users\yasit\OneDrive\Desktop\Grooming\Frontend

# Start development server
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 3. Open Browser
Open your browser to: http://localhost:5173

## Common Issues

### Issue: "Blank white page"
**Solution:** Open browser DevTools (F12) → Console tab → Check for errors

### Issue: "Cannot connect to backend"
**Symptoms:** Upload works but no predictions
**Solution:** 
1. Verify backend is running on port 5000
2. Check CORS is enabled in app.py (already done)
3. Try: `curl.exe -X POST -F "file=@path\to\image.jpg" http://127.0.0.1:5000/predict`

### Issue: "Gemini API error"
**Symptoms:** Skin analysis works but hair generation fails
**Solutions:**
1. Verify API key is set: `echo $env:GEMINI_API_KEY`
2. Check API key is valid at https://makersuite.google.com/app/apikey
3. Ensure API key has Gemini API enabled
4. Check backend terminal for error messages

### Issue: "Module not found: react-router-dom"
**Solution:**
```powershell
cd Frontend
npm install react-router-dom
```

## Testing Each Part

### Test 1: Backend is Running
```powershell
curl.exe http://127.0.0.1:5000/predict
```
Expected: Error about missing file (that's OK, means server is running)

### Test 2: Backend Skin Analysis Works
```powershell
curl.exe -X POST -F "file=@C:\Users\yasit\Downloads\asian.jpg" http://127.0.0.1:5000/predict
```
Expected: JSON response with tone, color, blackhead predictions

### Test 3: Backend Hair Generation Works
```powershell
curl.exe -X POST -F "file=@C:\Users\yasit\Downloads\asian.jpg" -F "prompt=Suggest hairstyles" http://127.0.0.1:5000/generate-hair
```
Expected: JSON response with Gemini recommendation

### Test 4: Frontend Loads
Open http://localhost:5173 in browser
Expected: Navigation bar with "Skin Analysis" and "Hair Generation" links

## Browser Console Debugging

If you see a blank page:
1. Press F12 to open DevTools
2. Go to Console tab
3. Look for red error messages
4. Common errors:
   - "Failed to fetch" → Backend not running
   - "Module not found" → Missing npm package
   - "Unexpected token" → Syntax error in code

## Still Not Working?

Share the following information:
1. Screenshot of browser page (with F12 DevTools console visible)
2. Backend terminal output
3. Frontend terminal output
4. Result of: `echo $env:GEMINI_API_KEY` (first 10 characters only)
