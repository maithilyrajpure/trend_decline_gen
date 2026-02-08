# 🎯 Quick Reference Card

## Installation (3 Commands)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Then open `frontend/index.html` in browser.

---

## Test Queries (Copy-Paste Ready)

### Query 1: Gaming Trend
```
Keyword: Gaming
Platform: YouTube
Start Date: 2022-01-01
End Date: 2022-12-31
```
**Expected:** 100+ posts, shows real data

### Query 2: Tech Trend
```
Keyword: Tech
Platform: Instagram
Start Date: 2023-01-01
End Date: 2023-12-31
```
**Expected:** 100+ posts, shows real data

### Query 3: Dance Challenge
```
Keyword: Dance
Platform: TikTok
Start Date: 2022-06-01
End Date: 2023-06-30
```
**Expected:** 200+ posts, full year data

---

## Available Hashtags (All Work)

`Gaming` • `Tech` • `Dance` • `Challenge` • `Comedy` • `Education` • `Fashion` • `Fitness` • `Music` • `Viral`

---

## Available Platforms (All Work)

`TikTok` • `Instagram` • `YouTube` • `Twitter`

---

## Success Indicators

✅ Backend console shows:
```
✓ Loaded 5000 records from data/viral_trends.csv
✓ Found XX posts for '#Gaming' on YouTube
✓ Using REAL Kaggle data
```

✅ Frontend shows:
- Status cards with real numbers
- Two charts (lifecycle + factors)
- AI insights

---

## Optional: Add AI Explanations

1. Get free key: https://featherless.ai
2. Edit `backend/.env`:
   ```
   FEATHERLESS_API_KEY=sk-your-key-here
   ```
3. Restart backend

---

## Troubleshooting

**"ModuleNotFoundError"**
→ Run: `pip install -r requirements.txt`

**"Dataset not found"**
→ Check: `backend/data/viral_trends.csv` exists

**"No data found"**
→ Use hashtags from the list above
→ Use dates between 2022-2023

---

## File Locations

```
├── backend/
│   ├── data/viral_trends.csv  ← Dataset (5000 posts)
│   └── .env                   ← Add API key here (optional)
└── frontend/
    └── index.html             ← Double-click to open
```

---

**Ready to demo in 60 seconds!** 🚀
