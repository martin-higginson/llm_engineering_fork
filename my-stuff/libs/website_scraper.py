
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class WebsiteScraper:
    """
    A utility class to represent a Website that we have scraped using Selenium
    """
    
    def __init__(self, url, headless=True, wait_timeout=10):
        self.url = url
        self.headless = headless
        self.wait_timeout = wait_timeout
        self.title = ""
        self.text = ""
        self.links = []
        self.body = ""
        
    def scrape(self):
        """Scrape the website and extract title, text content, and links"""
        # Set up Chrome options
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
        
        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=options)
        
        try:
            # Navigate to the website
            driver.get(self.url)
            
            # Wait for the page to load
            WebDriverWait(driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Small delay to ensure page is fully rendered
            time.sleep(1)
            
            # Get page source for BeautifulSoup processing
            page_source = driver.page_source
            self.body = page_source
            
            # Use BeautifulSoup to parse and clean the content
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract title
            self.title = soup.title.string if soup.title else "No title found"
            
            # Extract links
            links = [link.get('href') for link in soup.find_all('a')]
            self.links = [link for link in links if link]
            
            # Clean up irrelevant elements and extract text
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
                
        except Exception as e:
            print(f"Error scraping website: {e}")
            self.title = "Error"
            self.text = f"Failed to scrape: {str(e)}"
            self.links = []
        finally:
            # Close the browser
            driver.quit()
    
    def get_contents(self):
        """Return formatted content similar to BeautifulSoup version"""
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    
    def get_title(self):
        """Return the page title"""
        return self.title
    
    def get_text(self):
        """Return the cleaned text content"""
        return self.text
    
    def get_links(self):
        """Return list of links found on the page"""
        return self.links

# Example usage
if __name__ == "__main__":
    # Create a scraper instance
    scraper = WebsiteScraper("https://www.example.com", headless=True)
    
    # Scrape the website
    print("Scraping website...")
    scraper.scrape()
    
    # Print results
    print("=" * 50)
    print(scraper.get_contents())
    
    print("Links found:")
    for i, link in enumerate(scraper.get_links()[:10], 1):  # Show first 10 links
        print(f"{i}. {link}")
