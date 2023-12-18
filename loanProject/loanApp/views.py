from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .utils import *
import plotly.express as px
import base64
import pandas as pd
import joblib
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import os
from openai import OpenAI
from allauth.account.views import PasswordResetView as AllauthPasswordResetView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


# Create your views here.

client = OpenAI(api_key='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')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return render(request, 'login.html', {'form': form})
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def logout_user(request):
    logout(request)
    messages.success(request, ("You are logged out."))
    return redirect('welcome')


def home(request):
    return render(request, 'home.html')

def welcome(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return render(request, 'login.html', {'form': form})
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()

    #return render(request, 'welcome.html')
    return render(request, "home.html", {
        "form": form,
    })

def user_dashboard(request):
    if request.user.is_authenticated:
        user = request.user

        email = request.user.email
        username = request.user.username
        name = request.user.first_name + " " + request.user.last_name
        
        return render(request, "user/user-dashboard.html", {
            "name": name, 
            "email": email,
            "usr": username,
        })
     
    else:
        return render(request, 'anonymousProfile.html')


def loan_history(request):
    return render(request, 'user/loan-history.html')

def create_applicant(request):
    context = {'messages': []}

    if request.method == 'POST':
        form = LoanForm(request.POST)

        if form.is_valid():
            Age = form.cleaned_data['Age']
            Income_SEK = form.cleaned_data['Income']
            LoanAmount_SEK = form.cleaned_data['LoanAmount']
            CreditScore = form.cleaned_data['CreditScore']
            MonthsEmployed = form.cleaned_data['MonthsEmployed']
            LoanTerm = form.cleaned_data['LoanTerm']
            DTIRatio = form.cleaned_data['DTIRatio']
            
            manual_exchange_rate = 10
            Income_USD = Income_SEK / manual_exchange_rate
            LoanAmount_USD = LoanAmount_SEK / manual_exchange_rate
           
            model_path = 'newMLmodels/Tree_model.joblib'
            model = load_model(model_path)
            prediction = model.predict([[Age, Income_USD, LoanAmount_USD, CreditScore, MonthsEmployed, LoanTerm, DTIRatio]])
            print("Prediction Result:", prediction[0])

            save_to_database(
                [{
                    'Age': Age,
                    'Income': Income_USD,
                    'LoanAmount': LoanAmount_USD,
                    'CreditScore': CreditScore,
                    'MonthsEmployed': MonthsEmployed,
                    'LoanTerm': LoanTerm,
                    'DTIRatio': DTIRatio,
                }],
                [prediction[0]],
            )

            context['prediction_data'] = {
                'headers': ['Age', 'Income', 'LoanAmount', 'CreditScore', 'MonthsEmployed', 'LoanTerm', 'DTIRatio'],
                'records': [({
                    'Age': Age,
                    'Income': Income_USD,
                    'LoanAmount': LoanAmount_USD,
                    'CreditScore': CreditScore,
                    'MonthsEmployed': MonthsEmployed,
                    'LoanTerm': LoanTerm,
                    'DTIRatio': DTIRatio,
                }, prediction[0])],
            }
            context['application_result'] = "Congratulations, you qualify for a loan!" if prediction[0] == 0 else "Sorry, your application has been rejected."
    else:
        form = LoanForm()
    context['form'] = form
    return render(request, 'user/create-applicant.html', context)

@login_required
def view_profile(request):
     if request.user.is_authenticated:
        # User is authenticated, you can access the email attribute
        email = request.user.email
        username = request.user.username

        user = request.user

        hasPfp = user.image != ""


        if request.method == "POST":
            form = UpdateUserForm(request.POST, request.FILES)

            if form.is_valid():
                if user.image != form.cleaned_data["image"] and user.image != "":
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    imagePath = os.path.join(current_dir, '..', 'images', str(user.image))
                    os.remove(imagePath)

                user.first_name = form.cleaned_data["fname"]
                user.last_name = form.cleaned_data["lname"]
                user.username = form.cleaned_data["uname"]
                user.email = form.cleaned_data["email"]
                user.image = form.cleaned_data["image"]
                
                user.save()
                return redirect(view_profile)

        else:
            form = UpdateUserForm(initial={
                "fname": user.first_name,
                "lname": user.last_name,
                "uname": user.username,
                "email": user.email,
                "image": user.image,
            })

        return render(request, "user/profile.html", {
            "id": id, 
            "user": user.username,
            "fname": user.first_name,
            "lname": user.last_name,
            "email": user.email,
            "form": form,
            "image": user.image,
            "hasPfp": hasPfp,
        })
     
     else:
        return render(request, 'anonymousProfile.html')

@login_required
def delete_image(request):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        imagePath = os.path.join(current_dir, '..', 'images', str(request.user.image))
        os.remove(imagePath)
        request.user.image = ""
        request.user.save()


    except FileNotFoundError:
        print(FileNotFoundError)

    return redirect(view_profile)

def reset_password(request):
    return render(request, 'user/reset-password.html')

def aboutUs(request):
    return render(request, 'user/aboutUs.html')

@login_required
def remove_user(request):
    if request.method == "GET":
        user = request.user
        user.delete()

        redirect("home")
        
    return render(request, "user/remove-user.html")

def profile(request, id):
    try:
        user = CustomUser.objects.get(id=id)    
        position = ""

        if user.is_staff:
            position = "Staff"
        else:
            position = "User"    

        return render(request, "profile.html", {
                "id": id,
                "found": True,
                "fname": user.first_name,
                "lname": user.last_name,
                "usrnm": user.username,
                "email": user.email,
                "position": position,
            })
    
    except:
        return render(request, "profile.html", {"found": False, "msg": f"User id {id} not found"})
    
login_required
def update(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            form = UpdateUserForm(request.POST)

            if form.is_valid():
                user.first_name = form.cleaned_data["fname"]
                user.last_name = form.cleaned_data["lname"]
                user.email = form.cleaned_data["email"]

                user.save()
                return redirect('home')

        else:
            form = UpdateUserForm(initial={
                "fname": user.first_name,
                "lname": user.last_name,
                "email": user.email,
            })

        return render(request, "updateUser.html", {
            "found": False,
            "id": id, 
            "user": user.username,
            "fname": user.first_name,
            "lname": user.last_name,
            "email": user.email,
            "form": form,
        })

    else:
        return render(request, "anonymousProfile.html", {"found": False, "msg": f"User id {id} not found"})
    

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful')

                    if user.is_admin:
                        return redirect('predictions')
                    elif user.is_customer:
                        return redirect('create_applicant')
                    else:
                        msg = 'Invalid user role'
                else:
                    msg = 'User is not active'
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'

    return render(request, 'login.html', {'form': form, 'msg': msg})





@login_required
def profile(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # User is authenticated, you can access the email attribute
        email = request.user.email
        return render(request, 'profile.html', {'email': email})
    else:
        # User is not authenticated (anonymous), handle it accordingly
        return render(request, 'anonymousProfile.html')

@login_required
def applicants(request):
    if request.user.is_authenticated:
        applicants = LoanApplicant.objects.all()

        return render(request, 'admin/applicants.html', {
            "applicants": applicants,
        })

    return redirect(login)

def predictions(request):
    context = {'messages': []}

    if request.method == 'POST' and request.FILES['csv_file'] and 'selected_model' in request.POST:
        csv_file = request.FILES['csv_file']
        selected_model = request.POST['selected_model']

        try:
            model = select_model(selected_model)
        except FileNotFoundError as e:
            return HttpResponse(str(e))

        csv_data = read_csv_file(csv_file)
        csv_data, records_list = apply_label_encoders(csv_data)

        context['csv_data'] = {
            'headers': list(records_list[0].keys()),
            'records': records_list,
        }

        predictions_data = make_predictions(model, csv_data, records_list)

        context['predictions_data'] = {
            'headers': list(records_list[0].keys()),
            'records': predictions_data,
        }
        # Save to database with loan_id
        for record, prediction in zip(records_list, [prediction for _, prediction in predictions_data]):
            save_to_database([record], [prediction])

    # Get the list of available models for the dropdown
    context['available_models'] = get_available_models()

    return render(request, 'admin/predictions.html', context)


def performance(request):
    try:
        # Load the model
        model = joblib.load('loan_model.joblib')

        # Get the features used during training from the Django model
        features_used_in_training = [field.name for field in Applicant._meta.fields if field.name != 'id']

        # Get the test data from the Django model
        test_data = Applicant.objects.all().values(*features_used_in_training)

        # Create a DataFrame from the queryset
        test_data_df = pd.DataFrame.from_records(test_data, columns=features_used_in_training)

        # Ensure all columns are present (you may need to handle missing columns)
        missing_columns = set(features_used_in_training) - set(test_data_df.columns)

        # Drop missing columns
        test_data_df = test_data_df.drop(columns=missing_columns, errors='ignore')

        # Check for missing values in the test data
        print("Missing values in test data:")
        print(test_data_df.isnull().sum())

        # Print columns before handling missing columns
        print("Columns in test_data_df before handling missing columns:", test_data_df.columns)

        # Print other information
        print("Test Data DataFrame:")
        print(test_data_df)

        # Rename columns in the test_data_df to match the case in the training data
        test_data_df = test_data_df.rename(columns={'age': 'Age', 'car_ownership': 'Car_Ownership', 'current_house_years': 'Current_House_Years',
                                                    'current_job_years': 'Current_Job_Years', 'experience': 'Experience', 'house_ownership': 'House_Ownership',
                                                    'income': 'Income', 'marital_status': 'Marital_Status', 'profession': 'Profession'})

        # Apply label encoding for each categorical variable
        marital_status_encoder = LabelEncoder()
        house_ownership_encoder = LabelEncoder()
        car_ownership_encoder = LabelEncoder()
        profession_encoder = LabelEncoder()

        test_data_df['Marital_Status'] = marital_status_encoder.fit_transform(test_data_df['Marital_Status'])
        test_data_df['House_Ownership'] = house_ownership_encoder.fit_transform(test_data_df['House_Ownership'])
        test_data_df['Car_Ownership'] = car_ownership_encoder.fit_transform(test_data_df['Car_Ownership'])
        test_data_df['Profession'] = profession_encoder.fit_transform(test_data_df['Profession'])

        print("Columns before prediction:", test_data_df.columns)

        # Make predictions
        if 'risk_flag' not in test_data_df.columns:
            return render(request, 'performance.html', {'error': "'risk_flag' not found in the dataset"})

        # Print prediction input
        prediction_input = test_data_df.drop(['risk_flag', 'city', 'state','loan_id'], axis=1)
        print("Prediction Input:")
        print(prediction_input)

        test_prediction = model.predict(prediction_input)

        # Fetch 'Risk_Flag' values from the database
        Y_test = list(test_data_df['risk_flag'])

        # Handle NaN values in Y_test
        Y_test = np.nan_to_num(Y_test, nan=-1)  # Replace NaN with -1 or any other suitable value

        # Print statement before calculating accuracy
        print("Before calculating accuracy")

        # Calculate accuracy
        accuracy = accuracy_score(Y_test, test_prediction)
        # Print statement after calculating accuracy
        print("After calculating accuracy")

        # Calculate confusion matrix
        cm = confusion_matrix(Y_test, test_prediction)

        # Print for debugging
        print("Columns in test_data_df after handling missing columns:", test_data_df.columns)
        print("Accuracy:", accuracy)
        print("Confusion Matrix:", cm)

        # Pass values to the template
        context = {
            'accuracy': accuracy,
            'confusion_matrix': cm,
            'columns_after_missing_handling': test_data_df.columns.tolist()
        }

        # Print context data for debugging
        print("Context Data:", context)

        return render(request, 'admin/performance.html', context)

    except Exception as e:
        print("Error during prediction:", str(e))
        return render(request, 'admin/performance.html', {'error': f"Prediction error: {str(e)}"})


def reports(request):

    total_applications = Applicant.objects.count()
    approved_applications = Applicant.objects.filter(risk_flag=1).count()
    rejected_applications = Applicant.objects.filter(risk_flag=0).count()

    approval_rate = (approved_applications / total_applications) * 100 if total_applications > 0 else 0
    rejection_rate = (rejected_applications / total_applications) * 100 if total_applications > 0 else 0

    # Format approval and rejection rates with two decimal places
    approval_rate_formatted = "{:.2f}".format(approval_rate)
    rejection_rate_formatted = "{:.2f}".format(rejection_rate)

    data = Applicant.objects.values_list('risk_flag', flat=True)

    # Create a Plotly histogram
    fig = px.histogram(x=data, nbins=10, title='Distribution of approval rates',
                       labels={'x': 'risk_flag', 'y': 'Frequency'})

    fig.update_layout(xaxis=dict(tickvals=[0, 1]))
    fig.update_layout(height=300, width=400) 
    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Pass data to the HTML template
    #context = {'plot_html': plot_html}

    # Pass data to the HTML template
    context = {
        'total_applications': total_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'approval_rate': approval_rate_formatted,
        'rejection_rate': rejection_rate_formatted,
        'plot_html': plot_html,
    }

    return render(request, 'admin/reports.html', context)


def information(request):
    return render(request, 'admin/information.html')


def ask_openai(message):
    try:
        customPrompt = f"I am thinking of applying for a loan and {message}"
        response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=customPrompt,
        max_tokens=150,  
        temperature=0.7
    )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        print(f"Error in ask_openai: {e}")
        return "Sorry, I couldn't understand that."

def chat_assistance(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print('Received message:', message)
        response = ask_openai(message)
        print('Sending response:', response)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'user/chat-assistance.html')

def get_model_metadata(request):
    try:
        # Load the model
        model = joblib.load('loan_model.joblib')

        # Get the features used during training from the Django model
        features_used_in_training = [field.name for field in Applicant._meta.fields if field.name != 'id']

        # Get the test data from the Django model
        test_data = Applicant.objects.all().values(*features_used_in_training)

        # Create a DataFrame from the queryset
        test_data_df = pd.DataFrame.from_records(test_data, columns=features_used_in_training)

        # Ensure all columns are present (you may need to handle missing columns)
        missing_columns = set(features_used_in_training) - set(test_data_df.columns)

        # Drop missing columns
        test_data_df = test_data_df.drop(columns=missing_columns, errors='ignore')

        # Rename columns in the test_data_df to match the case in the training data
        test_data_df = test_data_df.rename(columns={'age': 'Age', 'car_ownership': 'Car_Ownership', 'current_house_years': 'Current_House_Years',
                                                    'current_job_years': 'Current_Job_Years', 'experience': 'Experience', 'house_ownership': 'House_Ownership',
                                                    'income': 'Income', 'marital_status': 'Marital_Status', 'profession': 'Profession'})

        # Apply label encoding for each categorical variable
        marital_status_encoder = LabelEncoder()
        house_ownership_encoder = LabelEncoder()
        car_ownership_encoder = LabelEncoder()
        profession_encoder = LabelEncoder()

        test_data_df['Marital_Status'] = marital_status_encoder.fit_transform(test_data_df['Marital_Status'])
        test_data_df['House_Ownership'] = house_ownership_encoder.fit_transform(test_data_df['House_Ownership'])
        test_data_df['Car_Ownership'] = car_ownership_encoder.fit_transform(test_data_df['Car_Ownership'])
        test_data_df['Profession'] = profession_encoder.fit_transform(test_data_df['Profession'])

        # Make predictions
        if 'risk_flag' not in test_data_df.columns:
            raise ValueError("'risk_flag' not found in the dataset")

        # Prepare prediction input
        prediction_input = test_data_df.drop(['risk_flag', 'city', 'state','loan_id'], axis=1)

        # Fetch 'Risk_Flag' values from the database
        Y_test = list(test_data_df['risk_flag'])

        # Handle NaN values in Y_test
        Y_test = np.nan_to_num(Y_test, nan=-1)  # Replace NaN with -1 or any other suitable value

        # Calculate accuracy
        accuracy = accuracy_score(Y_test, model.predict(prediction_input))

        # Calculate confusion matrix
        cm = confusion_matrix(Y_test, model.predict(prediction_input))

        # Return metadata as JSON
        metadata = {
            'accuracy': accuracy,
            'confusion_matrix': cm.tolist(),
            'success': True  # Flag indicating successful calculation
        }

        return JsonResponse(metadata)

    except Exception as e:
        # Return error message if an exception occurs
        error_message = f"Error during metadata calculation: {str(e)}"
        metadata = {'success': False, 'error': error_message}
        return JsonResponse(metadata)


class CustomPasswordResetView(AllauthPasswordResetView):
    template_name = 'custom_password_reset.html'  

    success_url = reverse_lazy('password_reset_done')  

    
class CustomPasswordResetDoneView(TemplateView):
    template_name = 'custom_password_reset_done.html'  
