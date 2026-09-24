from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.predictor import predict_url

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "WebGuard AI API is running",
        "status": "success"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({
                "error": "URL is required"
            }), 400

        url = data["url"].strip()

        if not url:
            return jsonify({
                "error": "URL cannot be empty"
            }), 400

        result = predict_url(url)

        return jsonify({
            "success": True,
            "url": result["url"],
            "prediction": result["prediction"],
            "risk_level": result["risk_level"],
            "phishing_probability": result["phishing_probability"],
            "legitimate_probability": result["legitimate_probability"]
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )