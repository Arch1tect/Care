import os  
import logging
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options
from image_diff import compare_img

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

chrome_options = Options()  
chrome_options.add_argument("--headless")
# binary_location is optional, selenium is able to find by itself
# chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  

# IMPORTANT: driver must be in system $PATH
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(10)
driver.set_window_size(1000, 2000) # bad, how to know the height of web page?
logger.info('Start')

url = "https://www.goo000dsdsgle.com"
url = "https://www.google.com"
# url = "https://www.zhihu.com/explore"
# url = "https://www.v2ex.com/t/379120"
url = 'https://time.is/'

try:

	driver.get(url)
	driver.save_screenshot('new_time.png')
	logger.info('Success')

except Exception as e:
	logger.exception(e)
	logger.error('Failed')

logger.info('Closing driver')
driver.close()

compare_img('time.png', 'new_time.png')


