# tests/test_scraper.py

import unittest
from src.scraper import scrape_site

class TestScraper(unittest.TestCase):
    def test_scrape_site_invalid_url(self):
        site = {
            "name": "Invalid Site",
            "url": "https://www.invalidsite.com",
            "css_selector": "h3",
            "domain": "invalidsite.com",
            "category": "Test"
        }
        with self.assertRaises(Exception):
            scrape_site(site)
    
    def test_scrape_site_valid(self):
        site = {
            "name": "BBC News",
            "url": "https://www.bbc.com/news",
            "css_selector": "h3.gs-c-promo-heading__title",
            "domain": "bbc.com",
            "category": "General"
        }
        headlines = scrape_site(site)
        self.assertIsInstance(headlines, list)
        if headlines:
            first = headlines[0]
            self.assertIn('headline', first)
            self.assertIn('link', first)
            self.assertIn('category', first)
            self.assertIn('source', first)
            self.assertIn('timestamp', first)

if __name__ == '__main__':
    unittest.main()
