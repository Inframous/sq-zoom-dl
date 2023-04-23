import requests
from pathlib import Path
import os
import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



LIST_OF_DICTS = []
HOME_DIR = Path.home()
URL = 'https://docs.google.com/document/u/0/export?format=txt&id=1r9XWDy0yt3YfwW8HwKmJFxUOF9HeqMc80TRfz3ZhvJo&token=AC4w5Vgrr26jK-Vu1ooN6lIgZ_jVOSwz9g:1679263645915&includes_info_params=true&cros_files=false&inspectorResult={"pc":5,"lplc":1}'


def download_file(url, output_file):
    ## Downloading google sheet as txt file
    google_sheet = requests.get(url)
    with open(output_file, 'w', encoding='utf8') as file:
        file.write(google_sheet.text)


def remove_empty_line(input_file, output_file):
    ## Removing empty lines from txt file.
    with open(file=input_file) as r, open(output_file, 'w', encoding='utf8') as o:
        for line in r:
            if line.strip():
                o.write(line)

def parse_file(file):
    ## Parsing the file
    with open(file, 'r') as DATA:
        lines = DATA.readlines()
    result = []
    count = 1
    for line in range(0, len(lines), 4):
            item = {}
            item['LessonNumber'] = count 
            item['Date'] = lines[line].strip().replace('/','-').replace(' :','').replace('\ufeff','')
            item['Link'] = lines[line+1].strip()
            # item['value3'] = lines[line+2].strip()
            item['Passcode'] = lines[line+3].strip()    
            if item['Link'].startswith("http"):
                result.append(item)
            else:
                count -= 1
            count += 1
    return result
    
def downloads_done(download_dir):
    ## Checking if download is done
    MP4 = False
    mp4_printed = False
    M4A = False
    m4a_printed = False
    TXT = False
    txt_printed = False
    DOWNLOADING = True
    while DOWNLOADING == True:
        for file in os.listdir(download_dir):
            if file.endswith('.mp4'):
                MP4 = True
                if mp4_printed == False:
                    print(f"Downloaded {file}.")
                    mp4_printed = True
            elif file.endswith('.m4a'):
                M4A = True
                if m4a_printed == False:
                    print(f"Downloaded (and deleted) {file}.")
                    os.remove(os.path.join(download_dir, file))
                    m4a_printed = True
            elif file.endswith('.txt'):
                TXT = True
                if txt_printed == False:
                    print(f"Downloaded {file}.")
                    txt_printed = True
            if MP4 == True and M4A == True and TXT == True:
                DOWNLOADING = False

def download_sq_clip(i):
    ## Downloading a single clip
    chrome_driver_path = ChromeDriverManager().install()
    S = Service(chrome_driver_path)
    lesson_count = i['LessonNumber']
    url = i['Link']
    lesson_date = i['Date']
    password = i['Passcode']
    
    download_dir = f'{HOME_DIR}/Downloads/sq-labs/Lesson {lesson_count} - {lesson_date}'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    ## Set the driver to load headless (no screen)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    ## Setting default download directory
    prefs = {'download.default_directory': download_dir, 
             'profile.default_content_setting_values.automatic_downloads': 1,
             } 
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(service=S, options=options)
    
    print("Connecting to server...")
    driver.get(url)
    
    ## Set the waitForElement time to 10 seconds.
    wait = WebDriverWait(driver, 15)
    
    ## Waiting for elements to appear (Passcode Field)
    password_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'zm-input__inner')))
    password_input.send_keys(password)
    
    ## Waiting for elements to appear (Passcode Button)
    click_to_enter = wait.until(EC.presence_of_element_located((By.ID, 'passcode_btn')))
    time.sleep(3)
    click_to_enter.click()
    print("Applying Passcode ...")

    ## Waiting for elements to appear (Download Button)
    download_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'download-btn')))
    ## Stalling, waiting for the files to be ready ..
    time.sleep(5)
    download_button.click()
    print(f"Downloading files, please stand by...")
    ## Stalling, letting the downloads to start.
    time.sleep(3)
    ## Sniffing for the files to determine if all 3 files were downloaded.
    downloads_done(download_dir)
    
    driver.quit()
    print("Download Complete!!")

def download_all():
    ## Function to download all clips
    print("Downloading ALL clips, this may take a while.")
    for item in parsed:
        print(f"Now downloading lesson {item['LessonNumber']} from {item['Date']}.")
        download_sq_clip(item)
        time.sleep(3)
    print("Downloaded ALL clips.")

def show_all():
    ## Function that returns a table of lesson numbers and dates.
    output = "LESSON #:      DATE:\n"
    for item in parsed:
        output += f"Lesson #{item['LessonNumber']} from {item['Date']}\n"
    return output

def download_specific():
    ## Function that download's a specific clip.
    print(show_all())
    choice = input("Please enter lesson number to download:  ")
    try:
        choice = int(choice) - 1
        print(f"Now downloading lesson {parsed[choice]['LessonNumber']} from {parsed[choice]['Date']}.")
        print("Waiting for download to finish.")
        download_sq_clip(parsed[choice])    
    except ValueError:
        print(f'"{choice}" is not an integer, returning to main menu.')
    
#### ------ ####

download_file(URL, 'raw.txt')
remove_empty_line('raw.txt', 'listed.txt')

parsed = parse_file('listed.txt')

os.system('clear')

def menu():
    print("Welcome to the menu!")
    print("1. Show All Clips")
    print("2. Download Specific Clips")
    print("3. Download All Clips")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print(show_all())
    elif choice == "2":
        download_specific()
    elif choice == "3":
        download_all()
    elif choice == "4":
        print("Exiting the program...")
        return
    else:
        print("Invalid choice. Please try again.")
    
    # Call menu() again to display the menu options until the user selects "4" to exit
    menu()

# Call the menu function to start the program
menu()
