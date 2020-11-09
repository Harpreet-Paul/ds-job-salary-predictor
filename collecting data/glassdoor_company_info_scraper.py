#!/usr/bin/env python
# coding: utf-8




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time



## Scraping glassdoor company info for a list of companies, given by the company_names variable. 

def scrape_glassdoor_company_info(company_names):
    
    ## Initializing empty list to which company info for each comany will be appended. 
    
    all_companies_info = []
    
    ## Initializing the webdriver. 

    options = webdriver.ChromeOptions()
    wd = webdriver.Chrome(executable_path="C:/Users/harpr/Documents/GitHub/ds_salary_proj/data scrapers/chromedriver.exe", options=options)

    ## Telling the webdriver to navigate to the Glassdoor company reviews home page. 
    
    wd.get('https://www.glassdoor.ca/Reviews/index.htm')
    time.sleep(7)
    
    ## Clicking the sign-in button. 
    wd.find_element_by_link_text('Sign In').click()
    time.sleep(5)
    
    ## Passing the username and password to the sign-in dialogue box and clicking submit. 
    
    wd.find_element_by_name("username").send_keys('some username')
    time.sleep(2)
    wd.find_element_by_name("password").send_keys('some password')
    time.sleep(2)
    wd.find_element_by_name("submit").click()
    
    i = 1
    
    ## Iteratively scraping each company in company_names.

    for company in company_names:
        
        time.sleep(10)
        
        ## Initializing empty dictionary within which company info for each company will be stored. 
        
        company_info = {}
    
        
        ## Finding the company name search box and entering in the company name to be searched. 
        ## Two different possible HTML elements corresponding to the company name search box are searched for since the element inexplicably varies from instance to instance. 
        
        try:
            company_name_search_box = WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.ID, "sc.keyword")))
            time.sleep(2)
            company_name_search_box.clear()
            time.sleep(2)
            company_name_search_box.send_keys(company)
        except:
            company_name_search_box = WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.NAME, "sc.keyword")))
            time.sleep(2)
            company_name_search_box.clear()
            time.sleep(2)
            company_name_search_box.send_keys(company)
            
        ## Trying to clear the location search box.
               
        try:
            location_search_box = wd.find_element_by_xpath("//*[@id='sc.location']")
            time.sleep(2)
            location_search_box.clear()
        except:
            pass
        
        ## Clicking the search button to search for the entered company name. 
        
        search_button = wd.find_element_by_xpath('//*[@id="scBar"]/div/button')
        time.sleep(2)
        search_button.click() 
        
        ## Checking if searching for a company name leads to a page of multiple search results. 
    
        if wd.current_url.startswith('https://www.glassdoor.ca/Reviews'):
            
            ## If so, the first search result is clicked. 
        
            try:
                first_search_result = WebDriverWait(wd, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class = "single-company-result module "][1]//a[1]')))
                link = first_search_result.get_attribute('href')
                time.sleep(3)
                wd.get(link)
                
            ## If no results are found, then the company is skipped and the next company name is searched. 
        
            except:
                print (company + ' not found')
                continue
        
        ## At this point, we're on the company info page. 
        
        
        company_info['company'] = company
        
        ## Headquarters, company size, company type, industry, revenue, company rating, recommend to a friend rating, ceo approval and interview difficulty rating are scraped. 
        
        ## A default value of -1 is set for any unfound elements on the company info page. 
    
        try:
            headquarters = wd.find_element_by_xpath('//div[@class="infoEntity"][2]/span').text
            company_info['headquarters'] = headquarters
        except:
            company_info['headquarters'] = -1
            
        time.sleep(2)
        
        try:
            company_size = wd.find_element_by_xpath('//div[@class="infoEntity"][3]/span').text
            company_info['company_size'] = company_size
        except:
            company_info['company_size'] = -1
        
        time.sleep(2)
    
        try:
            company_type = wd.find_element_by_xpath('//div[@class="infoEntity"][5]/span').text
            company_info['company_type'] = company_type
        except:
            company_info['company_type'] = -1
            
        time.sleep(2)
    
        try:
            industry = wd.find_element_by_xpath('//div[@class="infoEntity"][6]/span').text
            company_info['industry'] = industry
        except:
            company_info['industry'] = -1
            
        time.sleep(2)
    
        try:
            revenue = wd.find_element_by_xpath('//div[@class="infoEntity"][8]/span').text
            company_info['revenue'] = revenue
        except:
            company_info['revenue'] = -1
            
        time.sleep(2)
    
        try:
            company_rating = wd.find_element_by_xpath('//*[@id="EmpStats"]/div/div[1]/div/div/div').text
            company_info['company_rating'] = company_rating
        except:
            company_info['company_rating'] = -1
    
        time.sleep(2)
    
        try:
            recommend_to_a_friend = wd.find_element_by_id("EmpStats_Recommend").get_attribute('data-percentage')
            company_info['recommend_to_a_friend'] = recommend_to_a_friend
        except:
            company_info['recommend_to_a_friend'] = -1
        
        time.sleep(2)
        
        try:
            ceo_approval = wd.find_element_by_id("EmpStats_Approve").get_attribute('data-percentage')
            company_info['ceo_approval'] = ceo_approval
        except:
            company_info['ceo_approval'] = -1
    
        time.sleep(2)
        
        try:
            interview_difficulty = wd.find_element_by_class_name('difficultyLabel').text
            company_info['interview_difficulty'] = interview_difficulty
        except:
            company_info['interview_difficulty'] = -1
            
        ## Dictionary of company info for a particular company is appended to the all_companies_info list. 
        
        all_companies_info.append(company_info)
        
        print ("finished scraping company # " + str(i))
        
        i += 1
        
        ## Navigating back to the company search page. 
        
        wd.back()
        
        wd.implicitly_wait(5)
        
        if wd.current_url.startswith('https://www.glassdoor.ca/Reviews'):
            
            wd.back()
        
    df = pd.DataFrame(all_companies_info)
        
    return df


    
    







