from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
import random

app = Flask(__name__)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Dummy predictor function (replace this with your actual model)
def predictor(image_link, category_id, entity_name):
    return "10 inch" if random.random() > 0.5 else "5 inch"

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/predict', methods=['POST'])
def predict():
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
