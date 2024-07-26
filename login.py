from datetime import datetime
import time
import pytz
import schedule

import configParser as cp
import emailSender as emailSender
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cm = cp.ConfigManager()

# Accessing properties
user_details = cm.get_user_details()
base_url = cm.get_base_url()

#constants
duration = 10
MAX_RETRY_CNT = 3
CLOCK_IN = 1
CLOCK_OUT = 2


def perform_clock_in(driver):
    # Wait for the <a> tag within the div element to be present
    a_tag = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#_FOpt1\:_FOr1\:0\:_FONSr2\:0\:_FOTsr1\:1\:wcRgn\:0\:wcUpl\:UPsp1\:cil21Btn > a')))

    # Click on the <a> tag
    driver.execute_script("arguments[0].click();", a_tag)



######################################

def perform_clock_out(driver):
    # Wait for the <a> tag within the div element to be present
    a_tag = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#_FOpt1\:_FOr1\:0\:_FONSr2\:0\:_FOTsr1\:1\:wcRgn\:0\:wcUpl\:UPsp1\:cil21Btnj_id_1 > a')))

    # Click on the <a> tag
    driver.execute_script("arguments[0].click();", a_tag)
    # a_tag.click()


##################################

def login_to_website(base_url, email, password,m_seq):
    # Initialize Chrome WebDriver (you can use other browsers as well)
    driver = webdriver.Chrome()

    try:
        # Open the base URL
        driver.get(base_url)

        # Wait for the welcome page to load
        welcome_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ssoBtn'))
        )

        # Click the button on the welcome page
        welcome_page_button.click()

        # Wait for the login page to load
        login_page_email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'userNameInput'))
        )

        # Enter email and password
        login_page_email_field.send_keys(email)
        login_page_password_field = driver.find_element(By.ID, 'passwordInput')
        login_page_password_field.send_keys(password)

        # Submit the login form
        login_page_submit_button = driver.find_element(By.ID, 'submitButton')
        login_page_submit_button.click()

        # Locate and click the navigation button
        navigation_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'pt1:_UIScil1u'))
        )
        navigation_button.click()

        # Locate and click the Web Clock button
        webClock_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'HWM_HCMWFMWORKAREA_FUSE_WEBCLOCK_0'))
        )
        webClock_button.click()

        time.sleep(10)

        if(m_seq == 1):
            perform_clock_in(driver)
        else:
            perform_clock_out(driver)

        time.sleep(10)

        popup_a_tag = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#_FOpt1\:_FOr1\:0\:_FONSr2\:0\:_FOTsr1\:1\:wcRgn\:0\:wcUpl\:UPsp1\:tcfRgn\:0\:SISAltName1\:CLovMatrixAttributeAltName1\:\:btn')))
        driver.execute_script("arguments[0].click();", popup_a_tag)

        time.sleep(10)

        work_from_home_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#_FOpt1\:_FOr1\:0\:_FONSr2\:0\:_FOTsr1\:1\:wcRgn\:0\:wcUpl\:UPsp1\:tcfRgn\:0\:SISAltName1\:CLovMatrixAttributeAltName1\:\:item0 > th')))
        work_from_home_div.click()

        time.sleep(10)

        submit_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#_FOpt1\:_FOr1\:0\:_FONSr2\:0\:_FOTsr1\:1\:wcRgn\:0\:wcUpl\:UPsp1\:subBtn')))
        submit_btn.click()

        # This will keep the browser open for given time duration
        time.sleep(duration)
        return True

    except Exception as e:
        return False
        
    finally:
        # Close the browser
        driver.quit()

##################################

def check_time_and_run():
    # Get current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    current_hour = current_time.hour
    current_minute = current_time.minute
    print(current_time)

    retry = 0
    action = CLOCK_IN
    result = False
    if current_hour == 9 and current_minute == 38:
        action = CLOCK_IN
    elif current_hour == 23 and current_minute == 42:
        action = CLOCK_OUT
    else:
        return

    formatted_date = current_time.strftime('%d/%m/%Y')

    for person, details in user_details.items():
        print(f"Making attendance for {person}")
        retry = 0
        result = True
        emailId = details.get('emailId')
        password = details.get('password')
        to_email = details.get('to_email')
        while retry != MAX_RETRY_CNT:
            result = login_to_website(base_url, emailId, password,action)
            if result==False:
                retry = retry + 1
            else:
                break

        # Send email to user to tell them about attendance status for current date (dd/mm/yyyy)
        emailSender.send_attendance_notification(result,formatted_date,action,to_email)


###########################################


# Schedule the check_time_and_run function to run every minute
schedule.every().minute.do(check_time_and_run)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
