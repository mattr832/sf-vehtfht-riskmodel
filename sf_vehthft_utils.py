#!/usr/bin/env python
# coding: utf-8

import pickle
import scipy.stats as ss
from sf_vehthft_helperfuns import *


def get_risk(sample):
    # extract time related features for model
    datetime = sample['Time']
    hour = get_hour(sample['Time'])
    dayoweek = get_dow(sample['Time'])
    fdayoweek = get_fdow(sample['Time'])
    lat = float(sample['Latitude'])
    long = float(sample['Longitude'])

    # get coordinates from json and convert to df for feeding to model
    df = pd.DataFrame(sample, index=[0])
    df = df[['Latitude','Longitude']]
  
    # load the label encoders from disk
    pdistrict_labenc = pickle.load(open('pdistrict_labenc.pkl', 'rb'))
    sdistrict_labenc = pickle.load(open('sdistrict_labenc.pkl', 'rb'))
    hood_labenc = pickle.load(open('hood_labenc.pkl', 'rb'))
    inter_labenc = pickle.load(open('inter_labenc.pkl', 'rb'))

    # load the preprocessing models from disk
    pdistrict_knn = pickle.load(open('pdistrict_knn.pkl', 'rb'))
    sdistrict_lgbm = pickle.load(open('sdistrict_lgbm.pkl', 'rb'))
    hood_knn = pickle.load(open('hood_knn.pkl', 'rb'))
    inter_knn = pickle.load(open('inter_knn.pkl', 'rb'))

    # get preprocess predictions
    pdresult = pdistrict_knn.predict(df)
    sdresult = sdistrict_lgbm.predict(df)
    hresult = hood_knn.predict(df)
    iresult = inter_knn.predict(df)

    # convert predictions to preprocessed labels
    pdistrict = pdistrict_labenc.inverse_transform(pdresult)
    sdistrict = sdistrict_labenc.inverse_transform(sdresult)
    hood = hood_labenc.inverse_transform(hresult)
    inter = inter_labenc.inverse_transform(iresult)

    # get mappings from dics in helper_funs
    isection = inter[0]
    isection_te = inter_te.get(isection)
    nvt_te = NVT_TE.get(isection)
    burg_te = burglary_te.get(isection)

    # convert all preprocess features to df
    df = pd.DataFrame({'Incident_Hour': hour,
                 'Incident_Day_of_Week': dayoweek,
                 'Police_District': pdistrict,
                 'Analysis_Neighborhood': hood,
                 'Supervisor_District': sdistrict,
                 'Inter_TE': isection_te,
                 'NVT_TE': nvt_te,
                 'Burglary_TE': burg_te})

    # one hot encode the categorical features
    df2 = pd.DataFrame(df)
    
    for c in catvars:
        df2[catvars] = df2[catvars].astype('category')

    # score the df row
    vthft_model = pickle.load(open('vthft_model.pkl', 'rb'))
    prob = vthft_model.predict_proba(df2)[:,1]
    score = round(ss.percentileofscore(list(probs), prob, kind='strict'))

    # classify the risk score into risk levels based on quartile cutoff vals
    if score > 80:
        x = 'Very High'
    elif score > 60 and score <= 80:
        x = 'High'
    elif score > 40 and score <= 60:
        x = 'Medium'
    elif score > 20 and score <= 40:
        x = 'Low'
    else:
        x = 'Very Low'

     # convert all preprocess features to df for 3 hour advance risk score
    hour2 = hour + 3
    if hour2 > 23:
        newhour = hour2 - 24
    else:
        newhour = hour2
    
    if hour2 > 23:
        day = fdayoweek
    else:
        day = dayoweek
    
    df3 = pd.DataFrame({'Incident_Hour': newhour,
                 'Incident_Day_of_Week': day,
                 'Police_District': pdistrict,
                 'Analysis_Neighborhood': hood,
                 'Supervisor_District': sdistrict,
                 'Inter_TE': isection_te,
                 'NVT_TE': nvt_te,
                 'Burglary_TE': burg_te})

    # one hot encode the categorical features
    df4 = pd.DataFrame(df3)
    
    for c in catvars:
        df4[catvars] = df4[catvars].astype('category')

    # score the df row
    prob2 = vthft_model.predict_proba(df4)[:,1]
    score2 = round(ss.percentileofscore(list(probs), prob2, kind='strict'))

    # classify the risk score into risk levels based on quartile cutoff vals
    if score2 > 80:
        x2 = 'Very High'
    elif score2 > 60 and score2 <= 80:
        x2 = 'High'
    elif score2 > 40 and score2 <= 60:
        x2 = 'Medium'
    elif score2 > 20 and score2 <= 40:
        x2 = 'Low'
    else:
        x2 = 'Very Low'
        
    response = {'Risk Score': score, 
               'Risk Level': x,
               '3+ Hour Risk Score': score2,
               '3+ Hour Risk Level': x2,
               'DateTime': datetime,
               'Latitude': lat,
               'Longitude': long,
               'Neighborhood': hood[0],
               'Intersection':  inter[0]
              }
    return response

