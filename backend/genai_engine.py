import os
import requests
import json

class GenAIEngine:
    """
    Generates explainable AI insights about trend decline using Featherless AI
    
    Featherless AI analyzes PRECOMPUTED signals only - it does NOT predict
    It EXPLAINS why decline is happening based on the data
    """
    
    def __init__(self):
        self.api_key = os.getenv('FEATHERLESS_API_KEY', None)
        self.api_url = "https://api.featherless.ai/v1/chat/completions"
        self.model = "meta-llama/Meta-Llama-3.1-8B-Instruct"  # Free tier model
        self.use_api = self.api_key is not None
    
    def generate_explanation(self, analysis_result):
        """
        Generate human-readable insight from analysis results
        
        Uses Featherless AI if API key is available, otherwise falls back to rules
        """
        
        if self.use_api:
            try:
                return self._generate_with_featherless_ai(analysis_result)
            except Exception as e:
                print(f"⚠ Featherless AI error: {e}, falling back to rule-based")
                return self._generate_rule_based(analysis_result)
        else:
            print("⚠ Using rule-based explanations (set FEATHERLESS_API_KEY to use AI)")
            return self._generate_rule_based(analysis_result)
    
    def _generate_with_featherless_ai(self, analysis_result):
        """
        Call Featherless AI API with optimized prompt
        """
        # Extract key data
        status = analysis_result['trend_status']
        signals = analysis_result['decline_signals']
        features = analysis_result['feature_importance']
        data_source = analysis_result.get('data_source', 'unknown')
        
        # Build the prompt
        system_prompt = self._get_featherless_system_prompt()
        user_prompt = self._build_user_prompt(analysis_result)
        
        # API request payload
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Make API call
        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            insight = result['choices'][0]['message']['content'].strip()
            print(f"✓ Generated AI insight using {self.model}")
            return insight
        else:
            raise Exception(f"API returned {response.status_code}: {response.text}")
    
    def _get_featherless_system_prompt(self):
        """
        Optimized system prompt for Featherless AI
        
        CRITICAL: This prevents hallucination and ensures evidence-based responses
        """
        return """You are an expert social media analytics explainer. Your job is to analyze PRECOMPUTED trend decline signals and explain them in clear, concise language.

RULES:
1. You are NOT predicting - you are EXPLAINING already-calculated signals
2. Base ALL statements on the provided numeric data
3. Cite specific percentages and scores from the signals
4. Explain WHY the trend is declining (causality, not just correlation)
5. Keep explanations to 2-4 sentences maximum
6. Use professional, confident tone
7. Provide ONE actionable recommendation for marketers

OUTPUT FORMAT:
- Sentence 1: State the trend status and primary cause
- Sentence 2: Support with specific signal data (cite numbers)
- Sentence 3-4: Explain the mechanism and provide strategic recommendation

AVOID:
- Speculation beyond the data
- Vague statements
- Overly technical jargon
- Lengthy explanations"""
    
    def _build_user_prompt(self, analysis_result):
        """
        Build the user prompt with structured signal data
        """
        status = analysis_result['trend_status']
        signals = analysis_result['decline_signals']
        features = analysis_result['feature_importance']
        reasoning = analysis_result['explainable_reasoning']
        data_source = analysis_result.get('data_source', 'analyzed data')
        
        # Format feature importance
        features_str = "\n".join([
            f"  - {k}: {v*100:.0f}% contribution"
            for k, v in sorted(features.items(), key=lambda x: x[1], reverse=True)
        ])
        
        prompt = f"""Analyze this social media trend decline and provide a clear explanation:

TREND STATUS: {status}
DATA SOURCE: {data_source}

DECLINE SIGNALS (Precomputed):
  - Engagement Drop: {signals['engagement_drop_pct']}%
  - Engagement Velocity: {signals.get('engagement_velocity', 'N/A')} (negative = declining)
  - Post Frequency Decline: {signals.get('post_freq_decline_pct', 'N/A')}%
  - Content Saturation Score: {signals['content_saturation_score']} (0-1 scale)
  - Sentiment Score: {signals['sentiment_score']} (-1 to +1 scale)
  - Influencer Activity: {signals['influencer_activity_ratio']*100:.0f}% still active

CONTRIBUTING FACTORS:
{features_str}

DATA-DRIVEN OBSERVATION:
{reasoning}

Based on these PRECOMPUTED signals, explain in 3-4 sentences:
1. What is happening to this trend?
2. WHY is it happening (cite specific signals)?
3. What should marketers do?"""
        
        return prompt
    
    def _generate_rule_based(self, analysis_result):
        """
        Fallback rule-based explanation (original implementation)
        """
        
        
        # Extract key data
        status = analysis_result['trend_status']
        signals = analysis_result['decline_signals']
        features = analysis_result['feature_importance']
        
        # Get top contributing factors
        sorted_features = sorted(features.items(), key=lambda x: x[1], reverse=True)
        primary_factor = sorted_features[0][0]
        secondary_factor = sorted_features[1][0]
        
        # Generate insight based on status and signals
        if status == "Critical Decline":
            insight = self._generate_critical_insight(
                signals, primary_factor, secondary_factor
            )
        elif status == "Early Decline":
            insight = self._generate_early_decline_insight(
                signals, primary_factor, secondary_factor
            )
        elif status == "Plateauing":
            insight = self._generate_plateau_insight(
                signals, primary_factor, secondary_factor
            )
        else:
            insight = self._generate_growth_insight(signals)
        
        return insight
    
    def _generate_critical_insight(self, signals, primary, secondary):
        """Generate insight for critical decline"""
        base = f"This trend is in critical decline. "
        
        # Primary cause
        if "Engagement" in primary:
            base += f"The primary driver is severe engagement decay ({signals['engagement_drop_pct']}% drop), "
        elif "Influencer" in primary:
            ratio_pct = int((1 - signals['influencer_activity_ratio']) * 100)
            base += f"The primary driver is sharp influencer abandonment ({ratio_pct}% reduction), "
        elif "Saturation" in primary:
            base += f"The primary driver is extreme content saturation (score: {signals['content_saturation_score']}), "
        else:
            base += f"The primary driver is audience fatigue (sentiment: {signals['sentiment_score']}), "
        
        # Secondary cause
        if "Engagement" in secondary:
            base += f"compounded by rapid engagement loss. "
        elif "Influencer" in secondary:
            base += f"compounded by creator exodus. "
        elif "Saturation" in secondary:
            base += f"compounded by content oversaturation. "
        else:
            base += f"compounded by negative sentiment shifts. "
        
        # Recommendation
        base += "Brands should immediately exit this trend or pivot to adjacent messaging. "
        base += "Continuing investment will likely result in diminished ROI."
        
        return base
    
    def _generate_early_decline_insight(self, signals, primary, secondary):
        """Generate insight for early decline"""
        base = f"This trend is entering an early decline phase. "
        
        # Cause analysis
        if "Engagement" in primary:
            base += f"Engagement metrics show consistent downward trajectory ({signals['engagement_drop_pct']}% decline), "
        elif "Influencer" in primary:
            base += f"Key influencers are reducing participation, "
        elif "Saturation" in primary:
            base += f"Content saturation is becoming evident, "
        else:
            base += f"Audience sentiment is turning negative, "
        
        # Secondary signal
        if "Influencer" in secondary:
            base += f"and creator interest is waning. "
        elif "Saturation" in secondary:
            base += f"and the market shows signs of oversaturation. "
        else:
            base += f"and engagement velocity is slowing. "
        
        # Strategic recommendation
        base += "Brands still active in this trend should prepare exit strategies or refresh creative approaches. "
        base += "There's a narrow window to capitalize before the trend becomes unprofitable."
        
        return base
    
    def _generate_plateau_insight(self, signals, primary, secondary):
        """Generate insight for plateau"""
        base = f"This trend is plateauing, showing early warning signs. "
        
        if signals['content_saturation_score'] > 0.6:
            base += f"Content saturation (score: {signals['content_saturation_score']}) suggests the trend is maturing. "
        
        if signals['influencer_activity_ratio'] < 0.7:
            base += f"Influencer engagement is moderating, which often precedes broader decline. "
        
        base += "Brands should monitor closely and consider diversifying their content strategy. "
        base += "This is an optimal time to test new creative angles before momentum fully shifts."
        
        return base
    
    def _generate_growth_insight(self, signals):
        """Generate insight for growing trends"""
        base = "This trend is still growing or maintaining strong momentum. "
        
        if signals['engagement_drop_pct'] < 10:
            base += "Engagement remains stable with minimal decay. "
        
        if signals['influencer_activity_ratio'] > 0.7:
            base += "Influencer participation is strong, indicating continued creator interest. "
        
        base += "Brands can confidently invest in this trend, though monitoring for saturation signals is advisable."
        
        return base
    
    def get_llm_prompt_template(self):
        """
        Returns the prompt template for using with actual LLM APIs
        
        Use this when integrating Claude API, OpenAI, etc.
        """
        return """You are an Explainable AI system designed to analyze social media trends.

Given structured data about a trend's engagement, sentiment, influencer activity,
and content saturation, your task is to:

1. Determine whether the trend is declining.
2. Explain WHY the decline is happening using evidence from the data.
3. Avoid speculation. Base explanations strictly on provided signals.
4. Provide actionable insights for marketers or creators.

Return the explanation in clear, concise, professional language.

DATA:
{analysis_result}

Generate a 3-4 sentence insight that explains:
- Current trend status and key contributing factors
- Evidence from the data (specific numbers/percentages)
- Strategic recommendation for brands/creators
"""
