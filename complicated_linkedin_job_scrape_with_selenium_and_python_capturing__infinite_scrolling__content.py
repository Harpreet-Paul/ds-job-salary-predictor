# -*- coding: utf-8 -*-
"""Complicated LinkedIn Job Scrape with Selenium and Python - Capturing "Infinite Scrolling" content.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sJ_xsdzZanrZk8cqpOy3MCHPjsIazYxF

# LinkedIn Job Scrape with Selenium and Python

There has been a lot of discussion over the difficulty of accessing the LinkedIn job search results in an automated fashion. This notebook will show you how to use Selenium to connect to LinkedIn and scrape the data you need. Note that most website terms of service forbids this for commercial purposes, but typically does not mind against low bandwidth scraping for personal use. Review website terms of services before using Selenium to scrape any content to be sure you are not violating them by doing so...

Start by installing the Selenium dependencies and chromium-chromedriver so that we can use Selenium with a "headless" browser (refers to a browser without a user interface, IE no monitor to display the browser graphically).

The following commands are used on a Linux operating system, and will need to be modified if you are installing Selenium locally on a Windows OS (or Mac OS) instead of running Selenium via Colabs.
"""

!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

"""After running the cell, you may have a deprecation warning. You can ignore this for now. The deprecation warning indicates that they are changing the way ChromeOptions will be used for future versions. In the next cell, we add some setup options to indicate that we will be running headless Chromium (the development/open-source version of Chrome that is Google's base for commercial Chrome)"""

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

"""Next we navigate to the LinkedIn homepage."""

wd.get("https://www.linkedin.com/login")
print(wd.title)

"""Expected output: 

    LinkedIn Login, Sign in | LinkedIn

This is the title of the LinkedIn homepage.

Next we will use CSS selectors to focus on the login input fields, enter a username and password, and then submit the form to automate logging in. You will be prompted for a LinkedIn username and password. It is recommended to use a dummy account in case you make a programming mistake and cause LinkedIn to block your account due to abuse.

Elements are selected using the Selenium Webdriver find_element_by_xxx methods. You can read about them here: https://selenium-python.readthedocs.io/locating-elements.html. You can determine the selector for the element you wish to target by navigating to the page using your browser, right clicking on the element and selecting "Inspect Element" on most browsers (Chrome, Firefox, Edge...). This will bring up a dynamic HTML view of the element you are inspecting. Look for attributes like `id` or `class`. You can learn more about using css selectors (obtained from the class attribute) here: https://www.w3schools.com/cssref/css_selectors.asp

Next, we attempt to access the search field that is present on the LinkedIn homepage after logging in.

This block sets a 10 second timeout limit and polls for the existence of the search field. If the field isn't found, it checks the title of the page to determine if a security verification check is required. If so, it will prompt the user to enter the PIN that LinkedIn will forward to the users email, and then fills out the form. After the form is filled out, it checks again for the search field.

If the search field cannot be found and the page title does not indicate a security check is requested, there could be another page being displayed (usually asking to confirm a phone number or something similar). To resolve this, manually log into the browser and clear the screen, then rerun the code from the beginning. Note - if LinkedIn is asking you to confirm you are not a robot, then they will likely start blocking the account if it continues to scrape at the same rate soon.
"""

username = input('Enter your LinkedIn username: ')
password = input ('Enter your LinkedIn password: ')
username_field = wd.find_element_by_id('username')
username_field.clear()
username_field.send_keys(username)
password_field = wd.find_element_by_id('password')
password_field.clear()
password_field.send_keys(password)
submit_button = wd.find_element_by_css_selector('button')
submit_button.click()

wd.save_screenshot('test2.png')
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

"""Create a new jobs list, and define a function that extracts the job results that are on the page. This function will be used in the next cell.

The function takes a list of result elements, and then iterates over the list. It uses webdriver selectors to select HTML children in the list and save the text results to a job dictionary, that is then appended to the job list. The job data here excludes the more detailed description, skill list, and industries but obtains the URL for the job posting so that we can extract additional data at a later time
"""

