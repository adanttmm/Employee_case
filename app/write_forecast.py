#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:35:31 2023

@author: adan
"""

import psycopg2
import pandas as pd
from datetime import datetime
import tensorflow as tf
import pmdarima as pm
import pickle 
from sqlalchemy import create_engine

# Database connection parameters
db_params = {
    "database": "employee_case",
    "user": "nim_grav",
    "password": "nimble_grtavity_usecase",
    "host": "localhost",  
    "port": "5432",       
}

# Connect to employee_case database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

cursor.execute('SELECT * FROM emp_api.production_supervision_ratio')
obs_series = cursor.fetchall()

last_date_str = obs_series[-1][0]
date_str = last_date_str.split()[1] + ' ' + last_date_str.split()[0] + ' 01'
date_format = '%Y %B %d'
last_date = datetime.strptime(date_str, date_format)
idx = pd.date_range(last_date,periods = 25,freq='M')

# Write women in government forecast
filename = './women_gov_employee_final_model.pkl'
women_gov_employee_forecast = pickle.load(open(filename, 'rb'))

fitted = women_gov_employee_forecast.predict(n_periods=24)
fitted_series = pd.Series(fitted)
sarima_fcast = pd.DataFrame([fitted_series]).transpose().reset_index()
sarima_fcast.columns = ['date_series','forecast']
sarima_fcast.date_series = idx[1:]

engine = create_engine('postgresql+psycopg2://adanttmm:nimble_grtavity_usecase@localhost:5432/employee_case')

sarima_fcast.to_sql('women_in_government_forecast', 
                    engine,
                    schema='emp_api',
                    if_exists='append', 
                    index=False)

# Write production-supervision ratio forecast
obs_series_df = pd.DataFrame(obs_series)

filename = './production_supervision_ratio_final_model.h5'
conv1D_forecast = tf.keras.models.load_model(filename)

conv_preds = tf.squeeze(conv1D_forecast.predict(tf.constant(obs_series_df.iloc[-120:,1].to_numpy(),shape=(1,1,120))))
conv_df = pd.DataFrame()
conv_df.date_series = idx[1:]
conv_df.forecast = conv_preds
conv_preds.to_sql('production_supervision_forecast', 
                  engine,
                  schema='emp_api',
                  if_exists='append',
                  index=False)



