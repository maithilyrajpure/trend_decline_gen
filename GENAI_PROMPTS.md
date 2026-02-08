# 🤖 GenAI Integration Prompts

This document contains the exact prompts to use when integrating real LLM APIs (Claude, GPT-4, etc.) into the system.

---

## Frontend Expectation Prompt

**Use this when designing the UI or explaining to stakeholders:**

```
Design a responsive analytics dashboard for a Social Media Trend Decline 
Prediction System.

The dashboard should accept a hashtag or keyword, platform selection, 
and date range. It should visualize trend lifecycle data, decline signals, 
and AI-generated explanations.

The UI must clearly communicate both predictions and reasons behind 
trend decline using:
- Status cards (trend status, confidence, timeline)
- Interactive charts (lifecycle trends, factor importance)
- AI-generated insights (data analysis + strategic recommendations)
- Decline signals breakdown (engagement, sentiment, saturation, influencer activity)

Style: Professional, data-focused, dark theme with electric accents.
```

---

## Backend GenAI Analysis Prompt

**Use this in genai_engine.py when calling Claude/GPT API:**

```python
SYSTEM_PROMPT = """
You are an Explainable AI system specialized in social media trend analysis.

Your role is to analyze structured trend data and provide clear, evidence-based 
insights about trend health and trajectory.

CRITICAL RULES:
1. Base ALL conclusions strictly on provided data
2. Cite specific numbers and percentages from the signals
3. Explain causality (WHY the trend is declining, not just THAT it is)
4. Provide actionable strategic recommendations
5. Avoid speculation or assumptions beyond the data
6. Use professional, concise language (3-4 sentences maximum)

OUTPUT FORMAT:
- Sentence 1: Current trend status and primary contributing factor
- Sentence 2: Supporting evidence with specific metrics
- Sentence 3-4: Strategic recommendation for brands/creators

TONE: Professional, analytical, confident but not overstated.
"""

USER_PROMPT_TEMPLATE = """
Analyze this social media trend and provide an explainable insight:

TREND METADATA:
- Keyword: {keyword}
- Platform: {platform}
- Analysis Period: {start_date} to {end_date}

TREND STATUS:
- Classification: {trend_status}
- Confidence: {confidence_score}
- Predicted Decline: {predicted_decline_time}

DECLINE SIGNALS:
- Engagement Drop: {engagement_drop_pct}% (from peak to current)
- Sentiment Score: {sentiment_score} (range: -1 to +1)
- Influencer Activity Ratio: {influencer_activity_ratio} (% still active)
- Content Saturation Score: {content_saturation_score} (0-1, higher = more saturated)

FEATURE IMPORTANCE (what's driving decline):
{feature_importance}

DATA-DRIVEN REASONING:
{explainable_reasoning}

Based on this analysis, generate a strategic insight that:
1. Explains the current trend state and primary causes
2. Cites specific evidence from the signals above
3. Provides a clear recommendation for marketers/creators

Your insight:
"""
```

---

## Example API Call (Anthropic Claude)

```python
import anthropic
import os

def generate_explanation_with_claude(analysis_result):
    """
    Generate AI insight using Claude API
    """
    client = anthropic.Anthropic(
        api_key=os.getenv('ANTHROPIC_API_KEY')
    )
    
    # Format the user prompt with data
    user_prompt = USER_PROMPT_TEMPLATE.format(
        keyword=analysis_result.get('keyword', 'Unknown'),
        platform=analysis_result.get('platform', 'Unknown'),
        start_date=analysis_result.get('start_date', 'Unknown'),
        end_date=analysis_result.get('end_date', 'Unknown'),
        trend_status=analysis_result['trend_status'],
        confidence_score=f"{analysis_result['confidence_score'] * 100:.0f}%",
        predicted_decline_time=analysis_result['predicted_decline_time'],
        engagement_drop_pct=analysis_result['decline_signals']['engagement_drop_pct'],
        sentiment_score=analysis_result['decline_signals']['sentiment_score'],
        influencer_activity_ratio=analysis_result['decline_signals']['influencer_activity_ratio'],
        content_saturation_score=analysis_result['decline_signals']['content_saturation_score'],
        feature_importance='\n'.join([
            f"- {k}: {v*100:.0f}%" 
            for k, v in analysis_result['feature_importance'].items()
        ]),
        explainable_reasoning=analysis_result['explainable_reasoning']
    )
    
    # Make API call
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Extract text from response
    insight = response.content[0].text
    
    return insight.strip()
```

---

## Example API Call (OpenAI GPT-4)

```python
from openai import OpenAI
import os

def generate_explanation_with_gpt(analysis_result):
    """
    Generate AI insight using GPT-4 API
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Format the user prompt with data
    user_prompt = USER_PROMPT_TEMPLATE.format(
        # ... same as above
    )
    
    # Make API call
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        max_tokens=500,
        temperature=0.7,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    # Extract text from response
    insight = response.choices[0].message.content
    
    return insight.strip()
```

---

## Integration Steps

### 1. Install SDK
```bash
# For Claude
pip install anthropic

# For OpenAI
pip install openai
```

### 2. Set API Key
```bash
# In backend/.env
ANTHROPIC_API_KEY=sk-ant-xxxxx
# or
OPENAI_API_KEY=sk-xxxxx
```

### 3. Update genai_engine.py

Replace the `generate_explanation()` method:

```python
def generate_explanation(self, analysis_result):
    """
    Generate human-readable insight from analysis results
    """
    if self.api_key:
        # Use real LLM API
        return generate_explanation_with_claude(analysis_result)
        # or return generate_explanation_with_gpt(analysis_result)
    else:
        # Fallback to rule-based (current implementation)
        return self._generate_rule_based_explanation(analysis_result)
```

### 4. Test
```bash
python app.py
# Make a test request and verify the AI-generated insight
```

---

## Expected Output Quality

### Rule-Based (Current)
```
This trend is entering an early decline phase. Engagement metrics show 
consistent downward trajectory (38% decline), and creator interest is 
waning. Brands still active in this trend should prepare exit strategies 
or refresh creative approaches.
```

### LLM-Enhanced (After Integration)
```
The #SummerVibes trend has entered early decline with engagement falling 
38% from peak levels, driven primarily by content saturation (81% similarity 
score) and diminishing influencer participation (45% reduction). Data shows 
a clear downward velocity over the past week, suggesting the trend has passed 
its creative peak. Brands should either pivot to fresh creative angles that 
differentiate from saturated content or prepare exit strategies within the 
next 5-7 days to preserve ROI.
```

The LLM version will be:
- More specific and contextual
- Better at explaining causality chains
- More nuanced in recommendations
- Better at adapting tone to severity

---

## Cost Estimation

### Claude Sonnet 4 (as of Feb 2026)
- Input: ~500 tokens per request
- Output: ~150 tokens per request
- Cost: ~$0.015 per analysis
- 1000 analyses = ~$15

### GPT-4 Turbo
- Input: ~500 tokens per request
- Output: ~150 tokens per request  
- Cost: ~$0.01 per analysis
- 1000 analyses = ~$10

**Recommendation:** Start with Claude for better explainability and reasoning.

---

## Advanced: Multi-Agent Analysis

For even better insights, use multiple LLM calls:

```python
def generate_comprehensive_insight(analysis_result):
    # Agent 1: Technical Analysis
    technical = call_llm(TECHNICAL_ANALYST_PROMPT, analysis_result)
    
    # Agent 2: Business Strategy
    strategy = call_llm(BUSINESS_STRATEGIST_PROMPT, analysis_result)
    
    # Agent 3: Synthesis
    final = call_llm(SYNTHESIS_PROMPT, {
        "technical": technical,
        "strategy": strategy,
        "data": analysis_result
    })
    
    return final
```

This creates more robust, multi-perspective insights at 3x the cost.

---

## Monitoring & Evaluation

Track these metrics:

```python
# Log every LLM call
{
    "timestamp": "2026-02-07T10:30:00Z",
    "model": "claude-sonnet-4",
    "input_tokens": 487,
    "output_tokens": 142,
    "latency_ms": 1250,
    "cost_usd": 0.0147,
    "trend_status": "Early Decline",
    "user_rating": 4.5  # if you add feedback
}
```

---

**Ready to integrate?** Start with the Claude example above and test with a few queries!
