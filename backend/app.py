from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import TrendAnalyzer
from genai_engine import GenAIEngine
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize components
analyzer = TrendAnalyzer()
genai_engine = GenAIEngine()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/analyze-trend', methods=['POST'])
def analyze_trend():
    """
    Main endpoint for trend analysis
    
    Expected JSON body:
    {
        "keyword": "string",
        "platform": "string",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['keyword', 'platform', 'start_date', 'end_date']
        if not all(field in data for field in required_fields):
            return jsonify({
                "error": "Missing required fields",
                "required": required_fields
            }), 400
        
        keyword = data['keyword']
        platform = data['platform']
        start_date = data['start_date']
        end_date = data['end_date']
        
        # Step 1: Analyze trend data
        analysis_result = analyzer.analyze(
            keyword=keyword,
            platform=platform,
            start_date=start_date,
            end_date=end_date
        )
        
        # Step 2: Generate AI explanation
        genai_insight = genai_engine.generate_explanation(analysis_result)
        
        # Step 3: Combine results
        response = {
            "trend_status": analysis_result['trend_status'],
            "confidence_score": analysis_result['confidence_score'],
            "predicted_decline_time": analysis_result['predicted_decline_time'],
            "lifecycle": analysis_result['lifecycle'],
            "decline_signals": analysis_result['decline_signals'],
            "feature_importance": analysis_result['feature_importance'],
            "explainable_reasoning": analysis_result['explainable_reasoning'],
            "genai_insight": genai_insight
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/platforms', methods=['GET'])
def get_platforms():
    """Get available platforms"""
    platforms = [
        "Instagram",
        "TikTok",
        "Twitter/X",
        "YouTube",
        "LinkedIn"
    ]
    return jsonify({"platforms": platforms}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
