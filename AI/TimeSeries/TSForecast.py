from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from TimeSeriesNetworks import CSV_LSTM_PREDICTION_PIPELINE as CLPP

# Flask app setup
app = Flask(__name__)
app.secret_key = 'tejas'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PREDICTION_STEP = 3  # Example value

# Function to process the file
def process_file(filepath, inputColName, outputColName, start_date, end_date):
    df = pd.read_csv(filepath)
    print(f"Data preview:\n{df.head()}")

    runModel(filepath, inputColName, outputColName, start_date, end_date)
    return "File processed successfully!"

# Function to run the prediction model
def runModel(filepath, inputColName, outputColName, start_date, end_date):
    obj = CLPP(
        dataset=filepath,
        time_column_name=inputColName,
        target_column_name=outputColName,
        prediction_step=PREDICTION_STEP,
        iteration=1,
        relative_path_artifacts="TSArtifacts"
    )   

    obj.prepare_data()
    obj.train_test_split()
    obj.scale_data()
    obj.train_model(epochs=150, batch_size=4)
    obj.save_model()

    obj.evaluate()

    pred_df = obj.extrapolate(start_date=start_date, end_date=end_date)
    print(pred_df)

    obj.plot_X_test_predictions()

    df = pd.read_csv(filepath)
    df[inputColName] = pd.to_datetime(df[inputColName])

    plt.plot(pred_df['date'], pred_df['prediction'], label="Forecast")
    plt.plot(df[inputColName], df[outputColName], label="Actual", alpha=0.5)
    plt.legend()
    plt.show()

# Home page route
@app.route('/')
def index():
    return render_template('upload.html')



# Upload route
@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Extract parameters from form
        inputColName = request.form.get('inputColName')
        outputColName = request.form.get('outputColName')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        result_message = process_file(filepath, inputColName, outputColName, start_date, end_date)

        message = f"File '{file.filename}' uploaded successfully! {result_message}"
        return render_template('upload.html', message=message)
    else:
        message = "Please upload a valid CSV file."
        return render_template('upload.html', message=message)

if __name__ == "__main__":
    app.run()
