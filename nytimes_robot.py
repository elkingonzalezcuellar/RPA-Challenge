from RPA.Browser.Selenium import Selenium
from RPA.Robocloud.Items import Items
from RPA.Robocorp.WorkItems import WorkItems
from robocorp.tasks import task
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.FileSystem import FileSystem
import re
import requests
import json
import os
import datetime
import time
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




class NYTimesRobot:

    def __init__(self):
        self.browser = Selenium()
        self.files = Files()
        self.tables = Tables()
        self.pdf = PDF()
        self.fs = FileSystem()
    
    def read_config(self):
        with open("config.json") as config_file:
            config = json.load(config_file)
            return config["search_phrase"], config["news_category"], config["num_months"]
        
    
    def main(self):



        
        """ output_folder = "output"

        search_phrase, news_category, num_months = self.read_config()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        execution_folder_name = f"{current_date} - {search_phrase}"
        execution_folder = os.path.join(output_folder, execution_folder_name)
        os.makedirs(execution_folder, exist_ok=True)
        images_folder = os.path.join(execution_folder, "images")
        os.makedirs(images_folder, exist_ok=True)
        excel_folder = os.path.join(execution_folder, "excel")
        os.makedirs(excel_folder, exist_ok=True) """

        
       
        

        try:
            self.browser.open_available_browser("http://www.nytimes.com/")
        except Exception as e:
            print("Robocopr dont have  anybrowser")
        

        print("Hello")
        try:
            self.handle_dialog_and_continue()
        except Exception as e:
            print("I can't run  dialog")
        # end try """
        
        try:
            self.browser.maximize_browser_window()  
            # comment: 
        except Exception as e:
            print("i cant maximize browser")
        # end try

        try:
            WebDriverWait(self.browser.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='nav-button']"))
            )

            page_source = self.browser.get_source()
            
            with open("output/page_source2.html", "w", encoding="utf-8") as f:
                f.write(page_source)

            self.browser.click_element("css=[data-testid='nav-button']")
        except Exception as e:
            print("Error while clicking nav button:", e)

        # Esperar a que la página se cargue y el botón de búsqueda sea visible
        try:
           
            
            # Desplazar hacia el botón de búsqueda para asegurarse de que esté visible
            self.browser.scroll_element_into_view("css=[data-testid='search-button']")
            # Hacer clic en el botón de búsqueda
            self.browser.click_element("css=[data-testid='search-button']")
        except Exception as e:
            print("Error while clicking search button:", e)
        
        # Within the try block for capturing the page source
        # Within the try block for capturing the page source
        try:
            page_source = self.browser.get_source()
            
            with open("output/page_source.html", "w", encoding="utf-8") as f:
                f.write(page_source)
        except Exception as e:
            print("Failed to extract page source:", e) 

        # Within the try block for capturing the screenshot
        try:
            
            self.browser.capture_page_screenshot("output/captura.png")
        except Exception as e:
            print("Failed to capture screenshot:", e)
        

        """ try:
            self.browser.wait_until_element_is_visible("css=[data-testid='search-input']")
            

        except Exception as e:
            
            
            print("i cant found search phrase input",e)
        try:
            self.browser.input_text("css=[data-testid='search-input']", search_phrase)
             
        except Exception as e:
            print("i cant introduce search phrase",e)
        # end try

        try:
            self.browser.press_keys("css=[data-testid='search-input']", "ENTER")
        except Exception as e:
            print("i cant enter search phrase")
        try:
            self.apply_filters(news_category)
            # comment: 
        except Exception as e:
            print("i cant aply filters")
        # end try
        try:
             
            self.select_date_range(num_months)
        except Exception as e:
            print("i cant stablish date range")
        # end try
        try:
            self.sort_by_newest()
            # comment: 
        except Exception as e:
            print("i cant sort by newest")
        # end try

        try:
            self.load_more_news()
            # comment: 
        except Exception as e:
            print("i cant load all news")
        # end try
        try:
            news_data = self.get_values()
            # comme 
        except Exception as e:
            print("i cant get data values")
        # end try
        try:
            self.store_in_excel(news_data, search_phrase, excel_folder,images_folder) 
            # comment: 
        except Exception as e:
            print("i cant store date in excel")
        # end try
        try:
            self.browser.close_all_browsers()
            # comment: 
        except Exception as e:
            print("i cant close browsers") """
        # end try
    
    def handle_dialog_and_continue(self):
        try:
            continue_button = self.browser.find_element("css=.css-1fzhd9j")
            if continue_button:
                continue_button.click()
        except Exception as e:
            print("Error handling dialog:", e)
    
    def apply_filters(self, selected_categories):
        self.browser.click_element("css=[data-testid='search-multiselect-button']")
        
        for i in range(2, 11):  
            checkbox_selector = f"xpath=//*[@id='site-content']/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[{i}]/label/input"
            outer_span_selector = f"xpath=//*[@id='site-content']/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[{i}]/label/span"
            inner_span_selector = f"xpath=//*[@id='site-content']/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[{i}]/label/span/span"
            
            try:
                outer_span_text = self.browser.find_element(outer_span_selector).text
                
                inner_span_text = self.browser.find_element(inner_span_selector).text
                
                category_name = outer_span_text.replace(inner_span_text, '').strip()
                
                if category_name in selected_categories:
                    self.browser.click_element(checkbox_selector)
            except Exception as e:
                break
        
        self.browser.click_element("css=[data-testid='search-multiselect-button']")
        self.sort_by_newest()

        


    def sort_by_newest(self):
            sort_by_selector = "css=.css-v7it2b"
            self.browser.select_from_list_by_label(sort_by_selector, "Sort by Newest")

    def select_date_range(self, num_months):
        self.browser.click_element("css=[data-testid='search-date-dropdown-a']")
        self.browser.click_element("css=[value='Specific Dates']")
        today = datetime.datetime.today()
        start_date = (today - relativedelta(months=num_months)).strftime("%m/%d/%Y")
        end_date = today.strftime("%m/%d/%Y")
        self.browser.input_text("css=[data-testid='DateRange-startDate']", start_date)
        self.browser.input_text("css=[data-testid='DateRange-endDate']", end_date)
        self.browser.press_keys("css=[data-testid='DateRange-endDate']","ENTER")
        self.browser.wait_until_element_is_not_visible("css=[data-testid='DayPickerPopup']")

    def load_more_news(self):
            while True:
                try:
                    self.browser.click_button_when_visible("css=[data-testid='search-show-more-button']")
                    
                except Exception:
                    break
                


    def get_values(self):

            news_elements = self.browser.find_elements("css=[data-testid='search-bodega-result']")

            news_data = []
            for element in news_elements:
                date_element = self.browser.find_element("css=[data-testid='todays-date']", element).text
                title = self.browser.find_element("css=h4.css-2fgx4k", element).text
                try:
                    description = self.browser.find_element("css=p.css-16nhkrn", element).text
                    
                except Exception as e:
                    description = ""

                try:
                    image_element = self.browser.find_element("css=img.css-rq4mmj",element)
                    image_url = image_element.get_attribute("src")
                except Exception as e:
                    image_url = ""
                
                
                
                news_data.append({"date": date_element, "title": title, "description": description , "image_url": image_url})

            return news_data 

    def process_news_articles(self, num_months):
        for _ in range(num_months):
            articles = self.browser.find_elements("article-element-selector")
            for article in articles:
                title = article.find_element("title-selector").text
                date = article.find_element("date-selector").text
                description = article.find_element("description-selector").text
                self.store_in_excel(title, date, description)


    
    def store_in_excel(self, news_data, search_phrases, excel_folder,images_folder):
        excel_file = os.path.join(excel_folder, "news_data.xlsx")
        self.files.create_workbook(excel_file)

        sheet_name = "NewsData"
        header = ["Title", "Date", "Description", "Picture Filename", "Search Phrase Count", "Contains Money"]

        
        table = {col: [] for col in header}

        for news in news_data:
            title = news.get("title", "")
            date = news.get("date", "")
            description = news.get("description", "")
            picture_filename = news.get("picture_filename", "")
            image_url = news.get("image_url", "")
            search_phrase_count = self.count_search_phrases(title, description, search_phrases)
            contains_money = self.contains_money(title, description)
            image_filename = self.download_image(image_url,images_folder)

            
            table["Title"].append(title)
            table["Date"].append(date)
            table["Description"].append(description)
            table["Picture Filename"].append(image_filename)
            table["Search Phrase Count"].append(search_phrase_count)
            table["Contains Money"].append(contains_money)

        self.files.create_worksheet(sheet_name, content=table, header=True)  
        self.files.save_workbook(excel_file)
    
    def count_search_phrases(self, title, description, search_phrases):
        search_phrases = search_phrases.lower().split()
        search_phrase_count = 0
        for phrase in search_phrases:
            if phrase in title.lower() or phrase in description.lower():
                search_phrase_count += 1
        return search_phrase_count

    def contains_money(self, title, description):
            money_pattern = r'\$\d+(\.\d{1,2})?|\d+\s?(dollars|USD)'
            return bool(re.search(money_pattern, title)) or bool(re.search(money_pattern, description))
    def download_image(self, image_url, images_folder):
            if image_url:
                image_filename = os.path.basename(image_url)
                image_filename = image_filename.split("?")[0] 
                image_path = os.path.join(images_folder, image_filename) 
                
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    return image_path
            return ""


    

if __name__ == "__main__":
    nytimes_robot = NYTimesRobot()
    nytimes_robot.main()
