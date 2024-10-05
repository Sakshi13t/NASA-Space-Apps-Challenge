from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/test")
db = client.aquacrop

# Example of storing user input
@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    user_data = {
        "location": data.get("location"),
        "crop_type": data.get("crop_type"),
        "soil_moisture": data.get("soil_moisture"),
        "irrigation_schedule": data.get("irrigation_schedule")
    }
    db.user_data.insert_one(user_data)
    return jsonify({"message": "Data saved successfully"}), 201
