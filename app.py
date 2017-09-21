import os  
import logging
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

chrome_options = Options()  
chrome_options.add_argument("--headless")
# binary_location is optional, selenium is able to find by itself
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  

# IMPORTANT: driver must be in system $PATH
driver = webdriver.Chrome(chrome_options=chrome_options)
logger.info('start')
try: 
	driver.get("https://www.google.com")
	driver.save_screenshot('haha.png')
except Exception as e:
	logger.exception(e)
logger.info('done')
driver.close()