import time
jobs = []
def extract_jobs_on_page():  
  index = 0
  result_list = []
  global jobs

  while True:    
    print('Scraping job #' + str(index))
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
      posted_element = item.find_element_by_css_selector('.job-card-container__listed-time')
      posted = posted_element.get_attribute('datetime')
      url_element = item.find_element_by_css_selector('.job-card-container__link')
      url = url_element.get_attribute('href')
      job = {
        "company": company,
        "title": title,
        "location": location,
        "posted": posted,
        "href": url
      }
      jobs.append(job) 
    except:
      print('Error on job # ' + str(index))
    if index >= len(result_list) - 1:
      break
    index = index + 1
    wd.execute_script("return arguments[0].scrollIntoView();", result_list[index])

"""Get the first page of job results, and extract the results from the page. 

You can manually apply a specific search filter and extract the URL from your browser. If you replace it here, you should be able to scrape using your desired filters. Leave off the "&page" querystring variable when copying the URL here, as it is already being added to the end for you.

The expected output for the above cell should be the total number of results in your search based on the search criteria.

The next cell visits every page from 2 to 50 by incrementing the page querystring variable for each iteration, and extracts the job search results on each page. This cell may take a few minutes to complete.
"""

search_url = 'https://www.linkedin.com/jobs/search/?distance=10&geoId=104116203&keywords=data%20science'
wd.get(search_url)
print(wd.save_screenshot('test.png'))
result_count = wd.find_elements_by_css_selector('.jobs-search-two-pane__title-heading')
# result_count = wd.find_element_by_css_selector('.search-results__total')
result_list = wd.find_elements_by_css_selector('.search-results__list li .job')
# print(result_count.text)
# extract_jobs_on_page()

print(jobs)

"""# New Section"""

def extract_multiple_pgs(page_index):
  for i in range(11, 15):
    wd.get(search_url + '&start=' + str(i * 25))
    extract_jobs_on_page()
    time.sleep(3)
    print('Successfully scraped page ' + str(i+1))
  print(jobs)

extract_multiple_pgs(5)

print(str(len(jobs)) + ' jobs scraped')
print(jobs)

"""You should have received the total number of job listings that were scraped. Next, we will visit each job link individually and obtain detailed data such as job description, skill list and industries.

This cell can take a very long time to run (~30 minutes to 1 hour depending on the number of job postings)
"""

full_jobs = []
for job in jobs:
  wd.get(job['href'])
  
  ## extracting salary estimate
  
  try:
    salary = wd.find_element_by_css_selector('.salary-main-rail__data-amount')
    job['salary'] = salary.text

  ## setting salary to some default value if salary information is unavailable 

  except:
    job['salary'] = -1
  
  description = wd.find_element_by_css_selector('.jobs-description-content__text')
  job['description'] = description.text
  skills = []
  skill_list = wd.find_elements_by_css_selector('.jobs-ppc-criteria__list--skills li .jobs-ppc-criteria__value')
  for skill in skill_list:
    if(skill.text.strip() != ''): 
      skills.append(skill.text.strip())
  job['skills'] = skills
  industry_list = wd.find_elements_by_css_selector('.jobs-description-details__list li')
  industries = []
  for industry in industry_list:
    industry_name = industry.get_attribute('innerHTML')
    if (industry_name.strip() != ''): 
      industries.append(industry_name.strip())
  job['industry'] = industries
  full_jobs.append(job)
print(full_jobs[0])

"""An example of a completely scraped record should be displayed above.

Now you can take this data and store it anyway you choose - send it to a database or dump it into a file. The next link demonstrates how you can save the output to a CSV: https://code.tutsplus.com/tutorials/how-to-read-and-write-csv-files-in-python--cms-29907
"""