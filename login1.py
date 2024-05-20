from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import string
import traceback

# Function to generate random username and password
def generate_random_username_password(length=8):
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(characters) for _ in range(length))
    password = ''.join(random.choice(characters) for _ in range(length))
    return username, password

# Predefined list of student names, certificate types, and remarks
student_names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown"]
certificate_types = ["Completion", "Achievement", "Participation", "Excellence"]
remarks_list = ["Excellent performance", "Good job", "Well done", "Outstanding"]

# Generate random details
username, password = generate_random_username_password()
student_name = random.choice(student_names)
certificate_type = random.choice(certificate_types)
remarks = random.choice(remarks_list)

# Chrome options
default_options = [
    "--disable-extensions", "--disable-user-media-security=true",
    "--allow-file-access-from-files", "--use-fake-device-for-media-stream",
    "--use-fake-ui-for-media-stream", "--disable-popup-blocking",
    "--disable-infobars", "--enable-usermedia-screen-capturing",
    "--disable-dev-shm-usage", "--no-sandbox",
    "--auto-select-desktop-capture-source=Screen 1",
    "--disable-blink-features=AutomationControlled"
]

headless_options = ["--headless", "--use-system-clipboard", "--window-size=1920x1080"]

# Function to set browser options
def browser_options(chrome_type):
    webdriver_options = Options()
    notification_opt = {"profile.default_content_setting_values.notifications": 1}
    webdriver_options.add_experimental_option("prefs", notification_opt)
    if chrome_type == "headless":
        var = default_options + headless_options
    else:
        var = default_options
    for d_o in var:
        webdriver_options.add_argument(d_o)
    return webdriver_options

# Function to get webdriver instance
def get_webdriver_instance(browser=None):
    base_url = "https://accounts.teachmint.com/"
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=browser_options(browser))
    driver.maximize_window()
    driver.get(base_url)
    return driver

# Function to log in
def login(driver, username, password):
    try:
        # Enter username
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))).send_keys(username)
        print("Entered username")
        
        # Enter password
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(password)
        print("Entered password")
        
        # Click login button
        driver.find_element(By.XPATH, "//input[@id='send-otp-btn-id']").click()
        
        
        # Wait for login to complete
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='profile-user-name']")))
        print("Successfully logged in")
    
    except Exception as e:
        print(f"Exception occurred during login: {e}")
        driver.save_screenshot("login_error.png")
        print("Screenshot saved as 'login_error.png'")
        traceback.print_exc()

# Function to generate certificate
def generate_certificate(driver, student_name, certificate_type, remarks):
    try:
        # Navigate to certificates
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Certificates']"))).click()
        
        # Select certificate type
        select = Select(WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'certificateTypeSelect'))))
        select.select_by_visible_text(certificate_type)
        
        # Search and select the student
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Student']"))).send_keys(student_name)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{student_name}']"))).click()
        
        # Click on generate
        driver.find_element(By.XPATH, "//button[text()='Generate']").click()
        
        # Update remarks
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'remarks'))).send_keys(remarks)
        
        # Generate and download
        driver.find_element(By.XPATH, "//button[text()='Generate and Download']").click()
        
        # Validate the history of certificates
        history_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Certificate History']")))
        history_element.click()
        print("Certificate generated and history validated")
    
    except Exception as e:
        print(f"Exception occurred during certificate generation: {e}")
        driver.save_screenshot("certificate_generation_error.png")
        print("Screenshot saved as 'certificate_generation_error.png'")
        traceback.print_exc()

# Main function
def main():
    driver = get_webdriver_instance()
    login(driver, username, password)
    generate_certificate(driver, student_name, certificate_type, remarks)
    driver.quit()

if __name__ == "__main__":
    print("start")
    main()
    print("end")
