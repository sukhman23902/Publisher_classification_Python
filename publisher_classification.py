# -*- coding: utf-8 -*-
"""Publisher classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nSyQCda4awXgZvWsxCxFygwXPAqq3pnE
"""

import spacy
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import whois
import zstandard as zstd

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Expanded keyword lists
NEWS_KEYWORDS = [
    "article", "news", "journal", "magazine", "press", "release",
    "editorial", "headline", "report", "jobs", "elections", "politics",
    "breaking news", "regional news", "updates", "live"
]
FORMAL_WORDS = ["therefore", "accordingly", "consequently", "subsequently", "thus", "hence"]

def analyze_domain(domain):
    try:
        # WHOIS information
        w = whois.whois(domain)
        domain_creation_date = (
            min(w.creation_date) if isinstance(w.creation_date, list) else w.creation_date
        )
        if not domain_creation_date:
            raise ValueError("WHOIS data does not contain a valid creation date.")
        domain_age = (datetime.now() - domain_creation_date).days

        # Website content
        url = f"https://{domain}/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            ),
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Handle Zstandard compression if necessary
        if response.headers.get("Content-Encoding") == "zstd":
            dctx = zstd.ZstdDecompressor()
            soup = BeautifulSoup(dctx.decompress(response.content), "html.parser")
        else:
            soup = BeautifulSoup(response.content, "html.parser")

        # Extract text content
        text = soup.get_text()
        doc = nlp(text)

        # Debugging: Log content
        print(f"\nAnalyzing {domain} - First 500 characters:\n{text[:500]}")

        # Analyze keywords and writing style
        keyword_count = sum([token.text.lower() in NEWS_KEYWORDS for token in doc])
        formal_count = sum([token.text.lower() in FORMAL_WORDS for token in doc])

        # Debugging: Log feature counts
        print(f"{domain} - Keyword Count: {keyword_count}, Formal Count: {formal_count}")

        # Sentiment analysis
        sentiment = TextBlob(text).sentiment.polarity

        # Check for journalistic elements in HTML
        has_articles = bool(soup.find("article"))
        has_bylines = bool(soup.find("meta", {"name": "author"}))
        has_datelines = bool(soup.find("meta", {"name": "date"}))
        has_sections = any(
            header in text.lower() for header in ["world news", "sports", "entertainment", "business", "jobs"]
        )

        # Debugging: Log HTML features
        print(f"{domain} - Articles: {has_articles}, Bylines: {has_bylines}, Sections: {has_sections}")

        # Classification logic
        if (
            domain_age > 365 and  # At least 1 year old
            (keyword_count >= 2 or has_sections) and  # Keywords or sections
            formal_count >= 1 and  # Some formal writing
            sentiment >= -0.2 and  # Neutral to positive sentiment
            (has_articles or has_bylines or has_sections)  # Journalistic structure
        ):
            return "Traditional Publisher"
        else:
            return "Non-Traditional Publisher"

    except (ValueError, requests.exceptions.RequestException, Exception) as e:
        print(f"Error analyzing {domain}: {e}")
        return "Unknown"

# Example usage
if __name__ == "__main__":
    domains = ["indgovtjobs.in", "tv9bangla.com", "theprint.in", "eisamay.com", "bizzbuzz.news"]

    for domain in domains:
        classification = analyze_domain(domain)
        print(f"{domain}: {classification}")

import spacy
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import whois
import zstandard as zstd

# Load spaCy model (replace 'en_core_web_sm' with a larger model if needed)
nlp = spacy.load("en_core_web_sm")

