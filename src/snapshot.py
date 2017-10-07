import logging
import time

from selenium import webdriver  
from selenium.webdriver.chrome.options import Options

from image_diff import compare_img

logger = logging.getLogger(__name__)

chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
# binary_location is optional, selenium is able to find by itself
# chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  

driver = None

def get_driver():
	global driver
	if not driver:
		logger.info('Starting Chrome driver')
		# IMPORTANT: driver must be in system $PATH
		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.set_page_load_timeout(15)

	return driver

def close_driver():
	global driver
	logger.info('Closing Chrome driver')
	if driver:
		driver.close()
	driver = None

def take_snapshot(task, snapshot_path):
	# TODO: no need to save if found no change
	# https://stb-tester.com/blog/2016/09/20/add-visual-verification-to-your-selenium-tests-with-stb-tester
	driver = get_driver()
	try:
		logger.info('[Task {}] Loading {}'.format(task.id, task.url))
		driver.get(task.url)
		width = driver.execute_script("return document.body.scrollWidth")
		height = driver.execute_script("return document.body.scrollHeight")
		if width == 0:
			width = 800
		if height  == 0:
			height = 1200
		logger.info('[Task {}] Document size {},{}'.format(task.id, width, height))
		driver.set_window_size(width, height)
		time.sleep(1)
		logger.info('[Task {}] Taking snapshot'.format(task.id))
		driver.save_screenshot(snapshot_path)

		logger.info('[Task {}] Snapshot saved successfully - {}'.format(task.id, snapshot_path))

	except Exception as e:
		logger.exception(e)
		logger.error('[Task {}] Snapshot failed.'.format(task.id))
		return False
	return True