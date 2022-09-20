from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import pandas as pd 
from time import sleep

def get_jobs(path):

    data = {}
    job_name = []
    company = []
    experience_req = []
    posted = []
    salary = []
    skills_req = []
    link = []
    location = []

    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--headless")

    for page in range(1,6):
        url = f"https://www.naukri.com/disability-jobs-{page}"

        driver = webdriver.Chrome(executable_path=path, options=options)
        wait = WebDriverWait(driver, 60)

        try:
            driver.get(url)
            time.sleep(10)

            driver.find_element_by_class_name('crossIcon').click()

            try:
                job_class = driver.find_element_by_class_name('list')
                #print(job_class.text)
            except Exception as e:
                print(f'job_class error: {e}')
            

            try:
                job_list = job_class.find_elements_by_tag_name('article')
                #print(len(job_list))
            except Exception as e:
                print(f'job_list error: {e}')
        
            for job in job_list:

                job_name.append(job.find_element_by_tag_name('a').text)
                #print(job_name[0],'-------')

                link.append(job.find_element_by_tag_name('a').get_attribute('href'))
                #print(link[0],'-------')

                company_info = job.find_element_by_class_name('companyInfo')
                company.append(company_info.find_element_by_class_name('subTitle').text)
                #print(company[0],'-------')
            
                job_info = job.find_element_by_tag_name('ul')
                #experience_req.append(job_info.find_element_by_class_name('experience').text)
                #print(experience_req[0],'-------')
        
                salary.append(job_info.find_element_by_class_name('salary').text)
                #print(salary[0])

                location.append(job_info.find_element_by_class_name('location').text)
                #print(location[0])

                skills = job.find_element_by_class_name('tags')
                skill_list = skills.find_elements_by_tag_name('li')
                s_list = ''
                for skill in skill_list:

                    #s_list.append(skill.text)
                    if skill != skill_list[-1]:
                        s_list = s_list + skill.text + ', '
                    else:
                        s_list = s_list + skill.text
                skills_req.append(s_list)
                #print(skills_req[0])
                
                #job_footer = job.find_element_by_class_name('jobTupleFooter')
                #posted.append(job_footer.find_element_by_class_name('grey').find_element_by_class_name('fw500').text)
                """
                try:
                    posted.append(job_footer.find_element_by_class_name('grey').text)
                except Exception as e:
                    print(f'job_posted error {e}')
                #print(posted[0])
                """
                

        except Exception as e:
            print(f'driver.get error:\n {e}')
    """
    print(job_name,len(job_name))
    print(company,len(company))
    print(location,len(location))
    print(experience_req,len(experience_req))
    print(salary,len(salary))
    print(skills_req,len(skills_req))
    print(posted,len(posted))
    print(link,len(link))
    """
    jobs_data = pd.DataFrame({
        'job_name' : job_name,
        'company' : company,
        'location' : location,
        #'experience_req' : experience_req,
        'salary' : salary,
        'skills_req' : skills_req,
        #'posted' : posted,
        'link' : link
    })

    jobs_data.to_csv('jobs_scraped.csv')
    
    driver.quit()

get_jobs(r"chromedriver_win32\chromedriver.exe")