def analyze_domain(domain):
    """
    Analyzes a domain to classify it as a traditional or non-traditional publisher.

    Args:
        domain: The root domain to analyze.

    Returns:
        str: "Traditional Publisher", "Non-Traditional Publisher", or "Unknown"
    """

    try:
        # 1. Domain Age and WHOIS Information
        w = whois.whois(domain)

        # Handle multiple creation dates or missing creation date
        if isinstance(w.creation_date, list):
            domain_creation_date = min(w.creation_date)  # Take the earliest creation date
        else:
            domain_creation_date = w.creation_date

        if not domain_creation_date:
            raise ValueError("WHOIS data does not contain a valid creation date.")

        domain_age = (datetime.now() - domain_creation_date).days

        # 2. Website Content Analysis
        url = f"https://{domain}/"

        # Set custom headers to mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Connection": "keep-alive"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Handle Zstandard compression if present
        if response.headers.get("Content-Encoding") == "zstd":
            dctx = zstd.ZstdDecompressor()
            decompressed_content = dctx.decompress(response.content)
            soup = BeautifulSoup(decompressed_content, "html.parser")
        else:
            soup = BeautifulSoup(response.content, "html.parser")

        # Extract text content
        text = soup.get_text()

        # 3. Text Analysis
        doc = nlp(text)

        # Keyword analysis (example: find common keywords in publisher articles)
        keywords = ["news", "media", "journalism", "editorial", "articles", "magazine", "press", "report",
        "opinion", "story", "column", "bulletin", "daily", "journal", "post", "times",
        "tribune", "gazette", "broadcast", "coverage", "headline", "breaking news", "op-ed",
        "publication", "newspaper", "content", "reviews", "interviews", "analysis", "features",
        "reporter", "investigation", "coverage", "exposé", "reviews", "critique"]

        keyword_count = sum([token.text.lower() in keywords for token in doc])

        # Writing style analysis (simplified)
        formal_words = ["therefore", "accordingly", "consequently", "subsequently"]
        formal_count = sum([token.text.lower() in formal_words for token in doc])

        # Sentiment analysis
        sentiment = TextBlob(text).sentiment.polarity

        # 4. Journalistic Elements
        bylines = soup.find_all("meta", {"name": "author"})
        bylines = soup.find_all("meta", {"name": "og:image"})
        bylines = soup.find_all("meta", {"name": "og:description"})
        bylines = soup.find_all("meta", {"name": "og:site_name"})
        datelines = soup.find_all("meta", {"name": "date"})
        sources = soup.find_all("cite")

        # Combine features for classification (example: simplified logic)
        if (
            keyword_count > 2
            and formal_count > 1
            and sentiment >= 0.1
            and len(bylines) > 0
            and len(datelines) > 0
            and len(sources) > 0
            and domain_age > 365  # Consider age as a factor
        ):
            return "Traditional Publisher"
        else:
            return "Non-Traditional Publisher"

    except (ValueError, requests.exceptions.RequestException, Exception) as e:
        print(f"Error analyzing {domain}: {e}")
        return "Unknown"

# Example usage
if __name__ == "__main__":

    domains = ["indgovtjobs.in","tv9bangla.com"]

    for domain in domains:
        classification = analyze_domain(domain)
        print(f"{domain}: {classification}")

!pip install tldextract

import pandas as pd
import tldextract
import requests
from bs4 import BeautifulSoup

# Step 1: Input List of Domains
domains = ["nytimes.com", "amazon.com", "gov.uk", "hulu.com", "forbes.com", "walmart.com"]

# Optional: Load domains from a CSV file
# domains = pd.read_csv('domains.csv')['Domain'].tolist()

# Create a DataFrame
df = pd.DataFrame(domains, columns=["Domain"])

# Step 2: Define Keywords for Classification
TRADITIONAL_KEYWORDS = [
    "news", "media", "press", "journal", "magazine",
    "gazette", "bulletin", "times", "chronicle",
    "tribune", "reporter", "observer", "herald",
    "daily", "post", "standard", "review", "courier",
    "weekly", "monthly", "editorial", "periodical", "publisher"
]

TRADITIONAL_KEYWORDS = [
    "news", "media", "press", "journal", "magazine",
    "gazette", "bulletin", "times", "chronicle",
    "tribune", "reporter", "observer", "herald",
    "daily", "post", "standard", "review", "courier",
    "weekly", "monthly", "editorial", "periodical", "publisher"
]


# Step 3: Define Rule-Based Classification Function
def classify_domain(domain):
    extracted = tldextract.extract(domain)
    root_domain = extracted.domain.lower()

    # Check Traditional Keywords
    if any(keyword in root_domain for keyword in TRADITIONAL_KEYWORDS):
        return "Traditional"

    # Check Non-Traditional Keywords
    if any(keyword in root_domain for keyword in NON_TRADITIONAL_KEYWORDS):
        return "Non-Traditional"

    return "Unknown"

