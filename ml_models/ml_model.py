# -*- coding: utf-8 -*-
"""VCYou_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CUroxnmcVaUYeZ_0lniU4n5vFy2G4tVu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def GenerateJobLib():
    # Load data
    file_name = "/content/big_startup_secsees_dataset.csv"
    startup_raw = pd.read_csv(file_name)
    startup_raw.info()
    print("\n")

    # Data Cleaning and Processing
    startup = startup_raw.dropna().query("funding_total_usd != '-' ")
    startup['funding_total_usd'] = startup['funding_total_usd'].astype(float)

    # Formatting date columns
    startup['founded_at'] = pd.to_datetime(startup['founded_at'], format='%Y-%m-%d', errors='coerce')
    startup['first_funding_at'] = pd.to_datetime(startup['first_funding_at'], format='%Y-%m-%d', errors='coerce')
    startup['last_funding_at'] = pd.to_datetime(startup['last_funding_at'], format='%Y-%m-%d', errors='coerce')

    # Dropping rows with NA values
    startup = startup.dropna()
    startup.info()

    # Analysis of funding dates
    print(startup['founded_at'].dt.year.unique() >= 2023, '\n\n',
        startup['first_funding_at'].dt.year.unique() >= 2023, '\n\n',
        startup['last_funding_at'].dt.year.unique() >= 2023, '\n\n',
        startup['last_funding_at'].dt.year.unique())

    # Sorting by last funding date
    startup.sort_values('last_funding_at', ascending=False)

    # Correcting date anomalies
    startup['last_funding_at'] = startup['last_funding_at'].replace('21050501', '20150501')

    # Text processing
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(startup['category_list'])

    # Clustering
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=100)
    kmeans.fit(X)
    startup['category_cluster'] = kmeans.labels_

    # Filtering and preparing data for analysis
    startup_prep = startup.query("status == 'ipo' or status == 'closed'")
    startup_prep['status'] = startup_prep['status'].replace({'acquired': 1, 'ipo': 1, 'closed': 0})

    # Calculating funding period
    startup_prep['funding_period_year'] = (startup_prep['last_funding_at'] - startup_prep['first_funding_at']) / pd.Timedelta(days=365.25)
    startup_prep['funding_period_year'] = startup_prep['funding_period_year'].round(1)

    # Preparing data for modeling
    startup_modeling = startup_prep[['status', 'funding_rounds', 'funding_period_year', 'funding_total_usd', 'category_cluster']]
    X = startup_modeling.iloc[:, 1:]
    y = startup_modeling.iloc[:, 0]

    # Splitting the dataset
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    # SVM Model Training
    from sklearn.model_selection import GridSearchCV
    from sklearn.svm import SVC
    from sklearn.metrics import classification_report

    svm = SVC(kernel='poly', degree=4)
    svm = svm.fit(X_train, y_train)

    # Hyperparameter tuning with GridSearchCV
    svm_param = {
        'C': list(range(0, 11)),
        'kernel': ['rbf', 'poly'],
        'degree': [3, 4]
    }
    svm_model = SVC()
    svm_grid = GridSearchCV(svm_model, param_grid=svm_param, cv=5, n_jobs=-1)
    svm_grid.fit(X_train, y_train)

    # Best hyperparameters
    print("Best hyperparameters:", svm_grid.best_params_)
    print("Best cross-validated score:", svm_grid.best_score_)

    # Evaluating the model
    best_model = svm_grid.best_estimator_
    y_predict_1 = svm.predict(X_test)
    y_predict_2 = best_model.predict(X_test)
    print(classification_report(y_test, y_predict_1), classification_report(y_test, y_predict_2))

    from joblib import dump
    dump(best_model, 'VCYou.joblib')

def ExecuteJobLib(funding_rounds, funding_period_year, funding_USD, category):
    from joblib import load
    import pandas as pd
    
    # Load the trained model
    best_model = load('VCYou.joblib')

    # Define your custom input data
    feature_values = np.array([[funding_rounds, funding_period_year, funding_USD, category]])  # Your example input

    # Assuming these are your feature names
    feature_names = ['funding_rounds', 'funding_period_year', 'funding_total_usd', 'category_cluster']

    # Create a DataFrame for the custom data
    feature_values_df = pd.DataFrame(feature_values, columns=feature_names)

    # Use the model to predict using DataFrame
    prediction = best_model.predict(feature_values_df)

    print("Prediction:", prediction)

    return prediction
