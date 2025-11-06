import libs.llama_chat_basic as llama_chat
import libs.open_ai_chat_basic as oai_chat
import agents.brochure_generator as bga

# site_client = llama_chat.LlamaChatClient()
# link_client = llama_chat.LlamaChatClient()

site_client = oai_chat.OpenAIChatClient(temperature=0.5, max_tokens=2000)
link_client = oai_chat.OpenAIChatClient(temperature=0.5, max_tokens=2000)


#####
# Brochure GEN
#####
#
# Basic usage with defaults
# generator = bga.BrochureGenerator(site_client, link_client)
#
# # Custom configuration example
generator = bga.BrochureGenerator(
    site_client,
    link_client,
    brochure_domain="author",
    brochure_target_market="readers, reviewers",
    brochure_details="books, outlets",
    brochure_link_filter="about page, all books, books",
    brochure_links_example="""
{
"links": [
    {"type": "about page", "url": "https://full.url/goes/here/about"},
    {"type": "all books", "url": "https://another.full.url/all_books"},
    {"type": "books", "url": "https://another.full.url/books"}
]
}
"""
)

# # Generate a brochure
# company_name = "Vumatel"
# company_url = "https://vumatel.co.za"
#
brochure = generator.generate_brochure("L Higginson", "https://www.facebook.com/p/L-Higginson-61552388242364/")
if brochure:
    print(brochure.data)
else:
    print("Failed to generate brochure.")


##########
#   Website summariser ??
#########