# Step 4: Fetch Metadata for Enhancement
def fetch_metadata(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No Title"
        return title.lower()
    except Exception as e:
        return "Error"

# Step 5: Enhanced Classification with Metadata
def classify_domain_with_metadata(domain, metadata):
    # Check metadata for keywords
    if any(keyword in metadata for keyword in TRADITIONAL_KEYWORDS):
        return "Traditional"
    if any(keyword in metadata for keyword in NON_TRADITIONAL_KEYWORDS):
        return "Non-Traditional"
    return "Unknown"

# Step 6: Hybrid Classification
def hybrid_classification(domain):
    basic_classification = classify_domain(domain)
    if basic_classification == "Unknown":
        metadata = fetch_metadata(domain)
        return classify_domain_with_metadata(domain, metadata)
    return basic_classification

# Apply Classification
df["Basic Classification"] = df["Domain"].apply(classify_domain)
df["Metadata"] = df["Domain"].apply(fetch_metadata)  # Optional step for metadata fetching
df["Enhanced Classification"] = df.apply(
    lambda x: classify_domain_with_metadata(x["Domain"], x["Metadata"]), axis=1
)
df["Final Classification"] = df["Domain"].apply(hybrid_classification)

# Step 7: Output Results
print(df)

# Save Results to a CSV
df.to_csv("classified_domains.csv", index=False)

!pip install transformers

import requests
from transformers import pipeline
from bs4 import BeautifulSoup

# Load the GPT-J model from Hugging Face
generator = pipeline('text-generation', model='KoboldAI/GPT-J-6B-Shinen')

# Function to fetch website content
def fetch_website_content(url):
    try:
        # Make a GET request to fetch the website content
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content from <p> tags (common for article text)
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None

# Function to classify website content using GPT-J
def classify_content(content):
    # Ensure the input content length is manageable
    content = content[:2000]  # Limit the input size to avoid API errors

    prompt = f"Classify the following website content into one of the following categories: Traditional Publisher (e.g. news outlets, media), or Non-Traditional Publisher (e.g. ecommerce, jobs, streaming). Content: {content}"

    try:
        # Generate response from GPT-J model
        response = generator(prompt, max_length=1000, num_return_sequences=1)
        classification = response[0]['generated_text']

        # Check for classification response, remove excess text
        if "Traditional Publisher" in classification:
            return "Traditional Publisher"
        elif "Non-Traditional Publisher" in classification:
            return "Non-Traditional Publisher"
        else:
            return "Unclassified"
    except Exception as e:
        print(f"Error classifying content: {e}")
        return "Unclassified"

# Function to classify multiple domains
def classify_domains(domains):
    for domain in domains:
        print(f"Classifying domain: {domain}")
        content = fetch_website_content(f"https://{domain}")

        if content:
            classification = classify_content(content)
            print(f"Domain: {domain} - Classification: {classification}")
        else:
            print(f"Domain: {domain} - Failed to retrieve content")

# List of domains to classify
domains = [
    "nytimes.com", "amazon.com"
    # Add more domains as needed
]

# Classify all domains
classify_domains(domains)

# final and main one - created on - 21 Feb, 2025
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urljoin

# Keywords for classification
traditional_keywords = ["news", "media", "journalism", "editorial", "articles", "magazine", "press", "report",
                        "opinion", "story", "column", "bulletin", "daily", "journal", "post", "times",
                        "tribune", "gazette", "broadcast", "coverage", "headline", "breaking news", "op-ed",
                        "publication", "newspaper", "content", "reviews", "interviews", "analysis", "features",
                        "reporter", "investigation", "coverage", "exposé", "reviews", "critique"]

non_traditional_keywords = [
    'ecommerce', 'jobs', 'vacancy', 'shopping', 'career', 'shop', 'buy', 'product', 'service',
    'online store', 'job portal', 'recruitment', 'career opportunities', 'job listing',
    'employment', 'hiring', 'work from home', 'freelance', 'startup', 'business',
    'fashion', 'retail', 'electronics', 'consumer goods', 'b2b', 'b2c', 'subscription',
    'digital marketplace', 'advertising', 'marketing', 'platform', 'affiliate', 'booking',
    'real estate', 'property', 'travel', 'auto', 'insurance', 'banking', 'fintech',
    'lending', 'crypto', 'blockchain', 'nft', 'crowdfunding', 'auction', 'services', 'food delivery',
    'fitness', 'wellness', 'telemedicine', 'tutoring', 'learning', 'home improvement', 'events',
    'ticketing', 'courses', 'consulting', 'crowdsourcing', 'professional services', 'subscription box'
]

# Function to fetch metadata from a webpage
def fetch_metadata(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract metadata
        metadata = {
            'title': soup.title.string if soup.title else None,
            'description': None,
            'keywords': None,
            'h1': soup.h1.text if soup.h1 else None,
            'h2': [h2.text for h2 in soup.find_all('h2')],
            'links': [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        }

        # Extract description
        description = soup.find('meta', attrs={'name': 'description'}) or \
                      soup.find('meta', attrs={'property': 'og:description'}) or \
                      soup.find('meta', attrs={'name': 'twitter:description'})
        if description:
            metadata['description'] = description.get('content')

        # Extract keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if keywords:
            metadata['keywords'] = keywords.get('content')

        return metadata
    except Exception as e:
        print(f"Error fetching metadata from {url}: {e}")
        return None

# Function to classify publisher
def classify_publisher(metadata):
    if not metadata:
        return "Unknown"

    text = " ".join([str(metadata[key]) for key in metadata if metadata[key]])
    traditional_score = sum(keyword in text.lower() for keyword in traditional_keywords)
    non_traditional_score = sum(keyword in text.lower() for keyword in non_traditional_keywords)

    if traditional_score > non_traditional_score:
        return "Traditional Publisher"
    elif non_traditional_score > traditional_score:
        return "Non-Traditional Publisher"
    else:
        return "Unknown"

# Main function to process domains
def process_domains(domains):
    for domain in domains:
        print(f"Processing domain: {domain}")
        homepage_url = f"https://{domain}"
        homepage_metadata = fetch_metadata(homepage_url)

        if homepage_metadata:
            print("Homepage Metadata:")
            print(homepage_metadata)

            # Check for article pages
            article_metadata = []
            for link in homepage_metadata['links']:
                if any(keyword in link.lower() for keyword in ['article', 'post', 'blog']):
                    print(f"Fetching metadata from article page: {link}")
                    article_metadata.append(fetch_metadata(link))

            # Combine all metadata for classification
            all_metadata = [homepage_metadata] + article_metadata
            combined_metadata = {key: " ".join(str(m[key]) for m in all_metadata if m and key in m) for key in homepage_metadata}

            # Classify publisher
            classification = classify_publisher(combined_metadata)
            print(f"Classification: {classification}")
        print("-" * 50)

# Example usage
if __name__ == "__main__":
    domains = ["amazon.com"]  # Replace with your list of domains
    process_domains(domains)

import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin

# --- User Agents List ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/89.0",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
]

def fetch_site_metadata(domain):
    """
    Fetches metadata (title, description, image) from a given domain.

    Args:
        domain (str): The domain name (e.g., "example.com").

    Returns:
        dict: A dictionary containing the site's metadata, or None if an error occurs.
    """
    metadata = {
        "title": "Not Found",
        "description": "Not Found",
        "image": "Not Found",
    }
    try:
        # Construct URL, ensure it starts with http or https
        if not domain.startswith(('http://', 'https://')):
            url = 'https://' + domain
        else:
            url = domain

        # Choose a random User-Agent
        user_agent = random.choice(USER_AGENTS)
        headers = {'User-Agent': user_agent}

        # Make the request
        response = requests.get(url, headers=headers, timeout=10) # Added timeout for robustness
        print(f"Request Status for {domain}: {response.status_code} - {response.reason}") # Print status code
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        print(f"--- Content received from {domain} (first 500 chars): ---") # Print received content snippet
        print(response.content[:500].decode('utf-8', errors='ignore')) # Decode and print first 500 chars, handle potential decode errors

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Title ---
        title_tag = soup.find('title')
        if title_tag:
            metadata["title"] = title_tag.text.strip()

        # --- Description ---
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag:
            metadata["description"] = description_tag.get('content', 'Not Found').strip()
        else:
            # Fallback to og:description if description meta tag is not found
            og_description_tag = soup.find('meta',  attrs={'property': 'og:description'})
            if og_description_tag:
                metadata["description"] = og_description_tag.get('content', 'Not Found').strip()

        # --- Image ---
        image_url = None
        # 1. Check for og:image
        og_image_tag = soup.find('meta', attrs={'property': 'og:image'})
        if og_image_tag:
            image_url = og_image_tag.get('content')
        else:
            # 2. Check for link[rel='image_src'] (older approach, less common)
            image_src_link = soup.find('link', rel='image_src')
            if image_src_link:
                image_url = image_src_link.get('href')
            else:
                # 3. Check for link[rel='icon'] or link[rel='shortcut icon'] and favicon
                favicon_link = soup.find('link', rel="icon") or soup.find('link', rel="shortcut icon")
                if favicon_link:
                    image_url = favicon_link.get('href')
                else:
                    # 4. As a last resort, try to construct favicon URL from the domain root
                    image_url = urljoin(url, '/favicon.ico') # urljoin to handle relative paths

        if image_url:
             metadata["image"] = urljoin(url, image_url) # Ensure image URL is absolute


        return metadata

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {domain}: {e}")
        return None
    except Exception as e:
        print(f"Error processing {domain}: {e}")
        return None

def main():
    # --- Define your list of domains here ---
    domains = ["ninelineapparel.com"] # Add your domains in this list

    print("--- Website Metadata Fetcher ---")
    for domain in domains:
        print(f"\nFetching metadata for: {domain}")
        site_data = fetch_site_metadata(domain)
        if site_data:
            print("--- Metadata ---")
            print(f"  Title:       {site_data['title']}")
            print(f"  Description: {site_data['description']}")
            print(f"  Image:       {site_data['image']}")
        else:
            print("Failed to fetch metadata.")

if __name__ == "__main__":
    main()

!pip install requests beautifulsoup4 fake-useragent