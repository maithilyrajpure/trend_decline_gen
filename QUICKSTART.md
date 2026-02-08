# 🚀 Quick Start Guide (30 Seconds)

## For Hackathon Judges / Reviewers

### Step 1: Start Backend (10 seconds)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

Wait for: `Running on http://0.0.0.0:5000`

### Step 2: Open Frontend (5 seconds)
```bash
cd ../frontend
open index.html
```
(Or double-click `index.html` in file explorer)

### Step 3: Try It Out (15 seconds)
1. Enter keyword: `#Gaming`
2. Select platform: `YouTube`
3. Keep default dates
4. Click **"Analyze Trend"**
5. Watch the magic! 🎉

---

## What You'll See

- **Trend Status** with confidence score
- **Predicted decline timeline**
- **Interactive charts** (engagement lifecycle, decline factors)
- **AI-generated insights** (data analysis + recommendations)
- **Decline signals breakdown** with visual bars

---

## Key Selling Points

✅ **Explainable AI** - Transparent reasoning, not a black box  
✅ **Production Architecture** - Clean separation, scalable design  
✅ **Professional UI** - Modern, data-focused dashboard  
✅ **Business Impact** - Saves marketing budgets, optimizes ROI  

---

## Common Issues

**"Connection failed"**
→ Make sure backend is running on port 5000

**"CORS error"**
→ Backend has Flask-CORS enabled, should work automatically

**"No results"**
→ Check browser console for errors

---

## Architecture Overview

```
Frontend (HTML/CSS/JS)
    ↓ POST /analyze-trend
Backend (Flask)
    ↓
Analyzer (Trend Analysis)
    ↓
GenAI Engine (Explanations)
    ↓
Results (JSON) → Frontend Charts
```

---

**Questions?** Check the main README.md for full documentation.
