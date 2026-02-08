import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TrendDataLoader:
    """
    Loads and preprocesses the Kaggle viral trends dataset
    
    CSV Columns (Actual):
    - Post_ID, Post_Date, Platform, Hashtag, Content_Type, Region
    - Views, Likes, Shares, Comments, Engagement_Level
    """
    
    def __init__(self, csv_path='data/viral_trends.csv'):
        """
        Initialize with path to Kaggle dataset
        
        Args:
            csv_path: Path to the viral trends CSV file
        """
        self.csv_path = csv_path
        self.df = None
    
    def load_data(self):
        """Load the CSV file"""
        try:
            self.df = pd.read_csv(self.csv_path)
            
            # Convert Post_Date to datetime (format: DD-MM-YYYY)
            self.df['Post_Date'] = pd.to_datetime(self.df['Post_Date'], format='%d-%m-%Y')
            
            print(f"✓ Loaded {len(self.df)} records from {self.csv_path}")
            return True
        except FileNotFoundError:
            print(f"✗ Dataset not found at {self.csv_path}")
            print("  Please place viral_trends.csv in the data/ folder")
            return False
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return False
    
    def get_trend_data(self, keyword, platform, start_date, end_date):
        """
        Extract data for a specific trend and platform within date range
        
        Args:
            keyword: Hashtag (e.g., "#Gaming" or "Gaming")
            platform: Social media platform
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            DataFrame with filtered trend data, or None if no data found
        """
        if self.df is None:
            if not self.load_data():
                return None
        
        # Clean keyword - ensure it starts with #
        if not keyword.startswith('#'):
            keyword = '#' + keyword
        clean_keyword = keyword.replace('#', '').lower()
        
        # Filter by hashtag (case-insensitive partial match)
        # The CSV has hashtags like "#Gaming", "#Tech", etc.
        hashtag_mask = self.df['Hashtag'].str.lower().str.contains(clean_keyword, na=False)
        
        # Filter by platform (case-insensitive exact match)
        platform_mask = self.df['Platform'].str.lower() == platform.lower()
        
        # Combine filters
        filtered = self.df[hashtag_mask & platform_mask].copy()
        
        # Filter by date range
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        filtered = filtered[(filtered['Post_Date'] >= start) & (filtered['Post_Date'] <= end)]
        
        # Sort by date
        filtered = filtered.sort_values('Post_Date')
        
        if len(filtered) == 0:
            print(f"⚠ No data found for '{keyword}' on {platform} in date range")
            return None
        
        print(f"✓ Found {len(filtered)} posts for '{keyword}' on {platform}")
        return filtered
    
    def compute_engagement_score(self, row):
        """
        Compute total engagement score from metrics
        
        Weighted formula:
        - Likes: 1x (passive engagement)
        - Comments: 3x (active engagement)
        - Shares: 5x (viral indicator)  
        - Views: 0.01x (awareness baseline)
        """
        likes = row.get('Likes', 0) or 0
        comments = row.get('Comments', 0) or 0
        shares = row.get('Shares', 0) or 0
        views = row.get('Views', 0) or 0
        
        engagement = (
            likes * 1 +
            comments * 3 +
            shares * 5 +
            views * 0.01
        )
        
        return int(engagement)
    
    def prepare_lifecycle_data(self, trend_df):
        """
        Convert raw trend data into lifecycle format
        
        Returns:
            dict with dates, engagement, post_frequency arrays
        """
        if trend_df is None or len(trend_df) == 0:
            return None
        
        # Group by date (if multiple posts per day, aggregate)
        trend_df['Date'] = trend_df['Post_Date'].dt.date
        
        # Aggregate daily metrics
        daily_data = trend_df.groupby('Date').agg({
            'Likes': 'sum',
            'Comments': 'sum',
            'Shares': 'sum',
            'Views': 'sum',
            'Post_ID': 'count'  # Count of posts per day
        }).reset_index()
        
        # Rename post count
        daily_data.rename(columns={'Post_ID': 'Post_Count'}, inplace=True)
        
        # Compute engagement scores
        engagement_scores = []
        for _, row in daily_data.iterrows():
            score = self.compute_engagement_score(row)
            engagement_scores.append(score)
        
        # Format dates as "Day 1", "Day 2", etc.
        dates = [f"Day {i+1}" for i in range(len(daily_data))]
        
        return {
            'dates': dates,
            'engagement': engagement_scores,
            'post_frequency': daily_data['Post_Count'].tolist(),
            'raw_daily_data': daily_data  # Keep for further analysis
        }
    
    def get_available_trends(self, limit=20):
        """
        Get list of available hashtags in the dataset
        
        Returns:
            List of dicts with hashtag info
        """
        if self.df is None:
            if not self.load_data():
                return []
        
        # Group by hashtag and platform
        trends = self.df.groupby(['Hashtag', 'Platform']).agg({
            'Post_ID': 'count',
            'Likes': 'sum',
            'Views': 'sum'
        }).reset_index()
        
        # Rename columns for clarity
        trends.rename(columns={'Post_ID': 'Total_Posts'}, inplace=True)
        
        # Sort by total engagement (likes + views)
        trends['Total_Engagement'] = trends['Likes'] + (trends['Views'] * 0.01)
        trends = trends.sort_values('Total_Engagement', ascending=False).head(limit)
        
        return trends[['Hashtag', 'Platform', 'Total_Posts']].to_dict('records')
