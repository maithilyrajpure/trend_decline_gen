# 📋 CSV Field Reference - viral_trends.csv

## Dataset Overview

**File included:** `backend/data/viral_trends.csv`  
**Total records:** 5,000+ posts  
**Date range:** January 2022 - December 2023  
**File size:** ~500 KB

---

## Column Structure

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| **Post_ID** | String | Unique identifier | Post_1, Post_2, Post_3 |
| **Post_Date** | Date | When post was created | 13-01-2022, 23-03-2023 |
| **Platform** | String | Social media platform | TikTok, Instagram, Twitter, YouTube |
| **Hashtag** | String | Main trend hashtag | #Gaming, #Challenge, #Dance |
| **Content_Type** | String | Type of content | Video, Shorts, Post, Tweet, Reel, Live Stream |
| **Region** | String | Geographic region | UK, India, Brazil, Australia, Japan, Germany, Canada, USA |
| **Views** | Integer | Number of views | 4163464, 2051091 |
| **Likes** | Integer | Number of likes | 339431, 24472 |
| **Shares** | Integer | Number of shares | 53135, 54704 |
| **Comments** | Integer | Number of comments | 19346, 41737 |
| **Engagement_Level** | String | Pre-classified level | High, Medium, Low |

---

## Available Hashtags

The dataset includes these 10 main hashtags:

1. **#Gaming** - Gaming content and streams
2. **#Challenge** - Viral challenges
3. **#Dance** - Dance videos and trends
4. **#Comedy** - Comedy sketches and humor
5. **#Education** - Educational content
6. **#Music** - Music-related posts
7. **#Tech** - Technology news and reviews
8. **#Fitness** - Fitness and wellness
9. **#Fashion** - Fashion and style
10. **#Viral** - General viral content

---

## Available Platforms

1. **TikTok** - Short-form video platform
2. **Instagram** - Photos, reels, and stories
3. **Twitter** - Microblogging and updates
4. **YouTube** - Long-form video content

---

## Date Format

**Format:** `DD-MM-YYYY`  
**Examples:**
- `13-01-2022` = January 13, 2022
- `23-03-2023` = March 23, 2023
- `08-11-2022` = November 8, 2022

**Important:** This is different from standard YYYY-MM-DD format!

---

## Sample Queries That Work

### Query 1: Gaming on YouTube
```
Keyword: #Gaming or Gaming
Platform: YouTube
Date Range: 2022-01-01 to 2023-12-31
```
**Expected:** Lots of data (hundreds of posts)

### Query 2: Challenge on TikTok
```
Keyword: #Challenge or Challenge
Platform: TikTok
Date Range: 2022-01-01 to 2023-12-31
```
**Expected:** High engagement, viral trends

### Query 3: Dance on Instagram
```
Keyword: #Dance or Dance
Platform: Instagram
Date Range: 2022-06-01 to 2022-12-31
```
**Expected:** Seasonal data, varying engagement

### Query 4: Tech on Twitter
```
Keyword: #Tech or Tech
Platform: Twitter
Date Range: 2022-01-01 to 2023-06-30
```
**Expected:** Consistent engagement patterns

### Query 5: Education on YouTube
```
Keyword: #Education or Education
Platform: YouTube
Date Range: 2023-01-01 to 2023-12-31
```
**Expected:** Growing trend

---

## Engagement Calculation

The system calculates a **weighted engagement score**:

```python
Engagement Score = (
    Likes × 1 +
    Comments × 3 +
    Shares × 5 +
    Views × 0.01
)
```

**Why these weights?**
- **Views (0.01):** Passive metric, shows reach
- **Likes (1x):** Minimal effort, baseline engagement
- **Comments (3x):** Active engagement, conversation
- **Shares (5x):** Highest value, indicates virality

---

## Data Aggregation

When analyzing trends, the system:

1. **Filters** posts by hashtag and platform
2. **Groups** by date (daily aggregation)
3. **Sums** all engagement metrics per day
4. **Counts** number of posts per day
5. **Calculates** engagement scores
6. **Analyzes** trends over time

---

## Example Data Points

### High Engagement Post
```csv
Post_8,14-01-2022,YouTube,#Gaming,Shorts,UK,2066886,317502,45222,33638,High
```
- Views: 2M+
- Likes: 317K
- Shares: 45K
- Comments: 33K
- **Engagement Score:** ~643K

### Medium Engagement Post
```csv
Post_19,08-05-2022,TikTok,#Fashion,Post,USA,3461154,165335,50077,19505,Low
```
- Views: 3.4M
- Likes: 165K
- Shares: 50K
- Comments: 19K
- **Engagement Score:** ~469K

### Low Engagement Post
```csv
Post_22,26-01-2022,TikTok,#Viral,Live Stream,USA,3924406,35376,72832,3949,Medium
```
- Views: 3.9M
- Likes: 35K
- Shares: 72K
- Comments: 3K
- **Engagement Score:** ~459K

---

## Testing the Data Loader

### Python Test Script
```python
from data_loader import TrendDataLoader

# Initialize
loader = TrendDataLoader('data/viral_trends.csv')

# Load data
loader.load_data()
# Should see: ✓ Loaded 5000+ records

# Get trend data
data = loader.get_trend_data(
    keyword='Gaming',
    platform='YouTube',
    start_date='2022-01-01',
    end_date='2023-12-31'
)
# Should see: ✓ Found XXX data points

# Check available trends
trends = loader.get_available_trends()
print(trends)
```

---

## Common Issues & Solutions

### Issue: "No data found for trend"

**Possible causes:**
1. Keyword spelling (try without #)
2. Platform name case-sensitive
3. Date range too narrow
4. Hashtag not in dataset

**Solutions:**
```python
# Try different variations:
'Gaming' instead of '#Gaming'
'TikTok' instead of 'tiktok'
Wider date range: 2022-01-01 to 2023-12-31
```

### Issue: "Very few data points"

**Solution:** Expand date range or try a different hashtag

### Issue: "Date parsing error"

**Solution:** The CSV uses DD-MM-YYYY format, system converts automatically

---

## Data Quality Notes

✅ **Clean data** - No missing values in key columns  
✅ **Balanced platforms** - All platforms represented  
✅ **Time series** - 2 years of data (2022-2023)  
✅ **Realistic metrics** - Views, likes, shares, comments  
✅ **Categorized** - Pre-labeled engagement levels  

⚠ **Limitations:**
- Engagement_Level is pre-classified (may not match our calculations)
- No sentiment data (we approximate from patterns)
- No influencer flags (we approximate from posting frequency)

---

## Integration with Backend

The `data_loader.py` handles:
- ✅ Loading CSV with pandas
- ✅ Converting DD-MM-YYYY dates
- ✅ Filtering by hashtag (case-insensitive)
- ✅ Filtering by platform (case-insensitive)
- ✅ Date range filtering
- ✅ Daily aggregation
- ✅ Engagement score calculation
- ✅ Lifecycle data formatting

The `analyzer.py` receives this clean data and:
- ✅ Calculates decline signals
- ✅ Performs statistical analysis
- ✅ Generates predictions
- ✅ Computes confidence scores

---

**This CSV is now integrated and ready to use!** 🎉
