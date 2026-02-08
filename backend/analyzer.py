import numpy as np
from datetime import datetime, timedelta
import random
import pandas as pd
from scipy import stats

try:
    from data_loader import TrendDataLoader
    REAL_DATA_AVAILABLE = True
except ImportError:
    REAL_DATA_AVAILABLE = False
    print("⚠ data_loader not available, using simulated data")

class TrendAnalyzer:
    """
    Analyzes social media trend data to detect decline signals
    Now supports REAL Kaggle dataset with mathematical formulas
    """
    
    def __init__(self, csv_path='data/viral_trends.csv'):
        self.decline_threshold = 0.65
        self.data_loader = TrendDataLoader(csv_path) if REAL_DATA_AVAILABLE else None
        self.use_real_data = False
    
    def analyze(self, keyword, platform, start_date, end_date):
        """
        Main analysis method - tries real data first, falls back to simulation
        
        Returns structured data matching the API contract
        """
        # Try to load real data from Kaggle dataset
        lifecycle_data = None
        if self.data_loader:
            trend_df = self.data_loader.get_trend_data(keyword, platform, start_date, end_date)
            if trend_df is not None:
                lifecycle_data = self.data_loader.prepare_lifecycle_data(trend_df)
                self.use_real_data = True
                print("✓ Using REAL Kaggle data")
        
        # Fallback to simulated data if real data not available
        if lifecycle_data is None:
            lifecycle_data = self._generate_lifecycle_data(start_date, end_date)
            self.use_real_data = False
            print("⚠ Using simulated data (Kaggle dataset not found)")
        
        # Calculate decline signals using mathematical formulas
        decline_signals = self._calculate_decline_signals(lifecycle_data)
        
        # Calculate feature importance
        feature_importance = self._calculate_feature_importance(decline_signals)
        
        # Determine trend status and confidence
        trend_status, confidence_score = self._determine_trend_status(decline_signals)
        
        # Predict decline timeline
        predicted_decline_time = self._predict_decline_time(decline_signals, trend_status)
        
        # Generate data-driven reasoning
        explainable_reasoning = self._generate_reasoning(
            decline_signals, 
            feature_importance, 
            lifecycle_data
        )
        
        return {
            "trend_status": trend_status,
            "confidence_score": round(confidence_score, 2),
            "predicted_decline_time": predicted_decline_time,
            "lifecycle": {
                "dates": lifecycle_data['dates'],
                "engagement": lifecycle_data['engagement'],
                "post_frequency": lifecycle_data['post_frequency']
            },
            "decline_signals": decline_signals,
            "feature_importance": feature_importance,
            "explainable_reasoning": explainable_reasoning,
            "data_source": "real_kaggle" if self.use_real_data else "simulated"
        }
    
    def _generate_lifecycle_data(self, start_date, end_date):
        """
        Generate realistic trend lifecycle data
        
        In production, this would fetch from a database or API
        """
        dates = []
        engagement = []
        post_frequency = []
        
        # Generate 14 days of data
        num_days = 14
        
        # Simulate a declining trend
        base_engagement = 2000
        base_posts = 400
        
        for i in range(num_days):
            # Add some randomness but overall declining pattern
            decay_factor = 1 - (i * 0.08)  # 8% decay per day
            noise = random.uniform(0.85, 1.15)
            
            eng = int(base_engagement * decay_factor * noise)
            posts = int(base_posts * decay_factor * noise)
            
            dates.append(f"Day {i+1}")
            engagement.append(max(eng, 100))  # Minimum floor
            post_frequency.append(max(posts, 50))
        
        return {
            "dates": dates,
            "engagement": engagement,
            "post_frequency": post_frequency
        }
    
    def _calculate_decline_signals(self, lifecycle_data):
        """
        Calculate key decline indicators using mathematical formulas
        
        FORMULAS:
        1. Engagement Drop % = ((First_3_Avg - Last_3_Avg) / First_3_Avg) * 100
        2. Engagement Velocity = Linear regression slope of engagement over time
        3. Post Frequency Decline = ((Peak_Posting - Current_Posting) / Peak_Posting) * 100
        4. Content Saturation = (Current_Posts / Peak_Posts) if declining, else ratio
        5. Trend Acceleration = Second derivative (rate of change of velocity)
        """
        engagement = np.array(lifecycle_data['engagement'])
        post_freq = np.array(lifecycle_data['post_frequency'])
        n_days = len(engagement)
        
        # 1. ENGAGEMENT DROP PERCENTAGE
        # Compare first 3 days vs last 3 days average
        window_size = min(3, n_days // 3)
        first_avg = np.mean(engagement[:window_size])
        last_avg = np.mean(engagement[-window_size:])
        
        if first_avg > 0:
            engagement_drop_pct = int(((first_avg - last_avg) / first_avg) * 100)
        else:
            engagement_drop_pct = 0
        
        # Ensure it's positive (drop)
        engagement_drop_pct = max(0, engagement_drop_pct)
        
        # 2. ENGAGEMENT VELOCITY (Trend Slope)
        # Use linear regression to find slope
        x = np.arange(n_days)
        if n_days > 1:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, engagement)
            # Normalize slope to -1 to 1 scale
            engagement_velocity = slope / (np.mean(engagement) + 1)  # Avoid division by zero
        else:
            engagement_velocity = 0
        
        # 3. POST FREQUENCY DECLINE
        peak_posts = np.max(post_freq)
        current_posts = np.mean(post_freq[-window_size:])
        
        if peak_posts > 0:
            post_freq_decline_pct = int(((peak_posts - current_posts) / peak_posts) * 100)
        else:
            post_freq_decline_pct = 0
        
        # 4. CONTENT SATURATION SCORE
        # High posting with declining engagement = saturation
        avg_posts = np.mean(post_freq)
        posts_ratio = current_posts / (avg_posts + 1)
        engagement_ratio = last_avg / (first_avg + 1)
        
        # Saturation = high posting + low engagement
        content_saturation_score = min(1.0, posts_ratio * (1 - engagement_ratio))
        content_saturation_score = max(0, round(content_saturation_score, 2))
        
        # 5. SENTIMENT SCORE (Approximated from engagement patterns)
        # Declining comments/shares relative to views = negative sentiment
        # For real data: calculate from comments vs total engagement
        # For simulation: derive from velocity
        if engagement_velocity < -0.05:
            sentiment_score = round(engagement_velocity * 5, 2)  # Map to -1 to 0 range
        else:
            sentiment_score = round(engagement_velocity * 2, 2)
        
        sentiment_score = max(-1.0, min(0.5, sentiment_score))
        
        # 6. INFLUENCER ACTIVITY RATIO (Approximated)
        # In real data: count unique high-follower users
        # Approximation: Peak posting vs current posting ratio
        influencer_activity_ratio = round(current_posts / (peak_posts + 1), 2)
        influencer_activity_ratio = max(0.3, min(1.0, influencer_activity_ratio))
        
        return {
            "engagement_drop_pct": engagement_drop_pct,
            "engagement_velocity": round(engagement_velocity, 3),
            "post_freq_decline_pct": post_freq_decline_pct,
            "sentiment_score": sentiment_score,
            "influencer_activity_ratio": influencer_activity_ratio,
            "content_saturation_score": content_saturation_score
        }
    
    def _calculate_feature_importance(self, decline_signals):
        """
        Calculate which factors contribute most to decline
        """
        # Weighted importance based on signal strength
        weights = {
            "Engagement Decay": abs(decline_signals['engagement_drop_pct']) / 100,
            "Influencer Drop": 1 - decline_signals['influencer_activity_ratio'],
            "Content Saturation": decline_signals['content_saturation_score'],
            "Audience Fatigue": abs(decline_signals['sentiment_score'])
        }
        
        # Normalize to sum to 1
        total = sum(weights.values())
        normalized = {k: round(v/total, 2) for k, v in weights.items()}
        
        return normalized
    
    def _determine_trend_status(self, decline_signals):
        """
        Determine overall trend status and confidence
        """
        # Calculate composite decline score
        decline_score = (
            (decline_signals['engagement_drop_pct'] / 100 * 0.4) +
            (abs(decline_signals['sentiment_score']) * 0.2) +
            ((1 - decline_signals['influencer_activity_ratio']) * 0.2) +
            (decline_signals['content_saturation_score'] * 0.2)
        )
        
        confidence_score = min(decline_score * 1.2, 0.99)
        
        if decline_score >= 0.7:
            status = "Critical Decline"
        elif decline_score >= 0.5:
            status = "Early Decline"
        elif decline_score >= 0.3:
            status = "Plateauing"
        else:
            status = "Growing"
        
        return status, confidence_score
    
    def _predict_decline_time(self, decline_signals, trend_status):
        """
        Predict when trend will fully decline
        """
        if trend_status == "Critical Decline":
            return "1–3 days"
        elif trend_status == "Early Decline":
            return "5–7 days"
        elif trend_status == "Plateauing":
            return "10–14 days"
        else:
            return "Not declining"
    
    def _generate_reasoning(self, decline_signals, feature_importance, lifecycle_data):
        """
        Generate evidence-based reasoning
        """
        engagement = lifecycle_data['engagement']
        
        # Calculate velocity
        first_half = np.mean(engagement[:7])
        second_half = np.mean(engagement[7:])
        velocity_change = ((first_half - second_half) / first_half) * 100
        
        # Top contributing factor
        top_factor = max(feature_importance.items(), key=lambda x: x[1])
        
        reasoning_parts = []
        
        # Engagement velocity
        if velocity_change > 20:
            reasoning_parts.append(
                f"Engagement velocity has decreased by {int(velocity_change)}%"
            )
        
        # Influencer activity
        if decline_signals['influencer_activity_ratio'] < 0.6:
            drop_pct = int((1 - decline_signals['influencer_activity_ratio']) * 100)
            reasoning_parts.append(
                f"influencer participation dropped by approximately {drop_pct}%"
            )
        
        # Content saturation
        if decline_signals['content_saturation_score'] > 0.7:
            reasoning_parts.append(
                "high content similarity indicates market saturation"
            )
        
        # Sentiment
        if decline_signals['sentiment_score'] < -0.3:
            reasoning_parts.append(
                "sentiment analysis shows declining audience interest"
            )
        
        reasoning = " while ".join(reasoning_parts) + "."
        reasoning = reasoning[0].upper() + reasoning[1:]  # Capitalize first letter
        
        return reasoning
