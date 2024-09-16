from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
import random

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

# Dummy predictor function (replace this with your actual model)
def predictor(image_link, category_id, entity_name):
    # Example prediction logic using a random choice for entity units
    predicted_value = hash(entity_name) % 100  # Dummy prediction logic (you can replace with real model logic)
    unit = get_random_unit(entity_name)
    return f"{predicted_value} {unit}"

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission and file upload
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the form
    image_link = request.form['image_link']
    category_id = request.form['category_id']
    entity_name = request.form['entity_name']
    
    # Check if a CSV file was uploaded
    csv_file = request.files.get('csv_file')
    if csv_file and csv_file.filename != '':
        filepath = os.path.join(UPLOAD_FOLDER, csv_file.filename)
        csv_file.save(filepath)
        
        # Load CSV file and perform predictions
        data = pd.read_csv(filepath)
        
        # Check if the necessary columns exist
        if not {'index', 'image_link', 'group_id', 'entity_name'}.issubset(data.columns):
            return "CSV must contain 'index', 'image_link', 'group_id', and 'entity_name' columns", 400
        
        # Apply the predictor function to each row
        data['prediction'] = data.apply(
            lambda row: predictor(row['image_link'], row['group_id'], row['entity_name']), axis=1)
        
        # Save the predictions to a new CSV file
        output_filename = os.path.join(UPLOAD_FOLDER, 'test_out.csv')
        data[['index', 'prediction']].to_csv(output_filename, index=False)
        
        return f"Predictions saved to {output_filename}."

    # If no CSV is uploaded, perform prediction on the input data from the form
    prediction = predictor(image_link, category_id, entity_name)
    return f"The predicted value for the entity is: {prediction}"

# Starting the Flask application
if __name__ == "__main__":
    app.run(debug=True)
