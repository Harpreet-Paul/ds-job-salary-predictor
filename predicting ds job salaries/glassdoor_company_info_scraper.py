#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


# In[ ]:


def scrape_glassdoor_company_info(company_names):
    
    all_companies_info = []

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument('window-size=1920x1080')
    #options.add_argument('--proxy-server=%s' % PROXYVAR)
    wd = webdriver.Chrome(executable_path="/Users/isabellanguyen/predicting ds job salaries/chromedriver", options=options)

    wd.get('https://www.glassdoor.ca/Reviews/index.htm')
    wd.find_element_by_link_text('Sign In').click()
    wd.find_element_by_name("username").send_keys('harpreet.s.paul@outlook.com')
    wd.find_element_by_name("password").send_keys('happy23!')
    wd.find_element_by_name("submit").click()
    
    i = 1

    for company in company_names:
        
        company_info = {}
    
        #try:
            #try:
                #company_name_search_box = wd.find_element_by_id("sc.keyword")
            #except:
                #company_name_search_box = wd.find_element_by_name("sc.keyword")
        #except:
            #company_name_search_box = wd.find_element_by_xpath("//*[@id='sc.keyword']")
            
        try:
            company_name_search_box = WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.ID, "sc.keyword")))
            company_name_search_box.clear()
            company_name_search_box.send_keys(company)
        except:
            company_name_search_box = WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.NAME, "sc.keyword")))
            company_name_search_box.clear()
            company_name_search_box.send_keys(company)
            
               
        #company_name_search_box.clear()

        #company_name_search_box.send_keys(company)
        
        try:
            location_search_box = wd.find_element_by_xpath("//*[@id='sc.location']")
            location_search_box.clear()
        except:
            pass
        
        search_button = wd.find_element_by_xpath('//*[@id="scBar"]/div/button')
        search_button.click() 
    
        if wd.current_url.startswith('https://www.glassdoor.ca/Reviews'):
        
            try:
                first_search_result = WebDriverWait(wd, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class = "single-company-result module "][1]//a[1]')))
                link = first_search_result.get_attribute('href')
                wd.get(link)
        
            except:
                print (company + ' not found')
                continue
        
        company_info['company'] = company
    
        try:
            headquarters = wd.find_element_by_xpath('//div[@class="infoEntity"][2]/span').text
            company_info['headquarters'] = headquarters
        except:
            company_info['headquarters'] = -1
        
        try:
            company_size = wd.find_element_by_xpath('//div[@class="infoEntity"][3]/span').text
            company_info['company_size'] = company_size
        except:
            company_info['company_size'] = -1
    
        try:
            company_type = wd.find_element_by_xpath('//div[@class="infoEntity"][5]/span').text
            company_info['company_type'] = company_type
        except:
            company_info['company_type'] = -1
    
        try:
            industry = wd.find_element_by_xpath('//div[@class="infoEntity"][6]/span').text
            company_info['industry'] = industry
        except:
            company_info['industry'] = -1
    
        try:
            revenue = wd.find_element_by_xpath('//div[@class="infoEntity"][7]/span').text
            company_info['revenue'] = revenue
        except:
            company_info['revenue'] = -1
    
        try:
            company_rating = wd.find_element_by_xpath('//*[@id="EmpStats"]/div/div[1]/div/div/div').text
            company_info['company_rating'] = company_rating
        except:
            company_info['company_rating'] = -1
    
        try:
            recommend_to_a_friend = wd.find_element_by_id("EmpStats_Recommend").get_attribute('data-percentage')
            company_info['recommend_to_a_friend'] = recommend_to_a_friend
        except:
            company_info['recommend_to_a_friend'] = -1
        
        try:
            ceo_approval = wd.find_element_by_id("EmpStats_Approve").get_attribute('data-percentage')
            company_info['ceo_approval'] = ceo_approval
        except:
            company_info['ceo_approval'] = -1
    
        try:
            interview_difficulty = wd.find_element_by_class_name('difficultyLabel').text
            company_info['interview_difficulty'] = interview_difficulty
        except:
            company_info['interview_difficulty'] = -1
        
        all_companies_info.append(company_info)
        
        print ("finished scraping company # " + str(i))
        
        i += 1
        
        wd.back()
        
        wd.implicitly_wait(5)
        
        if wd.current_url.startswith('https://www.glassdoor.ca/Reviews'):
            
            wd.back()
        
    df = pd.DataFrame(all_companies_info)
        
    return df


    
    







