# -*- coding: utf-8 -*-
"""Removal_of_Non-traditional_publishers(test one).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12u8_KiT9SFogUPt2O3wTVrxlGCOlrKbp
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the exported SimilarWeb CSV file
file_path = "/content/india_leads_q1_2025_domains.csv"  # Update this with your CSV file path
data = pd.read_csv(file_path)

# Assuming the column with website URLs is named 'Website'
websites = data['Website']

# Define keywords to identify non-traditional publishers
exclude_keywords = {
    "OTT": ["streaming", "tv", "video", "netflix", "primevideo", "hotstar"],
    "E-Commerce": ["shop", "cart", "store", "ecommerce", "flipkart", "amazon"],
    "Banking": ["bank", "finance", "loan", "credit", "investment"],
    "Government": ["gov", "nic", "parliament", "ministry"],
    "Other Non-Traditional": ["game", "casino", "betting", "adult", "dating"]
}

def fetch_website_metadata(url):
    """Fetch the website content to analyze for keywords."""
    try:
        response = requests.get(f"https://{url}", timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text().lower()  # Get all text content from the page
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return ""

def is_non_traditional(url):
    """Check if a website matches non-traditional publisher keywords."""
    content = fetch_website_metadata(url)
    for keywords in exclude_keywords.values():
        if any(keyword in content for keyword in keywords):
            return True  # Mark as non-traditional
    return False

# Add a column to flag non-traditional publishers
data['Is_Non_Traditional'] = websites.apply(is_non_traditional)

# Filter out non-traditional publishers
filtered_data = data[~data['Is_Non_Traditional']]

# Save the filtered data to a new CSV file
filtered_data.to_csv("/content/filtered_publishers.csv", index=False)

print("Filtered data saved to 'filtered_publishers.csv'.")

# This is the script for web email scraping

import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

# List of domains to scrape
domains = ["cars24.com","indgovtjobs.in"]

# Regex pattern to extract email addresses
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Function to scrape emails from a single domain
def scrape_emails(domain):
    try:
        # Ensure domain starts with http or https
        if not domain.startswith(('http://', 'https://')):
            domain = 'http://' + domain

        # Make a GET request to fetch the website content
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(domain, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()  # Extract all visible text

        # Use regex to find all email addresses
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Remove duplicates
    except Exception as e:
        print(f"Error scraping {domain}: {e}")
        return []

# Scrape emails for each domain in the list
results = []
for domain in domains:
    print(f"Scraping emails from {domain}...")
    emails = scrape_emails(domain)
    results.append({
        'Domain': domain,
        'Emails': ", ".join(emails) if emails else None
    })

    # Optional: Add a small delay between requests to avoid overwhelming servers
    time.sleep(1)

# Convert the results to a DataFrame
df = pd.DataFrame(results)

# Save the DataFrame to a CSV file
output_file = "scraped_emails.csv"
df.to_csv(output_file, index=False)

print(f"\nEmail scraping completed. Results saved to '{output_file}'.")

!pip install tldextract

!pip install nltk

import nest_asyncio
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
from fuzzywuzzy import fuzz
import spacy
from transformers import pipeline

# Load spaCy model (for semantic similarity)
similarity_model = pipeline("zero-shot-classification")

# Define the extended non-traditional keywords list
NON_TRADITIONAL_KEYWORDS = [
    "e-commerce", "streaming", "finance", "government", "banking", "OTT", "retail",
    "store", "shopping", "checkout", "cart", "buy", "purchase", "products", "sales",
    "offers", "loan", "credit", "insurance", "mortgage", "investments", "startup", "SaaS",
    "platform", "cloud", "B2B", "enterprise", "business", "corporate", "app", "technology",
    "software", "subscription", "telecom", "healthcare", "medical", "pharmacy", "clinic",
    "hospital", "wellness", "education", "university", "school", "research", "study",
    "scholar", "academic", "courses", "training", "degrees", "government services",
    "municipal", "official", "city", "public service", "digital services", "ticketing",
    "gaming", "casino", "betting", "crypto", "NFT", "digital assets", "stream", "video",
    "music", "subscribe", "on-demand", "social", "blog", "forum", "influencer", "content creator",
    "online marketplace", "freelance", "remote work", "gig economy"
]

# Custom headers for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive"
}

# Use a set to track previously fetched websites to avoid redundant requests
fetched_websites = set()

async def fetch_website_metadata(session, url):
    """Fetch the website content to analyze for keywords."""
    if url in fetched_websites:
        return ""

    try:
        async with session.get(f"https://{url}", headers=headers, timeout=5) as response:
            if response.status == 200:
                fetched_websites.add(url)
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")

                # Extract relevant sections for text content (meta description, article content)
                text_content = ""

                # Extract meta description
                meta_description = soup.find("meta", attrs={"name": "description"})
                if meta_description:
                    text_content += meta_description.get("content", "")

                # Extract article content (if exists)
                article_content = soup.find("article")
                if article_content:
                    text_content += article_content.get_text()

                # Fallback: Extract main content
                if not text_content:
                    main_content = soup.find("main")
                    if main_content:
                        text_content += main_content.get_text()

                # Fallback: Just get all text content from the page if no specific sections found
                if not text_content:
                    text_content = soup.get_text()

                return text_content.lower()  # Convert to lowercase for easier comparison
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return ""

def fuzzy_match(keyword, content):
    """Perform fuzzy matching for keywords in content."""
    return fuzz.partial_ratio(keyword.lower(), content) > 70  # Match threshold can be adjusted

def semantic_similarity_check(content, keywords):
    """Perform semantic similarity check using BERT model."""
    for keyword in keywords:
        result = similarity_model(content, candidate_labels=[keyword])
        if result['scores'][0] > 0.75:  # Check if similarity score is greater than 0.75
            return True
    return False

async def is_non_traditional(session, url):
    """Check if a website matches non-traditional publisher keywords."""
    content = await fetch_website_metadata(session, url)

    if content:
        for keyword in NON_TRADITIONAL_KEYWORDS:
            # Fuzzy matching
            if fuzzy_match(keyword, content):
                return True  # Mark as non-traditional

            # Semantic similarity check using spaCy
            if semantic_similarity_check(content, [keyword]):
                return True  # Mark as non-traditional
    return False

async def categorize_publisher(session, url):
    """Categorize website as 'traditional' or 'non-traditional'."""
    if await is_non_traditional(session, url):
        return (url, "non-traditional")
    else:
        return (url, "traditional")

# Allow nested event loops (necessary for environments like Jupyter Notebooks)
nest_asyncio.apply()

websites = ["indgovtjobs.in","tv9bangla.com"]

async def main():
    async with aiohttp.ClientSession() as session:
        # Using asyncio.gather to fetch and categorize websites concurrently
        tasks = [categorize_publisher(session, url) for url in websites]
        categorized_websites = await asyncio.gather(*tasks)

        # Print results in 'domain publisher_type' format
        print("domain publisher_type")
        for domain, publisher_type in categorized_websites:
            print(f"{domain} ; {publisher_type}")

# Run the async main function
await main()

import requests
from bs4 import BeautifulSoup

# Function to fetch website metadata (title, description, keywords, etc.)
def fetch_metadata(url):
    try:
        # Make a GET request to fetch the website content
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            ),
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise exception for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract meta tags for title, description, and keywords
        title = soup.title.string if soup.title else ''
        description = ''
        keywords = ''

        # Extract description and keywords from meta tags
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag and description_tag.get('content'):
            description = description_tag['content']

        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag and keywords_tag.get('content'):
            keywords = keywords_tag['content']

        return {
            'title': title,
            'description': description,
            'keywords': keywords
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata from {url}: {e}")
        return None

# Function to classify website content based on metadata
def classify_website(metadata):
    # Define keywords for traditional and non-traditional publishers
    traditional_keywords = ["news", "media", "journalism", "editorial", "articles", "magazine", "press", "report",
        "opinion", "story", "column", "bulletin", "daily", "journal", "post", "times",
        "tribune", "gazette", "broadcast", "coverage", "headline", "breaking news", "op-ed",
        "publication", "newspaper", "content", "reviews", "interviews", "analysis", "features",
        "reporter", "investigation", "coverage", "exposé", "reviews", "critique"]
    non_traditional_keywords = [
    'ecommerce', 'jobs', 'vacancy','shopping', 'career', 'shop', 'buy', 'product', 'service',
    'online store', 'job portal', 'recruitment', 'career opportunities', 'job listing',
    'employment', 'hiring', 'work from home', 'freelance', 'startup', 'business',
    'fashion', 'retail', 'electronics', 'consumer goods', 'b2b', 'b2c', 'subscription',
    'digital marketplace', 'advertising', 'marketing', 'platform', 'affiliate', 'booking',
    'real estate', 'property', 'travel', 'auto', 'insurance', 'banking', 'fintech',
    'lending', 'crypto', 'blockchain', 'nft', 'crowdfunding', 'auction', 'services', 'food delivery',
    'fitness', 'wellness', 'telemedicine', 'tutoring', 'learning', 'home improvement', 'events',
    'ticketing', 'courses', 'consulting', 'crowdsourcing', 'professional services', 'subscription box'
    ]


    # Check if title, description, or keywords contain relevant term
    title = metadata['title'].lower() if metadata['title'] is not None else ""
    description = metadata['description'].lower() if metadata['description'] is not None else ""
    keywords = metadata['keywords'].lower() if metadata['keywords'] is not None else ""
    content = title + " " + description + " " + keywords

    # Check for traditional publisher
    if any(keyword in content for keyword in traditional_keywords):
        return "Traditional Publisher"

    # Check for non-traditional publisher
    elif any(keyword in content for keyword in non_traditional_keywords):
        return "Non-Traditional Publisher"

    return "Unclassified"

# Function to classify multiple domains
def classify_domains(domains):
    for domain in domains:
        metadata = fetch_metadata(f"https://{domain}")

        if metadata:
            classification = classify_website(metadata)
            print(f"{domain};{classification}")
        else:
            print(f"{domain};Failed to retrieve metadata")

# List of domains to classify
domains = ["ninelineapparel.com"]

# Classify all domains
classify_domains(domains)