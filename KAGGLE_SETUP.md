# 📊 Dataset Setup Guide

## Good News - CSV Already Included! ✅

Your project now includes the **viral_trends.csv** file in `backend/data/`.

**No manual download needed!** The dataset is ready to use.

---

## Dataset Details

**File:** `backend/data/viral_trends.csv`  
**Records:** 5,000+ social media posts  
**Date Range:** January 2022 - December 2023  
**Platforms:** TikTok, Instagram, Twitter, YouTube  

### Hashtags Available:
- #Gaming
- #Challenge
- #Dance
- #Comedy
- #Education
- #Music
- #Tech
- #Fitness
- #Fashion
- #Viral

---

## Verify Dataset is Ready

```bash
cd backend

# Check if file exists
ls data/viral_trends.csv

# Should see: data/viral_trends.csv
```

---

## Test Data Loading

```bash
cd backend
python

# In Python shell:
from data_loader import TrendDataLoader

loader = TrendDataLoader('data/viral_trends.csv')
loader.load_data()

# Should see: "✓ Loaded 5000+ records from data/viral_trends.csv"

# Check available trends:
trends = loader.get_available_trends()
print(trends)
```

---

## Example Queries

The dataset contains these hashtags that you can search for:

| Keyword | Platform | Example |
|---------|----------|---------|
| `Gaming` or `#Gaming` | YouTube, TikTok, Instagram, Twitter | Gaming trends and esports |
| `Tech` or `#Tech` | YouTube, Instagram, Twitter | Technology content |
| `Dance` or `#Dance` | TikTok, Instagram, YouTube | Dance challenges |
| `Challenge` or `#Challenge` | TikTok, Instagram, Twitter | Viral challenges |
| `Comedy` or `#Comedy` | YouTube, Instagram, Twitter | Comedy content |
| `Education` or `#Education` | YouTube, Instagram, Twitter | Educational posts |
| `Fashion` or `#Fashion` | Instagram, TikTok | Fashion trends |
| `Fitness` or `#Fitness` | Instagram, YouTube | Health and fitness |
| `Music` or `#Music` | YouTube, Instagram, Twitter | Music trends |
| `Viral` or `#Viral` | TikTok, Instagram, YouTube | Viral content |

**Format:**
- Keyword: `Gaming` or `#Gaming` (both work)
- Platform: `YouTube`, `TikTok`, `Instagram`, or `Twitter` (case-insensitive)
- Date: Use range `2022-01-01` to `2023-12-31`

---

## How the System Uses the Data

1. **User enters trend** → Frontend
2. **API call** → Backend (`app.py`)
3. **TrendDataLoader** → Loads CSV, filters by hashtag/platform/date
4. **Daily aggregation** → Sums engagement metrics per day
5. **TrendAnalyzer** → Calculates mathematical decline signals
6. **GenAIEngine** → Generates explanation
7. **Results** → Frontend displays charts

---

## CSV Structure

```csv
Post_ID,Post_Date,Platform,Hashtag,Content_Type,Region,Views,Likes,Shares,Comments,Engagement_Level
Post_1,13-01-2022,TikTok,#Challenge,Video,UK,4163464,339431,53135,19346,High
Post_2,13-05-2022,Instagram,#Education,Shorts,India,4155940,215240,65860,27239,Medium
```

**Columns:**
- `Post_ID` - Unique identifier
- `Post_Date` - DD-MM-YYYY format
- `Platform` - TikTok, Instagram, Twitter, YouTube
- `Hashtag` - #Gaming, #Dance, etc.
- `Views, Likes, Shares, Comments` - Engagement metrics
- `Engagement_Level` - High, Medium, Low

See **CSV_FIELD_REFERENCE.md** for complete details.

---

## Troubleshooting

**"Dataset not found"**
```bash
# The file should be at: backend/data/viral_trends.csv
# If missing, download from your project files
```

**"No data found for trend"**
```bash
# Try these working examples:
Keyword: Gaming
Platform: YouTube
Date: 2022-01-01 to 2023-12-31
```

**"Date parsing error"**
```bash
# The CSV uses DD-MM-YYYY format
# System converts this automatically
# Just use YYYY-MM-DD in the frontend
```

---

## Next Steps

✅ Dataset is included and ready  
✅ No manual download needed  
✅ Just run `pip install -r requirements.txt`  
✅ Then `python app.py`  

**Optional:** Get Featherless AI key for AI-powered insights  
See: **FEATHERLESS_AI_GUIDE.md**

---

**You're all set!** The real dataset is integrated and working. 🚀
