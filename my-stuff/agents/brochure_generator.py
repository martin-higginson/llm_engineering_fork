import json
import libs.website_scraper as ws
from IPython.display import Markdown


class BrochureGenerator:
    """
    A standalone class for generating company brochures from website content.
    
    This class scrapes a company's website, identifies relevant links, and uses
    AI to generate a marketing brochure suitable for customers, investors, and recruits.
    """
    
    def __init__(self, site_client, link_client, 
                 brochure_domain="company",
                 brochure_target_market="customers, investors and recruits",
                 brochure_details="company culture, customers, careers/jobs",
                 brochure_link_filter="about page, company page, careers page",
                 brochure_links_example=None):
        """
        Initialize the BrochureGenerator with AI clients and configuration.
        
        Args:
            site_client: AI client for generating brochure content
            link_client: AI client for extracting relevant links
            brochure_domain (str): Type of organization (default: "company")
            brochure_target_market (str): Target audience (default: "customers, investors and recruits")
            brochure_details (str): Specific details to include (default: "company culture, customers, careers/jobs")
            brochure_link_filter (str): Types of links to look for (default: "about page, company page, careers page")
            brochure_links_example (str, optional): Custom JSON example for link extraction
        """
        self.site_client = site_client
        self.link_client = link_client
        
        # Configuration for brochure generation
        self.brochure_domain = brochure_domain
        self.brochure_target_market = brochure_target_market
        self.brochure_details = brochure_details
        self.brochure_link_filter = brochure_link_filter
        
        # Set default or custom JSON example for link extraction
        if brochure_links_example is None:
            self.brochure_links_example = """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""
        else:
            self.brochure_links_example = brochure_links_example
        
        # Set up system prompts
        self._setup_system_prompts()
    
    def _setup_system_prompts(self):
        """Set up the system prompts for both AI clients."""
        # System prompt for brochure generation
        system_prompt = f"You are an assistant that analyzes the contents of several relevant pages from a {self.brochure_domain} website " \
                       f"and creates a short brochure about the company for prospective {self.brochure_target_market}. Respond in markdown. " \
                       f"Include details of company {self.brochure_details} if you have the information."
        
        self.site_client.set_system_message(system_prompt)
        
        # System prompt for link extraction
        link_system_prompt = f"You are provided with a list of links found on a webpage. " \
                           f"You are able to decide which of the links would be most relevant to include in a brochure about the {self.brochure_domain}, " \
                           f"such as links to {self.brochure_link_filter}.\n"
        link_system_prompt += "You should respond in JSON and ONLY JSON as in this example:"
        link_system_prompt += self.brochure_links_example
        
        self.link_client.set_system_message(link_system_prompt)
    
    def _get_links_user_prompt(self, scraper):
        """
        Generate the user prompt for link extraction.
        
        Args:
            scraper: WebsiteScraper instance with scraped content
            
        Returns:
            str: Formatted user prompt for link extraction
        """
        user_prompt = f"Here is the list of links on the website of {scraper.url} - "
        user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. " \
                      "Do not include Terms of Service, Privacy, email links.\n"
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += "\n".join(scraper.links)
        return user_prompt
    
    def get_relevant_links(self, url):
        """
        Extract relevant links from a website for brochure generation.
        
        Args:
            url (str): The website URL to analyze
            
        Returns:
            dict: Dictionary containing relevant links with their types
        """
        scraper = ws.WebsiteScraper(url, headless=False)
        scraper.scrape()
        result = self.link_client.chat(self._get_links_user_prompt(scraper), [])
        
        # Add proper error handling for JSON parsing
        if not result or not result.strip():
            print("Warning: Empty response from chat client")
            return {"links": []}
        
        try:
            # Clean the result - remove any markdown code blocks if present
            clean_result = result.strip()
            if clean_result.startswith('```json'):
                clean_result = clean_result.replace('```json', '').replace('```', '').strip()
            elif clean_result.startswith('```'):
                clean_result = clean_result.replace('```', '').strip()
            
            parsed_json = json.loads(clean_result)
            return parsed_json
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response was: {repr(result)}")
            # Return a fallback structure
            return {"links": []}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"links": []}
    
    def _get_all_website_details(self, url):
        """
        Scrape content from the main URL and all relevant linked pages.
        
        Args:
            url (str): The main website URL
            
        Returns:
            str: Combined content from all relevant pages
        """
        result = "Landing page:\n"
        scraper = ws.WebsiteScraper(url, headless=False)
        scraper.scrape()
        result += scraper.get_contents()
        
        links = self.get_relevant_links(url)
        print("Found links:", links)
        
        # Add error handling for missing or invalid links structure
        if "links" not in links:
            print("Warning: No 'links' key found in response")
            return result
        
        for link in links["links"]:
            if "type" in link and "url" in link:
                result += f"\n\n{link['type']}\n"
                scraper = ws.WebsiteScraper(link["url"], headless=False)
                scraper.scrape()
                result += scraper.get_contents()
            else:
                print(f"Warning: Invalid link structure: {link}")
        
        return result
    
    def _get_brochure_user_prompt(self, company_name, url):
        """
        Generate the user prompt for brochure creation.
        
        Args:
            company_name (str): Name of the company
            url (str): Company website URL
            
        Returns:
            str: Formatted user prompt for brochure generation
        """
        user_prompt = f"You are looking at a company called: {company_name}\n"
        user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
        user_prompt += self._get_all_website_details(url)
        user_prompt = user_prompt[:5_000]  # Truncate if more than 5,000 characters
        return user_prompt
    
    def generate_brochure(self, company_name, url):
        """
        Generate a complete brochure for a company based on their website.
        
        Args:
            company_name (str): Name of the company
            url (str): Company website URL
            
        Returns:
            Markdown: Formatted brochure content, or None if generation fails
        """
        try:
            result = self.site_client.chat(self._get_brochure_user_prompt(company_name, url), [])
            if result:
                return Markdown(result)
            else:
                print("Error: Empty response from chat client")
                return None
        except Exception as e:
            print(f"Error creating brochure: {e}")
            return None
    
    def update_configuration(self, domain=None, target_market=None, details=None, link_filter=None, links_example=None):
        """
        Update the brochure generation configuration.
        
        Args:
            domain (str, optional): Type of organization (e.g., "company", "nonprofit")
            target_market (str, optional): Target audience for the brochure
            details (str, optional): Specific details to include
            link_filter (str, optional): Types of links to look for
            links_example (str, optional): Custom JSON example for link extraction
        """
        if domain:
            self.brochure_domain = domain
        if target_market:
            self.brochure_target_market = target_market
        if details:
            self.brochure_details = details
        if link_filter:
            self.brochure_link_filter = link_filter
        if links_example:
            self.brochure_links_example = links_example
        
        # Update system prompts with new configuration
        self._setup_system_prompts()


# # Example usage
# if __name__ == "__main__":
#     # Create AI clients
#     site_client = oai_chat.OpenAIChatClient(temperature=0.5, max_tokens=2000)
#     link_client = oai_chat.OpenAIChatClient(temperature=0.5, max_tokens=2000)
#
#     # Basic usage with defaults
#     generator = BrochureGenerator(site_client, link_client)
#
#     # Custom configuration example
#     generator_nonprofit = BrochureGenerator(
#         site_client,
#         link_client,
#         brochure_domain="nonprofit organization",
#         brochure_target_market="donors, volunteers and beneficiaries",
#         brochure_details="mission, impact, volunteer opportunities, donation methods",
#         brochure_link_filter="about page, mission page, volunteer page, donate page",
#         brochure_links_example="""
# {
#     "links": [
#         {"type": "about page", "url": "https://full.url/goes/here/about"},
#         {"type": "mission page", "url": "https://another.full.url/mission"},
#         {"type": "volunteer page", "url": "https://another.full.url/volunteer"}
#     ]
# }
# """
#     )
#
#     # Generate a brochure
#     company_name = "Example Company"
#     company_url = "https://example.com"
#
#     brochure = generator.generate_brochure(company_name, company_url)
#     if brochure:
#         print("Brochure generated successfully!")
#     else:
#         print("Failed to generate brochure.")
