from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
service = Service(executable_path=ChromeDriverManager().install())

print(1)
driver = webdriver.Chrome(service=service)
print(2)
driver.get("http://www.python.org")
print(3)
assert "Python" in driver.title
print(4)
elem = driver.find_element(By.NAME, "q")
print(5)
elem.clear()
print(6)
elem.send_keys("pycon")
print(7)
elem.send_keys(Keys.RETURN)
print(8)
assert "No results found." not in driver.page_source
print(9)
driver.close()