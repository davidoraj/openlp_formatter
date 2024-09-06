from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import transliterate
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Set up the Selenium WebDriver (replace the path with your driver path)
service = Service('/Users/david_ogirala/work/webdrivers/gecko/geckodriver')
driver = webdriver.Firefox(service=service)

# Replace with the URL you want to scrape
root_url = 'https://songsofzion.org'
book_url = '/book/1'

# Get list of songs
driver.get(root_url + book_url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

linkdivs = soup.find_all('div', class_='book-song-div-a')
song_urls = []
for linkdiv in linkdivs:
    link = linkdiv.find('a')
    song_url = root_url + link.get('href')
    song_urls.append(song_url)
    song_name = link.text.split('|')[0]
    print(song_url + " - " + link.text.strip())

print()

# song_urls = ['https://songsofzion.org/songs/2789']
for song_url in song_urls[503:]:
    print(f'Downloading song {song_url}')
    try:
        driver.get(song_url)
        timeout_in_seconds = 10
        WebDriverWait(driver, timeout_in_seconds).until(
            expected_conditions.presence_of_element_located((By.ID, 'noanim-tab-example-tabpane-Translation')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except TimeoutException:
        print(f'Unable to get song: {song_url}')

    # driver.get(song_url)
    # time.sleep(0.5)
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.find('h4')
    telugu_name = title.get_text().split('|')[-1]
    content = soup.find('div', id='noanim-tab-example-tabpane-Translation').get_text(separator="\n")
    content = content.replace('.', '. ').replace(':', '').replace(' ', '').replace(' ','').replace('  ', ' ')

    eng_content = soup.find('div', id="noanim-tab-example-tabpane-English").get_text(separator="\n").split('\n')[0]
    song_name = transliterate.translate(telugu_name).title()
    translated = transliterate.translate(content)


    filename = f"{song_name}.txt"
    transliterate.write_to_file(translated, content, filename, eng_content)

# Close the browser
driver.quit()
