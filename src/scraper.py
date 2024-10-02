import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'news_sites.json'
OUTPUT_DIR = Path(__file__).parent.parent / 'output'

def load_news_sites(config_path=CONFIG_PATH):
    """Load news sites from the JSON config file."""
    with open(config_path, 'r') as file:
        return json.load(file)

def scrape_site(site):
    """Scrape headlines from a given news site."""
    try:
        response = requests.get(site['url'])
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {site['name']}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []
    
    # Fetch titles and links based on the CSS selectors defined in the config
    titles = soup.select(site['title_css_selector'])
    links = soup.select(site['link_css_selector'])
    
    for title_elem, link_elem in zip(titles, links):
        headline = title_elem.get_text(strip=True)
        link = link_elem['href'] if link_elem['href'].startswith('http') else f"https://{site['domain']}{link_elem['href']}"
        
        headlines.append({
            'headline': headline,
            'link': link,
            'category': site.get('category', 'General'),
            'source': site['name'],
            'timestamp': datetime.utcnow().isoformat()
        })
        
    print(f"Scraped {len(headlines)} headlines from {site['name']}.")
    return headlines

def save_headlines(headlines, output_dir=OUTPUT_DIR):
    """Save scraped headlines to a JSON file."""
    now = datetime.utcnow()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H-%M-%S')
    dir_path = output_dir / date_str
    dir_path.mkdir(parents=True, exist_ok=True)
    
    file_path = dir_path / f"{time_str}_headlines.json"
    with open(file_path, 'w') as file:
        json.dump(headlines, file, indent=4)
    print(f"Saved headlines to {file_path}.")

def main():
    """Main function to run the scraper."""
    news_sites = load_news_sites()
    all_headlines = []
    
    for site in news_sites:
        headlines = scrape_site(site)
        all_headlines.extend(headlines)
    
    if all_headlines:
        save_headlines(all_headlines)
        print(f"Total headlines saved: {len(all_headlines)}")
    else:
        print("No headlines found.")

if __name__ == "__main__":
    main()
