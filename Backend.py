# Install Flask and dependencies
pip install Flask requests pymongo

# Create `app.py`
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# NASA API key (you need to sign up to get one)
NASA_API_KEY = os.getenv('NASA_API_KEY', 'YOUR_NASA_API_KEY')

# Example of a NASA API endpoint for soil moisture
NASA_SOIL_MOISTURE_URL = "https://api.nasa.gov/planetary/earth/assets"

# Route to get soil moisture data based on location (lat, lon)
@app.route('/soil_moisture', methods=['GET'])
def get_soil_moisture():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    # Make API call to NASA API for soil moisture data
    params = {
        'lat': lat,
        'lon': lon,
        'api_key': NASA_API_KEY
    }
    response = requests.get(NASA_SOIL_MOISTURE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

# Example of route for irrigation recommendations based on soil moisture data
@app.route('/irrigation_schedule', methods=['POST'])
def get_irrigation_schedule():
    data = request.get_json()
    crop_type = data.get('crop_type')
    soil_moisture = data.get('soil_moisture')

    if not crop_type or not soil_moisture:
        return jsonify({"error": "Crop type and soil moisture data are required"}), 400
    
    # Simplified logic: schedule depends on soil moisture (you can add ML model here)
    irrigation_schedule = "Irrigate every 3 days" if soil_moisture < 0.3 else "Irrigate every 7 days"
    
    return jsonify({
        "crop_type": crop_type,
        "soil_moisture": soil_moisture,
        "recommendation": irrigation_schedule
    })

if __name__ == '__main__':
    app.run(debug=True)
