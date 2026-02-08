# 🤖 Featherless AI Integration Guide

## What is Featherless AI?

Featherless AI is a **free-tier LLM API** that provides access to open-source models like Llama without requiring payment or complex setup.

**Why we use it:**
- ✅ **Free tier available** (no credit card needed)
- ✅ **Fast API responses** (< 2 seconds)
- ✅ **Open-source models** (Meta Llama 3.1)
- ✅ **Simple REST API** (easy to integrate)
- ✅ **No vendor lock-in** (can switch to OpenAI/Claude later)

---

## Step 1: Get API Key

1. **Visit:** https://featherless.ai
2. **Sign up** (email + password, no payment info needed)
3. **Go to API Keys section**
4. **Create new API key**
5. **Copy the key** (looks like: `sk-...`)

---

## Step 2: Add to Your Project

**Edit `backend/.env`:**
```env
FEATHERLESS_API_KEY=sk-your-actual-key-here
```

**That's it!** The system will automatically detect the key and use AI explanations.

---

## How It Works

### The Prompt Strategy

We use a **two-stage approach**:

**Stage 1: Backend Calculates Signals**
```python
# analyzer.py computes these mathematically:
{
    "engagement_drop_pct": 38,
    "engagement_velocity": -0.042,
    "post_freq_decline_pct": 25,
    "content_saturation_score": 0.81,
    "sentiment_score": -0.42,
    "influencer_activity_ratio": 0.55
}
```

**Stage 2: Featherless AI Explains**
```python
# genai_engine.py sends signals to AI with this prompt:
"""
You are an expert social media analytics explainer.
Your job is to EXPLAIN these PRECOMPUTED signals.

DECLINE SIGNALS (Precomputed):
  - Engagement Drop: 38%
  - Engagement Velocity: -0.042 (negative = declining)
  - Content Saturation Score: 0.81
  ...

Based on these signals, explain in 3-4 sentences:
1. What is happening to this trend?
2. WHY is it happening?
3. What should marketers do?
"""
```

### Why This Approach Works

✅ **Prevents hallucination** - AI only explains real numbers, doesn't invent data  
✅ **Fast & cheap** - Small prompt = quick response  
✅ **Consistent** - Same signals always get similar explanations  
✅ **Explainable** - Can verify AI's reasoning against the signals  

---

## API Details

**Endpoint:**
```
POST https://api.featherless.ai/v1/chat/completions
```

**Model we use:**
```
meta-llama/Meta-Llama-3.1-8B-Instruct
```

**Request format:**
```json
{
  "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
  "messages": [
    {
      "role": "system",
      "content": "You are an expert social media analytics explainer..."
    },
    {
      "role": "user",
      "content": "Analyze this trend: [signals here]"
    }
  ],
  "max_tokens": 300,
  "temperature": 0.7
}
```

**Response format:**
```json
{
  "choices": [
    {
      "message": {
        "content": "This trend is entering early decline phase..."
      }
    }
  ]
}
```

---

## Example AI Responses

### Input Signals:
```
Engagement Drop: 42%
Engagement Velocity: -0.055
Content Saturation: 0.78
Influencer Activity: 48%
```

### AI Output (Featherless):
```
This trend is experiencing rapid decline driven primarily by severe 
content saturation (78% similarity) and influencer exodus (52% reduction). 
The engagement velocity of -0.055 indicates accelerating decay, with 
total engagement falling 42% from peak levels. Brands should immediately 
pivot creative strategy or exit the trend within 5-7 days to preserve ROI.
```

### Fallback (Rule-Based):
```
This trend is entering an early decline phase. Engagement metrics show 
consistent downward trajectory (42% decline), and creator interest is 
waning. Brands still active in this trend should prepare exit strategies 
or refresh creative approaches.
```

**Notice:** AI version is more specific and nuanced!

---

## Cost & Rate Limits

**Free Tier:**
- 1000 requests per day
- ~100-300 tokens per response
- Adequate for hackathons and demos

