# 📊 Dataset Reference - Viral Trends CSV

## Dataset Information

**File:** `viral_trends.csv`  
**Total Records:** 5,000 social media posts  
**Date Range:** January 2022 - December 2023  
**Source:** Kaggle Viral Social Media Trends Dataset

---

## CSV Structure

### Column Names
```
Post_ID, Post_Date, Platform, Hashtag, Content_Type, Region,
Views, Likes, Shares, Comments, Engagement_Level
```

### Column Details

| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `Post_ID` | String | Unique post identifier | Post_1, Post_2, ... |
| `Post_Date` | Date | When post was created | 13-01-2022 (DD-MM-YYYY) |
| `Platform` | String | Social media platform | TikTok, Instagram, YouTube, Twitter |
| `Hashtag` | String | Main hashtag for the post | #Gaming, #Tech, #Dance |
| `Content_Type` | String | Type of content | Video, Shorts, Post, Tweet, Reel, Live Stream |
| `Region` | String | Geographic region | USA, UK, India, Brazil, Japan, Germany, Canada, Australia |
| `Views` | Integer | Number of views | 0 - 5,000,000 |
| `Likes` | Integer | Number of likes | 0 - 500,000 |
| `Shares` | Integer | Number of shares | 0 - 100,000 |
| `Comments` | Integer | Number of comments | 0 - 50,000 |
| `Engagement_Level` | String | Overall engagement | High, Medium, Low |

---

## Available Hashtags

The dataset contains exactly **10 hashtags**:

1. **#Gaming** - Gaming and esports content
2. **#Tech** - Technology and innovation
3. **#Dance** - Dance challenges and choreography
4. **#Challenge** - Viral challenges
5. **#Comedy** - Comedy and humor content
6. **#Education** - Educational and learning content
7. **#Fashion** - Fashion and style trends
8. **#Fitness** - Health and fitness content
9. **#Music** - Music and audio trends
10. **#Viral** - General viral content

---

## Available Platforms

1. **TikTok** - Short-form video platform
2. **Instagram** - Photo and video sharing
3. **YouTube** - Long-form and short-form video
4. **Twitter** - Microblogging and tweets

---

## Sample Data

```csv
Post_ID,Post_Date,Platform,Hashtag,Content_Type,Region,Views,Likes,Shares,Comments,Engagement_Level
Post_1,13-01-2022,TikTok,#Challenge,Video,UK,4163464,339431,53135,19346,High
Post_8,14-01-2022,YouTube,#Gaming,Shorts,UK,2066886,317502,45222,33638,High
Post_39,28-09-2022,TikTok,#Gaming,Shorts,USA,4499253,469481,89583,41549,High
```

---

## Data Distribution

### Posts by Platform (Approximate)
- YouTube: ~1,250 posts
- TikTok: ~1,250 posts
- Instagram: ~1,250 posts
- Twitter: ~1,250 posts

### Posts by Hashtag (Approximate)
- Each hashtag: ~500 posts

### Date Range Coverage
- 2022: ~2,500 posts
- 2023: ~2,500 posts

---

## How Our System Uses This Data

### 1. Data Loading (`data_loader.py`)
```python
loader = TrendDataLoader('data/viral_trends.csv')
trend_data = loader.get_trend_data(
    keyword="#Gaming",
    platform="YouTube",
    start_date="2022-01-01",
    end_date="2022-12-31"
)
```

### 2. Engagement Score Calculation
```python
engagement_score = (
    Likes * 1 +
    Comments * 3 +
    Shares * 5 +
    Views * 0.01
)
```

### 3. Daily Aggregation
Posts are grouped by date and metrics are summed:
- Multiple posts on same day → Combined into single data point
- Engagement scores calculated per day
- Post frequency counted per day

### 4. Lifecycle Analysis
System creates time series showing:
- Daily engagement trends
- Post frequency over time
- Engagement velocity (rate of change)

---

## Example Queries

### High Engagement Trends
```
Keyword: Gaming
Platform: YouTube
Date Range: 2022-01-01 to 2022-06-30
Expected: Hundreds of posts, high engagement
```

### Declining Trends
```
Keyword: Challenge
Platform: TikTok
Date Range: 2023-06-01 to 2023-12-31
Expected: Shows decline pattern over time
```

### Cross-Platform Comparison
```
Same Hashtag: #Tech
Platform 1: Twitter (2022)
Platform 2: Instagram (2023)
Compare engagement patterns
```

---

## Data Quality Notes

### Strengths
✅ Consistent date format  
✅ Clean numeric fields  
✅ No missing values in key columns  
✅ Realistic engagement ranges  
✅ Good distribution across platforms  

### Limitations
⚠️ Simulated dataset (not real social media data)  
⚠️ Limited to 10 hashtags  
⚠️ 2-year date range only  
⚠️ No sentiment text data  
⚠️ No user demographics details  

---

## Testing Tips

### Quick Tests
1. **Load test:** `loader.load_data()` → Should load 5000 records
2. **Filter test:** Search for `#Gaming` on `YouTube` → Should find hundreds
3. **Date test:** Use 2022 dates → More data available
4. **Platform test:** All 4 platforms should work

### Expected Results
- **Found data:** 50-500 posts per query (depending on date range)
- **No data:** Wrong hashtag, platform mismatch, or date range issue
- **Processing time:** < 1 second for most queries

---

## Troubleshooting

**"No data found"**
- Check hashtag spelling (must match exactly)
- Verify platform name (TikTok, Instagram, YouTube, Twitter)
- Expand date range (try 2022-01-01 to 2023-12-31)

**"Error loading data"**
- Verify CSV is at `backend/data/viral_trends.csv`
- Check file isn't corrupted
- Ensure pandas is installed

**"Too few data points"**
- Expand date range
- Try different hashtag
- Check if platform has that hashtag

---

## Integration with Featherless AI

When real data is loaded, AI explanations become more accurate:

**Simulated Data Response:**
```
"This trend shows typical decline patterns..."
```

**Real Data Response:**
```
"Based on 347 #Gaming posts on YouTube from Jan-Jun 2022, 
engagement dropped 52% from peak levels in March. The data shows
317,502 average likes declining to 124,237 by June..."
```

Much more specific and credible!

---

**The dataset is already included in your project** at `backend/data/viral_trends.csv` 🎉
