from keras.models import load_model
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


class CSV_LSTM_PREDICTION_PIPELINE:
    def __init__(self, dataset, time_column_name, target_column_name,
                 prediction_step, iteration, relative_path_artifacts):
        self.data_path = dataset
        self.df = pd.read_csv(self.data_path)
        self.time_col_name = time_column_name
        self.target_col_name = target_column_name
        self.prediction_step = prediction_step
        self.iteration = iteration
        self.relative_path_artifacts = relative_path_artifacts

        self.model_path = f"{self.relative_path_artifacts}/lstm_model_{self.iteration}.keras"
        self.scaler_path = f"{self.relative_path_artifacts}/lstm_scaler_{self.iteration}.joblib"
        self.target_scaler_path = f"{self.relative_path_artifacts}/lstm_target_scaler_{self.iteration}.joblib"


        self.df[self.time_col_name] = pd.to_datetime(self.df[self.time_col_name])

        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None

        self.scaler = None
        self.target_scaler = None

    def evaluate(self):
        """
        Evaluates the model on the X_test set and prints MAE, MSE, RMSE, and R2 score.
        """
        y_actual, y_pred = self.predict_X_test()
        
        mse = mean_squared_error(y_actual, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_actual, y_pred)
        r2 = r2_score(y_actual, y_pred)
        
        print(f"Evaluation Metrics for iteration {self.iteration}:")
        print(f"Mean Absolute Error (MAE): {mae:.4f}")
        print(f"Mean Squared Error (MSE): {mse:.4f}")
        print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        return {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}


    def extract_time_features(self):
        """Convert datetime to numerical features."""
        self.df['year'] = self.df[self.time_col_name].dt.year
        self.df['month'] = self.df[self.time_col_name].dt.month

    def prepare_data(self):
        """Prepare features and target arrays."""
        self.extract_time_features()
        feature_cols = ['year', 'month']
        self.X = self.df[feature_cols].values
        self.y = self.df[self.target_col_name].values.reshape(-1, 1)

    def train_test_split(self, test_size=0.2):
        split_idx = int(len(self.X) * (1 - test_size))
        self.X_train = self.X[:split_idx]
        self.X_test = self.X[split_idx:]
        self.y_train = self.y[:split_idx]
        self.y_test = self.y[split_idx:]

    def scale_data(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.target_scaler = MinMaxScaler(feature_range=(0, 1))

        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

        self.y_train = self.target_scaler.fit_transform(self.y_train)
        self.y_test = self.target_scaler.transform(self.y_test)

    def create_sequences(self, X_data, y_data):
        """Create sequences for LSTM."""
        X_seq, y_seq = [], []
        for i in range(len(X_data) - self.prediction_step):
            X_seq.append(X_data[i:i + self.prediction_step])
            y_seq.append(y_data[i + self.prediction_step])
        return np.array(X_seq), np.array(y_seq)

    def build_model(self):
        self.model = Sequential()
        input_shape = (self.prediction_step, self.X_train.shape[1])
        self.model.add(LSTM(50, activation='tanh', input_shape=input_shape))
        self.model.add(Dense(1))
        self.model.compile(optimizer='adam', loss='mse')

    def train_model(self, epochs=50, batch_size=16):
        self.X_train_seq, self.y_train_seq = self.create_sequences(self.X_train, self.y_train)
        self.X_test_seq, self.y_test_seq = self.create_sequences(self.X_test, self.y_test)
        self.build_model()
        self.model.fit(self.X_train_seq, self.y_train_seq, epochs=epochs,
                       batch_size=batch_size, verbose=1)

    def save_model(self):
        # Save the Keras model
        self.model.save(f"{self.relative_path_artifacts}/lstm_model_{self.iteration}.keras")
        # Save the scalers using joblib
        joblib.dump(self.scaler, self.scaler_path)
        joblib.dump(self.target_scaler, self.target_scaler_path)


    def load_model(self):
        # Load the Keras model
        self.model = load_model(f"{self.relative_path_artifacts}/lstm_model_{self.iteration}.keras")
        # Load the scalers using joblib
        self.scaler = joblib.load(self.scaler_path)
        self.target_scaler = joblib.load(self.target_scaler_path)


    def predict_sequence(self, input_seq):
        """Predict a single sequence and return in original scale."""
        pred_scaled = self.model.predict(input_seq)
        return self.target_scaler.inverse_transform(pred_scaled)

    def extrapolate(self, start_date, end_date):
        """
        Predict values from start_date to end_date iteratively.
        Returns a DataFrame with 'date' and 'prediction' columns.
        """
        self.load_model()
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df_sorted = self.df.sort_values(by=self.time_col_name).reset_index(drop=True)

        # Get last sequence before start_date
        past_data = df_sorted[df_sorted[self.time_col_name] < start_date]
        if len(past_data) < self.prediction_step:
            raise ValueError("Not enough past data to create initial sequence.")
        initial_seq = past_data.iloc[-self.prediction_step:]
        feature_seq = initial_seq[['year', 'month']].values
        scaled_seq = self.scaler.transform(feature_seq)
        current_seq = scaled_seq.copy()

        future_dates = pd.date_range(start=start_date, end=end_date, freq='MS')
        predictions = []

        for date in future_dates:
            # Reshape and predict
            input_seq = current_seq.reshape(1, self.prediction_step, self.X_train.shape[1])
            pred = self.predict_sequence(input_seq)[0, 0]
            predictions.append({'date': date, 'prediction': pred})

            # Update sequence with new date
            new_feature = np.array([[date.year, date.month]])
            new_feature_scaled = self.scaler.transform(new_feature)
            current_seq = np.vstack([current_seq[1:], new_feature_scaled])

        return pd.DataFrame(predictions)



    def predict_X_test(self):
        """
        Predicts for the X_test set and returns actual vs predicted in original scale.
        """
        self.load_model()
        # Create sequences for X_test
        X_test_seq, y_test_seq = self.create_sequences(self.X_test, self.y_test)

        # Predict
        y_pred_scaled = self.model.predict(X_test_seq)
        y_pred = self.target_scaler.inverse_transform(y_pred_scaled)
        y_actual = self.target_scaler.inverse_transform(y_test_seq)

        return y_actual.flatten(), y_pred.flatten()

    def plot_X_test_predictions(self):
        """
        Plots actual vs predicted values for X_test.
        """
        y_actual, y_pred = self.predict_X_test()
        plt.figure(figsize=(12, 6))
        plt.plot(y_actual, label='Actual', marker='o')
        plt.plot(y_pred, label='Predicted', marker='x')
        plt.title("LSTM Predictions vs Actual Values on X_test")
        plt.xlabel("Time Step")
        plt.ylabel(self.target_col_name)
        plt.legend()
        plt.show()