**Paid Tier (if needed):**
- ~$0.0001 per 1K tokens
- 1000 analyses = ~$0.10

**For this project:**
- 1 analysis = 1 API call
- 100 demo queries = free
- Perfect for hackathons!

---

## Testing the Integration

### Without API Key:
```bash
# In backend/.env, leave FEATHERLESS_API_KEY empty

python app.py
# Start analysis

# You'll see:
⚠ Using rule-based explanations (set FEATHERLESS_API_KEY to use AI)
```

### With API Key:
```bash
# In backend/.env:
FEATHERLESS_API_KEY=sk-your-key

python app.py
# Start analysis

# You'll see:
✓ Generated AI insight using meta-llama/Meta-Llama-3.1-8B-Instruct
```

---

## Error Handling

The system has **automatic fallback**:

```python
try:
    # Try Featherless AI
    insight = call_featherless_api(signals)
except Exception as e:
    print(f"⚠ AI error: {e}, falling back")
    # Use rule-based explanation
    insight = generate_rule_based(signals)
```

**You'll never see a crash** - system gracefully degrades.

---

## Advanced: Prompt Engineering

### Our System Prompt (Optimized)

```python
"""You are an expert social media analytics explainer. 
Your job is to analyze PRECOMPUTED trend decline signals 
and explain them in clear, concise language.

RULES:
1. You are NOT predicting - you are EXPLAINING already-calculated signals
2. Base ALL statements on the provided numeric data
3. Cite specific percentages and scores from the signals
4. Explain WHY the trend is declining (causality, not just correlation)
5. Keep explanations to 2-4 sentences maximum
6. Use professional, confident tone
7. Provide ONE actionable recommendation for marketers

AVOID:
- Speculation beyond the data
- Vague statements
- Overly technical jargon
- Lengthy explanations"""
```

**Why this works:**
- ✅ Clear role definition
- ✅ Explicit constraints (no hallucination)
- ✅ Format guidance (2-4 sentences)
- ✅ Evidence requirement (cite numbers)

---

## Comparison with Other APIs

| Feature | Featherless AI | OpenAI GPT-4 | Claude |
|---------|---------------|--------------|--------|
| Free Tier | ✅ 1000/day | ❌ | ❌ |
| Setup | Easy | Credit card | Credit card |
| Speed | Fast | Faster | Fast |
| Quality | Good | Excellent | Excellent |
| Cost | Free → $0.0001/1K | $0.01/1K | $0.003/1K |

**For hackathons:** Featherless is perfect  
**For production:** Can upgrade to GPT-4/Claude with same code

---

## Switching to Other APIs

The code is designed to be **API-agnostic**. To switch:

### To OpenAI:
```python
# genai_engine.py
import openai

def _generate_with_openai(self, analysis_result):
    client = openai.OpenAI(api_key=self.api_key)
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content
```

### To Claude:
```python
# genai_engine.py
import anthropic

def _generate_with_claude(self, analysis_result):
    client = anthropic.Anthropic(api_key=self.api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.content[0].text
```

**Same prompt structure works across all APIs!**

---

## Troubleshooting

**"API returned 401"**
→ Invalid API key, check `.env` file

**"API returned 429"**
→ Rate limit hit (wait 1 minute or upgrade tier)

**"Connection timeout"**
→ Network issue, system will auto-fallback

**"Response is empty"**
→ Model didn't generate, check prompt formatting

---

## For Hackathon Judges

**Highlight these points:**

1. **"We use Featherless AI for explainable insights"**
   - Shows you integrated real AI
   - Free tier = no ongoing costs
   - Production-ready architecture

2. **"The AI only EXPLAINS, it doesn't predict"**
   - Shows understanding of AI limitations
   - More trustworthy than black-box predictions
   - Evidence-based approach

3. **"Automatic fallback ensures reliability"**
   - System never crashes
   - Works with or without API
   - Graceful degradation

---

**Get your key and try it now:** https://featherless.ai 🚀
