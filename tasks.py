from robocorp import browser
from robocorp.tasks import task
from pathlib import Path
import os
import sys
from time import sleep  # Import sleep function for waiting
from robocorp import browser
import time
import re
from datetime import datetime
import requests
import shutil
import uuid
import pandas as pd


class NewsProcessor:
    def __init__(self, browser,search_phrase, news_category):
        self.browser = browser
        self.search_phrase = search_phrase  # Store search_phrase as an attribute
        self.news_category = news_category
        self.file_name = f"challenge_{uuid.uuid4()}.xlsx"

    # Function to process news data
    def process_news(self,browser, search_phrase: str, news_category: str):
        # Step 1: Open the Gothamist website
        try:
            page = browser.goto("https://gothamist.com/")  
        except TimeoutError as e:
            print("Navigation timeout occurred:", e)
        # Step 2: Click on search bar and enter search phrase
        self.click_and_enter_search(page, search_phrase)

        # Step 3: Wait for the page to load after search
        sleep(10)  # Adjust time as needed for page to load

        # Step 6: Extract data and store in CSV file
        self.extract_and_store_data( page)


    # Function to open the Gothamist website
    # Function to open the Gothamist website and close pop-up ad if it exists
    def open_gothamist_website(self,browser):
        page = browser.goto("https://gothamist.com/")
        
        close_button = page.query_selector("#om-yamoqiem3ef6jawyqxal-yesno > div > button > svg")
        if close_button:
            close_button.click()
        return page


    # Function to click on search bar and enter search phrase
    def click_and_enter_search(self,page, search_phrase: str):
        # Click on the search bar
        page.click("#__nuxt > div > div > main > header > div.top.flex.justify-content-between.align-items-center.sm\:align-items-end > div.gothamist-header-right.align-items-center.gap-2 > div.search-button > button")

        # Enter the search phrase
        page.fill("#search > input", search_phrase)
        page.press("#search > button > span.pi.pi-arrow-right.p-button-icon", "Enter")  # Submit the search

    # Function to count occurrences of search phrase in the title
    def count_search_phrase_in_title(self,title: str, search_phrase: str) -> int:
        return title.lower().count(search_phrase.lower())
        # Function to save data to CSV file
    def save_to_csv(self, df, output_file):
        # Save the DataFrame to a CSV file
        df.to_csv(output_file, index=False)
        print("Data saved to CSV file:", output_file)
    
    # Function to delete all images in the output folder
    def delete_images(self):
        output_directory = os.path.join(os.getcwd(), "output", "images")
        for filename in os.listdir(output_directory):
            file_path = os.path.join(output_directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    # Function to save parameters and image path in an Csv file

    # Function to count occurrences of search phrase in the description
    def count_search_phrase_in_description(self,description: str, search_phrase: str) -> int:
        # Define a regular expression pattern to match variations of the search phrase
        pattern = re.compile(r'\b' + re.escape(search_phrase) + r'\b', re.IGNORECASE)

        # Count occurrences of the search phrase in the description using the pattern
        count = len(re.findall(pattern, description))
        return count


    # Function to check if title or description contains any amount of money
    def contains_money(self,title: str, description: str) -> bool:
        money_pattern = r'\$\d+(\.\d+)?|\d+(\.\d+)?\s*(dollars|USD)'
        return bool(re.search(money_pattern, title, re.IGNORECASE)) or bool(re.search(money_pattern, description, re.IGNORECASE))


    # Function to download an image from a URL and save it locally
    def download_image(slef,url: str, title: str) -> str:
        # Send a GET request to the image URL
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Generate a random string for the filename
            random_string = str(uuid.uuid4())
            filename = f"image-gothamit-{random_string}.jpg"
            
            # Get the absolute path to the "output\images" directory
            current_directory = os.getcwd()  # Get the current working directory
            images_directory = os.path.join(current_directory, "output", "images")
            os.makedirs(images_directory, exist_ok=True)  # Create the directory if it doesn't exist
            
            # Construct the full path to save the image
            image_path = os.path.join(images_directory, filename)
            
            # Open a new file and write the image content to it in binary mode
            with open(image_path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            
            print("Image downloaded successfully:", image_path)  # Print the downloaded image path for debugging
            
            return filename
        else:
            print("Failed to download image.")
            return ""


    # Function to parse date string into datetime object
    def parse_date_string(self,date_string):
        # Split the date string into components
        parts = date_string.split()
        month = parts[1]
        day = parts[2][:-1]  # Remove the comma at the end
        year = parts[3]
        
        # Convert month abbreviation to its corresponding number
        months = {
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
            "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
            "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
        }
        month_number = months.get(month)
        
        # Construct and return the datetime object
        return str(year)+"_-_"+str(month_number)+"_-_"+str(day)
        
        # Function to extract data and store in CSV file
    def extract_and_store_data(self, page):
        num_articles = 5  # Set the default number of articles to 5

        # Define the selector for the load more button
        load_more_button_selector = "#resultList > div.col > button > span.p-button-label"

        self.delete_images()

        # Initialize an empty list to store data
        data = []

        # Iterate through the specified number of articles
        for i in range(1, num_articles + 1):
            # Construct selectors for title, description, and image elements based on the index
            title_selector = f"#resultList > div.col > div:nth-child({i}) > div > div.card-details > div.card-title > a > div"
            
            description_selector = f"#resultList > div.col > div:nth-child({i}) > div > div.card-details > div.card-slot > p"
            image_selector = f"#resultList > div.col > div:nth-child({i}) > div > div.card-image-link.card-image-wrapper > figure:nth-child(2) > div > div > a > div > img"

            # Extract information for the current news item
            title_element = page.query_selector(title_selector)
            title = title_element.inner_text() if title_element else "Unknown"

            description_element = page.query_selector(description_selector)
            description = description_element.inner_text() if description_element else "Unknown"

            image_element = page.query_selector(image_selector)
            image_filename = ""
            if image_element:
                # Get the image source URL
                image_url = image_element.get_attribute("src")

                # Download the image
                image_filename = self.download_image(image_url, title)
                print("Downloaded image filename:", image_filename)

            # Click on the title to navigate to the full article page
            title_element.click()
            sleep(5)  # Wait for the page to load

            # Extract author and date of publication from the article page
            author_element = page.query_selector("#author-selector")
            author = author_element.inner_text() if author_element else "Unknown"

            date_element = page.query_selector("#date-selector")
            date_published_string = date_element.inner_text() if date_element else "Unknown"

            # Parse the date string into datetime object
            date_published = str(self.parse_date_string(date_published_string) if date_published_string != "Unknown" else "Unknown")
            date_published = date_published.replace(" ", " at ")
            date_published = "'" + date_published

            # Print the title, author, and date of publication for debugging
            print("Title:", title)
            print("Author:", author)
            print("Date of Publication:", date_published)
            print("Description:", description)

            # Count occurrences of search phrase in title and description
            search_phrase_title_count = self.count_search_phrase_in_title(title, self.search_phrase)
            search_phrase_description_count = self.count_search_phrase_in_description(description, self.search_phrase)

            # Check if title or description contains any amount of money
            money_present = self.contains_money(title, description)

            # Print search phrase counts and money presence
            print("Search phrase '{}' count in title: {}".format(self.search_phrase, search_phrase_title_count))
            print("Search phrase '{}' count in description: {}".format(self.search_phrase, search_phrase_description_count))
            print("Money present in title or description:", money_present)

            # Append the data to the list
            print("Appending data for:", title, "Date of Publication:", date_published)
            data.append([title, author, date_published, description, search_phrase_title_count,
                        search_phrase_description_count, money_present, image_filename])

            # Navigate back to the main page
            page.go_back()
            sleep(5)  # Wait for the page to load again

            # If it's not the last article, click on the load more button to load more articles
            if i < num_articles:
                load_more_button = page.query_selector(load_more_button_selector)
                if load_more_button:
                    load_more_button.click()
                    sleep(5)  # Wait for the page to load after loading more articles

        # Create a DataFrame from the collected data
        df = pd.DataFrame(data, columns=["Title", "Author", "Date Published", "Description",
                                        "Search Phrase Title Count", "Search Phrase Description Count",
                                        "Money Present", "Image Filename"])

        # Generate a unique file name using uuid
        file_name = f"challenge_{uuid.uuid4()}.csv"
        output_dir = os.environ.get('ROBOT_ARTIFACTS')
        csv_file = os.path.join(output_dir, file_name)

        # Save the DataFrame to a CSV file
        df.to_csv(csv_file, index=False)

        print("Data saved to CSV file:", csv_file)

   

# Define task to solve the RPA challenge
@task
def solve_challenge():
    """
    Solve the RPA challenge
    
    """
    browser.configure(
        browser_engine="chromium",
        screenshot="only-on-failure",
        headless=False,
    )
    try:
        search_phrase = "Microsoft"
        news_category = ""  # No category needed for Gothamist
        
        # Create an instance of NewsProcessor
        news_processor = NewsProcessor(browser, search_phrase, news_category)
        
        # Process news data using NewsProcessor instance
        news_processor.process_news(browser, search_phrase, news_category,)

    finally:
        # Place for teardown and cleanups
        # Playwright handles browser closing
        print('Done')
