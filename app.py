from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import random
import os

app = Flask(__name__)

# Define entity_unit_map directly in the app.py file
entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'maximum_weight_recommendation': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitre', 'pint', 'quart'}
}

# Function to get a random unit for each entity based on the entity name
def get_random_unit(entity_name):
    units = entity_unit_map.get(entity_name)
    if units:
        return random.choice(list(units))
    return 'unknown unit'

# Example function to predict entity value (replace with actual logic)
def predict_entity_value(entity_name):
    return hash(entity_name) % 100  # Dummy prediction logic

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form data
    image_link = request.form.get('image_link', '')
    
    # Check if a file is uploaded
    if 'csv_file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['csv_file']
    if file.filename == '':
        return "No file selected", 400

    if file:
        # Save the file to process
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        # Load CSV and process it
        data = pd.read_csv(file_path)
        
        # Check if required columns are present
        if not {'index', 'entity_name'}.issubset(data.columns):
            return "CSV must contain 'index' and 'entity_name' columns", 400
        
        # Generate predictions
        data['unit'] = data['entity_name'].apply(get_random_unit)
        data['prediction_value'] = data['entity_name'].apply(predict_entity_value) * 1.1  # Example operation
        data['prediction_value'] = data['prediction_value'].astype(str)  # Convert prediction_value to string
        data['prediction'] = [f"{x} {unit}" for x, unit in zip(data['prediction_value'], data['unit'])]

        # Save results to test_out.csv without the group_id and entity_name columns
        output_file = 'test_out.csv'
        data[['index', 'prediction']].to_csv(output_file, index=False)
        
        return f"Prediction complete. Results saved in {output_file}."

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)  # Create uploads directory if not exists
    app.run(debug=True)
