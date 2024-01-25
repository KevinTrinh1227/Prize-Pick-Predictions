from selenium import webdriver
from bs4 import BeautifulSoup
import json

driver = webdriver.Chrome()

#Initializes a web driver and opens the page in a new chrome window
url = 'https://api.prizepicks.com/projections?league_id=7'
driver.get(url)

#Beautiful soup parsing through the page contents
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
pre_tag = soup.find('pre') #finds the tag starting with "pre"

#Dumps the json contents into the filenamed "pre_formatted_predictions.json"
json_text = pre_tag.text
data = json.loads(json_text)
filename = "pre_formatted_predictions.json"
print(data)
