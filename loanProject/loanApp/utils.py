import pandas as pd
import io
import os
from sklearn import preprocessing
import joblib
from django.http import HttpResponse
from .models import *
from django.db.models import Max

def get_available_models():
    model_folder = 'newMLmodels'
    models = [file for file in os.listdir(model_folder) if file.endswith('.joblib')]
    return models

def select_model(selected_model):
    model_path = os.path.join('newMLmodels', selected_model)
    if not os.path.exists(model_path):
        raise FileNotFoundError("Selected model not found")
    
    return load_model(model_path)

def read_csv_file(csv_file):
    try:
        csv_content = csv_file.read().decode("utf-8")
        print("CSV Content:")
        print(csv_content)

        csv_data = pd.read_csv(io.StringIO(csv_content), sep='[;,]', engine='python')
        return csv_data

    except pd.errors.EmptyDataError:
        return HttpResponse("Empty CSV file")
    except Exception as e:
        return HttpResponse(f"Error reading CSV file: {e}")

def apply_label_encoders(csv_data):
    records_list = csv_data.to_dict(orient="records")

    label_encoder_marital = preprocessing.LabelEncoder()
    csv_data['EmploymentType'] = label_encoder_marital.fit_transform(csv_data['EmploymentType'])

    return csv_data, records_list

def load_model(model_path):
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        return HttpResponse("Model file not found")

def make_predictions(model, csv_data, records_list):
    predictions = model.predict(csv_data)
    predictions_list = predictions.tolist()
    zipped_data = list(zip(records_list, predictions_list))

    return zipped_data

def save_to_database(records_list, predictions):
    for record, prediction in zip(records_list, predictions):
        try:
            applicant = LoanApplicant.objects.create(
                Age=record['Age'],
                Income=record['Income'],
                LoanAmount=record['LoanAmount'],
                CreditScore=record['CreditScore'],
                MonthsEmployed=record['MonthsEmployed'],
                LoanTerm=record['LoanTerm'],
                DTIRatio=record['DTIRatio'],
                EmploymentType= record['EmploymentType'],
            )
            applicant.Default = prediction
            applicant.save()

        except Exception as e:
            print(f"Error processing record: {e}")
