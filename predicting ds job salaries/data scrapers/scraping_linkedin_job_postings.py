#!/usr/bin/env python
# coding: utf-8




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


jobs = []


def chromedriver_set_options(chromedriver_path, PROXYVAR):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--proxy-server=%s' % PROXYVAR)
    wd = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)
    
    return wd





def log_into_linkedin(username, password, wd):
    wd.get("https://www.linkedin.com/login")
    username_field = wd.find_element_by_id('username')
    username_field.clear()
    username_field.send_keys(username)
    password_field = wd.find_element_by_id('password')
    password_field.clear()
    password_field.send_keys(password)
    submit_button = wd.find_element_by_css_selector('button')
    submit_button.click()





def search_for_searchfield(wd):
    wd.implicitly_wait(10)
    try:
      search_field = wd.find_element_by_css_selector('.search-global-typeahead__input')
    except:
      if wd.title == 'Security Verification | LinkedIn':
        # LinkedIn is asking for a verification code. Check your email and input the code here
        code = input('Enter the verification code: ')
        verification_input = wd.find_element_by_css_selector('.input_verification_pin')
        verification_input.clear()
        verification_input.send_keys(code)
        submit_button = wd.find_element_by_id('email-pin-submit-button')
        submit_button.click()
        # Implicit wait already set to 10 seconds
        search_field = wd.find_element_by_css_selector('.search-global-typeahead__input')





def partially_extract_jobs_on_single_page(wd, search_url):
    
    index = 0
    result_list = []
    global jobs
    
    wd.get(search_url)

    while True:
        
        print('successfully partially scraped job # ' + str(index))
        job = {}
        time.sleep(1)    
        
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
            
            job = {"company": company, "title": title, "location": location, "href": url}
            jobs.append(job) 
        
        except:
            
            print('error partially scraping job # ' + str(index))
        
        if index >= len(result_list) - 1:
            break
        
        index = index + 1
        wd.execute_script("return arguments[0].scrollIntoView();", result_list[index]) 





##def partially_extract_jobs_on_subsequent_pages(num_of_pages, wd, search_url):
    
    ##if num_of_pages > 1:
        
        ##for i in range(1, num_of_pages):
            
            ##partially_extract_jobs_on_single_page(wd, search_url + '&start=' + str(i * 25))
        
            ##time.sleep(3)
            ##print('successfully partially scraped page # ' + str(i+1))

def partially_extract_jobs_on_subsequent_pages(num_of_pages, wd, search_url):
    
    if num_of_pages > 1:
        
        for i in range(1, num_of_pages):
            
            try:
            
                next_page_url = search_url[0:-3] + str(int(search_url[-3:]) + (i * 25))
            
            except:
                
                next_page_url = search_url + '&start=' + str(i * 25)
            
            partially_extract_jobs_on_single_page(wd, next_page_url)
        
            time.sleep(3)
            print('successfully partially scraped page # ' + str(i+1))




def fully_extract_jobs_on_all_pages(wd):
    
    global jobs
    
    for job in jobs:
        wd.get(job['href'])
  
  ## extracting salary estimate
        
        try:
            salary = wd.find_element_by_css_selector('.salary-main-rail__data-amount').text
            job['salary'] = salary

  ## setting salary to some default value if salary information is unavailable 

        except:
            print('no salary for job # ' + str(jobs.index(job)))
            continue
            #job['salary'] = -1
  
        try:
            description = wd.find_element_by_css_selector('.jobs-description-content__text').text
            job['description'] = description

        except:
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




def scraper(chromedriver_path, PROXYVAR, username, password, search_url, num_of_pages):
    
    wd = chromedriver_set_options(chromedriver_path, PROXYVAR)
    
    log_into_linkedin(username, password, wd)
    
    search_for_searchfield(wd)
    
    partially_extract_jobs_on_single_page(wd, search_url)
    
    partially_extract_jobs_on_subsequent_pages(num_of_pages, wd, search_url)
    
    fully_extract_jobs_on_all_pages(wd)
    
    df = pd.DataFrame(jobs)
    
    return df
    
    

