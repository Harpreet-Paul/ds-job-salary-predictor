#!/usr/bin/env python
# coding: utf-8

############ This is where the Flask web app is defined. This .py file will be run on the google cloud virtual machine. ############


import pickle
import numpy as np
import pandas as pd
import flask

## Loading in the model pipeline.

gb_pipeline = pickle.load(open("pickle objects/gb_pipeline.pkl", "rb"))

## Instantiating a flask object with the 'template_folder' parameter defining where to retrieve the homepage HTML template that will be rendered when get/post requests are made at the specified URL. 

app = flask.Flask(__name__, template_folder='templates')

## Specifying which URL and which HTTP methods will trigger the 'main' function. 

@app.route('/', methods=['GET', 'POST'])

## Defining the function that will be triggered at the specified URL.

def main():
    
    ## When a 'get' request is made, the app homepage is rendered, which contains a form through which the user can submit the parameters needed to make a salary prediction. 
    
    if flask.request.method == 'GET':
        return(flask.render_template('home_page_html', prediction = ''))

    ## When a 'post' request is made, ie. when the user submits the form needed to make a salary estimate, the 'predict' method of the model pipeline will be called on the passed in parameters and a salary estimate will be returned to the user. 
    
    if flask.request.method == 'POST':
        
        ## Initializing variables with the inputted form values. 
        
        description = flask.request.form['description']
        
        company_size = flask.request.form['company_size']
        
        company_type = flask.request.form['company_type']
      
        industry = flask.request.form['industry']
    
        revenue = flask.request.form['revenue']
        
        company_rating = flask.request.form['company_rating']
        
        recommend_to_a_friend = flask.request.form['recommend_to_a_friend']
        
        ceo_approval = flask.request.form['ceo_approval']
        
        interview_difficulty = flask.request.form['interview_difficulty']
        
        location_bin = flask.request.form['location_bin']
        
                                          
        data = [description, company_size, company_type, industry, revenue, company_rating, recommend_to_a_friend, ceo_approval, interview_difficulty, location_bin]
        
        ## Subbing an unknown feature values with np.nan so they can be imputed by the SimpleImputer transformer of the modelling pipeline. 
        
        for feature in data:
            if feature == 'Unknown':
                feature = np.nan
        
        ## Storing user submitted parameters in a df. 
            
        data_array = np.array(data).reshape(1,-1)
        df = pd.DataFrame(data_array, columns = ['description', 'company_size', 'company_type', 'industry',
       'revenue', 'company_rating', 'recommend_to_a_friend', 'ceo_approval',
       'interview_difficulty', 'location_bin'])
        
        ## Calling 'predict' method of model pipeline on submitted parameters to get a salary prediction. 
                                          
        prediction = gb_pipeline.predict(df)
        prediction = "$" + str(round(prediction[0])) + " USD/Year"
        
        ## Rendering the same homepage HTML template but with the salary estimate returned to the user. 
        
        return(flask.render_template('home_page_html', prediction = prediction))
        
       
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

## Setting host to 0.0.0.0 tells the operating system to listen on all public IPs (makes the app accessible to other users through the external IP of the GCP VM instance). 
