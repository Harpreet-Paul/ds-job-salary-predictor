# Data Science Job Salary Predictor

## Background

The data science job salary predictor is a web application that allows data science job seekers to input information from a job posting and receive a salary estimate for the position. The motivation for building this app was to give job seekers a tool they could use to better negotiate salaries for future positions, knowing what these positions were worth. 

## How to Use

| :point_right:        | **Access the app here:** [Job Salary Predictor](http://34.124.114.236/)   |
|---------------|:------------------------|

Note: The job salary predictor is only usable with job postings from the US, Canada, Scotland, Ireland or England.

## Deployment

This github repository was cloned into a VM instance on Google Cloud Platform. The app.py file is running on the VM and is accessible to other users through the external IP address of the VM.

## Learn More

Please see the [`collecting data.ipynb`](https://github.com/Harpreet-Paul/ds-job-salary-predictor/blob/master/collecting%20data/collecting%20data.ipynb), [`cleaning data.ipynb`](https://github.com/Harpreet-Paul/ds-job-salary-predictor/blob/master/cleaning%20and%20modelling%20data/cleaning%20data.ipynb) and [`modelling data.ipynb`](https://github.com/Harpreet-Paul/ds-job-salary-predictor/blob/master/cleaning%20and%20modelling%20data/modelling%20data.ipynb) notebooks for details on the data collection, data cleaning and data modelling steps respectively.

## Acknowledgements

Credit to Daniel Fredriksen for providing most of the source code for the linkedin job scraper `scraping_linkedin_job_postings.py` .

## Key Repository Contents
* cleaning and modelling data
  * `cleaning data.ipynb` : notebook detailing data cleaning process
  * `modelling data.ipynb` : notebook detailing data modelling process
* collecting data
  * `collecting data.ipynb` : notebook detailing data collection process
  * `glassdoor_company_info_scraper.py` : module for the glassdoor company info scraper
  * `scraping_linkedin_job_postings.py` : module for the linkedin job posting scraper
* pickle objects
* static
  * `home_page.css` : CSS file for app home page
* templates
  * `home_page_html` : HTML template for app home page
* `app.py` : main flask app
* `requirements.txt` : dependencies for the app
