#!/usr/bin/env python
# coding: utf-8




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


## Initializing the empty list to which scraped job search results will be appended. 

jobs = []


## Initializing webdriver 

def chromedriver_set_options(chromedriver_path, PROXYVAR):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--proxy-server=%s' % PROXYVAR)
    wd = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)
    
    return wd


def log_into_linkedin(username, password, wd):
    
    ## Telling the webdriver to navigate to the Linkedin login page
    
    wd.get("https://www.linkedin.com/login")
    
    ## Webdriver enters the username and password and then clicks login
    
    username_field = wd.find_element_by_id('username')
    username_field.clear()
    username_field.send_keys(username)
    password_field = wd.find_element_by_id('password')
    password_field.clear()
    password_field.send_keys(password)
    submit_button = wd.find_element_by_css_selector('button')
    submit_button.click()



## Telling the webdriver to check if Linkedin is requesting security verification.
## If so, the user inputs the verification code recieved in their email and the webdriver submits this code to the verification page. 

def search_for_searchfield(wd):
    wd.implicitly_wait(10)
    try:
      search_field = wd.find_element_by_css_selector('.search-global-typeahead__input')
    except:
      if wd.title == 'Security Verification | LinkedIn':
        code = input('Enter the verification code: ')
        verification_input = wd.find_element_by_css_selector('.input_verification_pin')
        verification_input.clear()
        verification_input.send_keys(code)
        submit_button = wd.find_element_by_id('email-pin-submit-button')
        submit_button.click()
        search_field = wd.find_element_by_css_selector('.search-global-typeahead__input')


## Telling the webdriver to scrape partial info for each job found in the results list of the first page of search results for a job search. 

def partially_extract_jobs_on_single_page(wd, search_url):
    
    index = 0
    result_list = []
    global jobs
    
    ## Telling the webdriver to navigate to the first page of search results for a job search. 
    
    wd.get(search_url)

    while True:
        
        print('successfully partially scraped job # ' + str(index))
        job = {}
        time.sleep(1) 
        
        ## Webdriver finds the results list and then scrapes the company name, job title, location and href for each result.
        
        try:
            result_list = wd.find_elements_by_css_selector('.job-card-list--underline-title-on-hover')
            item = result_list[index]
            
            company_element = item.find_element_by_css_selector('.job-card-container__company-name')
            company = company_element.text
                 
            title_element = item.find_element_by_css_selector('.job-card-list__title')
            title = title_element.text
            
            location_element = item.find_element_by_css_selector('.artdeco-entity-lockup__caption')
            location = location_element.text
            
            url_element = item.find_element_by_css_selector('.job-card-container__link')
            url = url_element.get_attribute('href')
            
            ## The information for each result is stored in a dictionary and each dictionary is stored within the jobs list. 
            
            job = {"company": company, "title": title, "location": location, "href": url}
            jobs.append(job) 
        
        except:
            
            print('error partially scraping job # ' + str(index))
        
        if index >= len(result_list) - 1:
            break
        
        index = index + 1
        wd.execute_script("return arguments[0].scrollIntoView();", result_list[index]) 

        
## Now, the webdriver scrapes the results from subsequent pages in the job search.

def partially_extract_jobs_on_subsequent_pages(num_of_pages, wd, search_url):
    
    if num_of_pages > 1:
        
        for i in range(1, num_of_pages):
            
            try:
            
                next_page_url = search_url[0:-3] + str(int(search_url[-3:]) + (i * 25))
            
            except:
                
                next_page_url = search_url + '&start=' + str(i * 25)
                
            ## The partially_extract_jobs_on_single_page function is called on the URLs corresponding to the subsequent pages.
            ## Results from subsequent pages are also appended onto the jobs list. 
            
            partially_extract_jobs_on_single_page(wd, next_page_url)
        
            time.sleep(3)
            print('successfully partially scraped page # ' + str(i+1))


## Scraping the job description and other information for each search result from the job search by navigating to the unique URL for each job posting.            

def fully_extract_jobs_on_all_pages(wd):
    
    global jobs
    
    ## Telling the webdriver to go to the URLs corresponding to each job posting within the jobs list.
    
    for job in jobs:
        wd.get(job['href'])
        
    ## Once on the unique page for each job posting, the webdriver scrapes the salary estimate, job description, skills list (job requirements) and job details (position seniority, e.g. entry level, etc.).
    
    ## All the new elements listed above are simply added as additional key-value pairs into the already existing dictionary of information for each job posting.
        
        try:
            salary = wd.find_element_by_css_selector('.salary-main-rail__data-amount').text
            job['salary'] = salary
            
        ## If the salary element is not found on the webpage, then the remaining info is not scraped and the webdriver goes to the URL corresponding to the next job posting. 

        except:
            print('no salary for job # ' + str(jobs.index(job)))
            continue
  
        try:
            description = wd.find_element_by_css_selector('.jobs-description-content__text').text
            job['description'] = description

        except:
            
            ## A default value of -1 is set for unfound web elements. 
            
            job['description'] = -1

        try:
            skills_list = []
            for skill in wd.find_elements_by_xpath(".//div[@id='job-details']//li"):
                skills_list.append(skill.get_attribute('innerHTML'))
            job['skills'] = skills_list

        except:
            job['skills'] = -1

        try:
            details = wd.find_element_by_class_name('jobs-description-details').text
            job['details'] = details

        except:
            job['details'] = -1

        print('successfully fully scraped job # ' + str(jobs.index(job)))


## Wrapping all the helper functions under the main 'scraper' function. 

def scraper(chromedriver_path, PROXYVAR, username, password, search_url, num_of_pages):
    
    wd = chromedriver_set_options(chromedriver_path, PROXYVAR)
    
    log_into_linkedin(username, password, wd)
    
    search_for_searchfield(wd)
    
    partially_extract_jobs_on_single_page(wd, search_url)
    
    partially_extract_jobs_on_subsequent_pages(num_of_pages, wd, search_url)
    
    fully_extract_jobs_on_all_pages(wd)
    
    ## The scraped information, which exists as a list of dictionaries, is converted into a df. 
    
    df = pd.DataFrame(jobs)
    
    return df
    
    

