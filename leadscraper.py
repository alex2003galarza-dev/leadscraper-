#!/usr/bin/env python3
"""
Illinois Business Lead Scraper
Searches multiple directories for businesses that may need IT services or pentesting
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from datetime import datetime
from urllib.parse import quote_plus
import json

class IllinoisLeadScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.leads = []
        
    def rate_limit(self, min_seconds=2, max_seconds=5):
        """Respectful rate limiting between requests"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def scrape_yellowpages(self, category, location="Illinois"):
        """Scrape Yellow Pages for Illinois businesses"""
        print(f"\n🔍 Searching Yellow Pages for {category} in {location}...")
        
        try:
            # Yellow Pages URL structure
            search_term = quote_plus(category)
            location_term = quote_plus(location)
            url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location_term}"
            
            self.rate_limit()
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = soup.find_all('div', class_='result')
                
                for result in results[:20]:  # Limit to first 20 results per category
                    try:
                        name_elem = result.find('a', class_='business-name')
                        name = name_elem.text.strip() if name_elem else "N/A"
                        
                        phone_elem = result.find('div', class_='phones')
                        phone = phone_elem.text.strip() if phone_elem else "N/A"
                        
                        address_elem = result.find('div', class_='street-address')
                        city_elem = result.find('div', class_='locality')
                        address = ""
                        if address_elem:
                            address = address_elem.text.strip()
                        if city_elem:
                            address += ", " + city_elem.text.strip()
                        
                        # Check for website
                        website_elem = result.find('a', class_='track-visit-website')
                        has_website = "Yes" if website_elem else "No"
                        website = website_elem.get('href', 'N/A') if website_elem else "N/A"
                        
                        lead = {
                            'source': 'YellowPages',
                            'business_name': name,
                            'phone': phone,
                            'address': address,
                            'has_website': has_website,
                            'website': website,
                            'category': category,
                            'state': 'Illinois'
                        }
                        
                        self.leads.append(lead)
                        print(f"  ✓ Found: {name} | Website: {has_website}")
                        
                    except Exception as e:
                        print(f"  ⚠ Error parsing result: {e}")
                        continue
                        
        except Exception as e:
            print(f"  ❌ Error scraping Yellow Pages: {e}")
    
    def scrape_manta(self, category, state="Illinois"):
        """Scrape Manta business directory"""
        print(f"\n🔍 Searching Manta for {category} in {state}...")
        
        try:
            # Manta URL structure
            search_term = quote_plus(category)
            state_code = "IL"  # Illinois
            url = f"https://www.manta.com/search?search={search_term}&state={state_code}"
            
            self.rate_limit()
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = soup.find_all('div', class_='card-body')
                
                for result in results[:20]:
                    try:
                        name_elem = result.find('h3') or result.find('h2')
                        name = name_elem.text.strip() if name_elem else "N/A"
                        
                        phone_elem = result.find('a', href=lambda x: x and 'tel:' in x)
                        phone = phone_elem.text.strip() if phone_elem else "N/A"
                        
                        address_elem = result.find('address') or result.find('p', class_='address')
                        address = address_elem.text.strip() if address_elem else "N/A"
                        
                        # Check for website link
                        website_elem = result.find('a', href=lambda x: x and ('http' in x or 'www' in x))
                        has_website = "Yes" if website_elem else "No"
                        website = website_elem.get('href', 'N/A') if website_elem else "N/A"
                        
                        lead = {
                            'source': 'Manta',
                            'business_name': name,
                            'phone': phone,
                            'address': address,
                            'has_website': has_website,
                            'website': website,
                            'category': category,
                            'state': state
                        }
                        
                        self.leads.append(lead)
                        print(f"  ✓ Found: {name} | Website: {has_website}")
                        
                    except Exception as e:
                        print(f"  ⚠ Error parsing result: {e}")
                        continue
                        
        except Exception as e:
            print(f"  ❌ Error scraping Manta: {e}")
    
    def scrape_superpages(self, category, location="Illinois"):
        """Scrape Superpages directory"""
        print(f"\n🔍 Searching Superpages for {category} in {location}...")
        
        try:
            search_term = quote_plus(category)
            location_term = quote_plus(location)
            url = f"https://www.superpages.com/search?search_terms={search_term}&geo_location_terms={location_term}"
            
            self.rate_limit()
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = soup.find_all('div', class_='listing')
                
                for result in results[:20]:
                    try:
                        name_elem = result.find('a', class_='business-name')
                        name = name_elem.text.strip() if name_elem else "N/A"
                        
                        phone_elem = result.find('span', class_='phone')
                        phone = phone_elem.text.strip() if phone_elem else "N/A"
                        
                        address_elem = result.find('span', class_='street-address')
                        city_elem = result.find('span', class_='locality')
                        address = ""
                        if address_elem:
                            address = address_elem.text.strip()
                        if city_elem:
                            address += ", " + city_elem.text.strip()
                        
                        website_elem = result.find('a', string=lambda x: x and 'website' in x.lower())
                        has_website = "Yes" if website_elem else "No"
                        website = website_elem.get('href', 'N/A') if website_elem else "N/A"
                        
                        lead = {
                            'source': 'Superpages',
                            'business_name': name,
                            'phone': phone,
                            'address': address,
                            'has_website': has_website,
                            'website': website,
                            'category': category,
                            'state': 'Illinois'
                        }
                        
                        self.leads.append(lead)
                        print(f"  ✓ Found: {name} | Website: {has_website}")
                        
                    except Exception as e:
                        print(f"  ⚠ Error parsing result: {e}")
                        continue
                        
        except Exception as e:
            print(f"  ❌ Error scraping Superpages: {e}")
    
    def export_to_csv(self, filename=None):
        """Export leads to CSV file"""
        if not self.leads:
            print("\n❌ No leads to export!")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"illinois_leads_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['source', 'business_name', 'phone', 'address', 
                            'has_website', 'website', 'category', 'state']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.leads)
            
            print(f"\n✅ Exported {len(self.leads)} leads to {filename}")
            
            # Print statistics
            no_website = sum(1 for lead in self.leads if lead['has_website'] == 'No')
            print(f"\n📊 Statistics:")
            print(f"   Total leads: {len(self.leads)}")
            print(f"   Without website: {no_website} ({no_website/len(self.leads)*100:.1f}%)")
            print(f"   With website: {len(self.leads) - no_website}")
            
        except Exception as e:
            print(f"\n❌ Error exporting to CSV: {e}")
    
    def run_search(self, categories, cities=None):
        """Run the scraper across multiple sources"""
        print("="*60)
        print("Illinois Business Lead Scraper")
        print("="*60)
        
        for category in categories:
            print(f"\n{'='*60}")
            print(f"Searching for: {category}")
            print(f"{'='*60}")
            
            # Search all directories
            self.scrape_yellowpages(category)
            self.scrape_manta(category)
            self.scrape_superpages(category)
        
        # Remove duplicates based on business name and phone
        print(f"\n🔄 Removing duplicates...")
        seen = set()
        unique_leads = []
        for lead in self.leads:
            identifier = (lead['business_name'].lower(), lead['phone'])
            if identifier not in seen and lead['business_name'] != "N/A":
                seen.add(identifier)
                unique_leads.append(lead)
        
        self.leads = unique_leads
        print(f"✓ Kept {len(self.leads)} unique leads")


def main():
    """Main function to run the scraper"""
    
    # Categories of businesses that typically need IT services/pentesting
    categories = [
        "medical offices",
        "law firms",
        "accounting firms",
        "dental offices",
        "insurance agencies",
        "financial advisors",
        "real estate offices",
        "manufacturing companies",
        "retail stores",
        "restaurants"
    ]
    
    print("\n🎯 Target Categories for IT/Pentesting Services:")
    for i, cat in enumerate(categories, 1):
        print(f"   {i}. {cat}")
    
    print("\n" + "="*60)
    response = input("Press Enter to start scraping, or type custom categories (comma-separated): ")
    
    if response.strip():
        categories = [cat.strip() for cat in response.split(',')]
    
    scraper = IllinoisLeadScraper()
    scraper.run_search(categories)
    scraper.export_to_csv()
    
    print("\n" + "="*60)
    print("✅ Scraping complete!")
    print("="*60)


if __name__ == "__main__":
    main()
