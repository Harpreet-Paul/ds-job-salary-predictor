#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import numpy as np
import pandas as pd
import flask


# In[ ]:


gb_pipeline = pickle.load(open("pickle objects/gb_pipeline.pkl", "rb"))


# In[ ]:



app = flask.Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])



def main():
    
    if flask.request.method == 'GET':
        return(flask.render_template('home_page_html', prediction = ''))

    
    if flask.request.method == 'POST':
        
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
        
        for feature in data:
            if feature == 'Unknown':
                feature = np.nan
            
        data_array = np.array(data).reshape(1,-1)
        df = pd.DataFrame(data_array, columns = ['description', 'company_size', 'company_type', 'industry',
       'revenue', 'company_rating', 'recommend_to_a_friend', 'ceo_approval',
       'interview_difficulty', 'location_bin'])
                                          
        prediction = gb_pipeline.predict(df)
        prediction = "$" + str(round(prediction[0])) + " USD/Year"
        
        return(flask.render_template('home_page_html', prediction = prediction))
        
       
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

