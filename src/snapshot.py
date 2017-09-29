import logging

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


# url = "https://www.goo000dsdsgle.com"
# url = "https://www.google.com"
# # url = "https://www.zhihu.com/explore"
# url = "https://www.v2ex.com/t/379120"
# # url = 'https://time.is/'
# url = 'https://www.sitepoint.com/how-to-create-mysql-events/'


def get_driver():
	global driver
	if not driver:
		logger.info('Starting Chrome driver')
		# IMPORTANT: driver must be in system $PATH
		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.set_page_load_timeout(10)
		driver.set_window_size(1000, 2000) # bad, how to know the height of web page?

	return driver

def close_driver():
	global driver
	logger.info('Closing Chrome driver')
	if driver:
		driver.close()
	driver = None

def take_snapshot(task, snapshot_path, snapshot_name):
	# TODO: no need to save if found no change
	# https://stb-tester.com/blog/2016/09/20/add-visual-verification-to-your-selenium-tests-with-stb-tester
	driver = get_driver()
	try:
		logger.info('[Task {}] Loading {}'.format(task.id, task.url))
		driver.get(task.url)
		logger.info('[Task {}] Taking snapshot'.format(task.id))
		driver.save_screenshot(snapshot_path)

		logger.info('[Task {}] Snapshot saved successfully - {}'.format(task.id, snapshot_name))

	except Exception as e:
		logger.exception(e)
		logger.error('[Task {}] Snapshot failed.'.format(task.id))
		return False
	return True