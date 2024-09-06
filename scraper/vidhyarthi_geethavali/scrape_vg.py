from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import transliterate
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import concurrent.futures
import numpy

# Set up the Selenium WebDriver (replace the path with your driver path)
service = Service('/Users/david_ogirala/work/webdrivers/gecko/geckodriver')
driver = webdriver.Firefox(service=service)

# Replace with the URL you want to scrape
root_url = 'https://www.christiandatahouse.com/p/vidhyarthi-geethavalii.html#google_vignette'

# Get list of songs
driver.get(root_url)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')

linkdivs = soup.find('div', id='post-body-9084307637722674644')
links = linkdivs.find_all('a')
song_urls = []
for link in links:
    song_url = link.get('href')
    song_urls.append(song_url)
    song_name = link.text.strip
    print(song_url + " - " + link.text.strip())

print()
driver.quit()


def download_songs(song_urls):
    print()
    driver = webdriver.Firefox(service=service)
    for song_url in song_urls:
        print(f'Downloading song {song_url}')
        try:
            driver.get(song_url)
            timeout_in_seconds = 10
            WebDriverWait(driver, timeout_in_seconds).until(
                expected_conditions.presence_of_element_located((By.ID, 'Blog1')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except TimeoutException:
            print(f'Unable to get song: {song_url}')
            continue

        title = soup.find('h3')
        telugu_name = title.get_text().strip('( )\n0123456789')

        content_list = soup.find('div', class_='post-body entry-content').get_text(
            separator='\n').replace('\n\n', '\n').replace('.', '. ').replace(':', '').replace(' ', '').replace(' ',
                                                                                                               '').replace(
            '  ', ' ').split('\n')

        filtered_contents = []
        for line in content_list:
            if 'telugu' in line.lower():
                continue
            if 'chord' in line.lower() or 'english' in line.lower():
                break
            filtered_contents.append(line)

        song_name = transliterate.translate(telugu_name).title()
        content = '\n'.join(filtered_contents)
        translated = transliterate.translate(content)

        filename = f"songs_dump/{song_name}.txt"
        transliterate.write_to_file(translated, content, filename, song_url)
    # Close the browser
    driver.quit()


def main():
    # chunks = numpy.array_split(song_urls, 30)
    # pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    # for chunk in chunks:
    #     pool.submit(download_songs, chunk)
    # pool.shutdown(wait=True)

    download_songs(song_urls)


if __name__ == "__main__":
    main()
