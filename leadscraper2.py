#!/usr/bin/env python3
"""
Illinois Business Lead Scraper v2.0
Uses more reliable methods to find businesses that need IT services
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from datetime import datetime
from urllib.parse import quote_plus, urlencode
import json
import re

class IllinoisLeadScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.leads = []
        
    def rate_limit(self, min_seconds=3, max_seconds=6):
        """Respectful rate limiting between requests"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def scrape_yellowpages_new(self, category, location="Illinois"):
        """Scrape Yellow Pages with updated selectors"""
        print(f"\n🔍 Searching Yellow Pages for {category} in {location}...")
        
        try:
            search_term = quote_plus(category)
            location_term = quote_plus(location)
            url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location_term}"
            
            print(f"   URL: {url}")
            self.rate_limit()
            response = self.session.get(url, timeout=15)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try multiple possible selectors
                results = (soup.find_all('div', class_='result') or 
                          soup.find_all('div', class_='search-results') or
                          soup.find_all('div', class_='organic'))
                
                print(f"   Found {len(results)} potential results")
                
                if len(results) == 0:
                    # Try finding any div with business info
                    results = soup.find_all('div', attrs={'data-business-name': True})
                
                for idx, result in enumerate(results[:20]):
                    try:
                        # Try multiple ways to extract business name
                        name = None
                        name_elem = (result.find('a', class_='business-name') or
                                   result.find('h2', class_='n') or
                                   result.find('a', class_='listing-title') or
                                   result.get('data-business-name'))
                        
                        if name_elem:
                            if isinstance(name_elem, str):
                                name = name_elem
                            else:
                                name = name_elem.text.strip()
                        
                        if not name or name == "N/A":
                            continue
                        
                        # Try multiple ways to extract phone
                        phone = "N/A"
                        phone_elem = (result.find('div', class_='phones') or
                                    result.find('div', class_='phone') or
                                    result.find('a', href=re.compile(r'tel:')))
                        
                        if phone_elem:
                            phone = phone_elem.text.strip() if hasattr(phone_elem, 'text') else phone_elem.get('href', '').replace('tel:', '')
                        
                        # Extract address
                        address = "N/A"
                        address_elem = (result.find('div', class_='street-address') or
                                      result.find('span', class_='street-address') or
                                      result.find('div', class_='adr'))
                        
                        if address_elem:
                            address = address_elem.text.strip()
                            city_elem = result.find('div', class_='locality')
                            if city_elem:
                                address += ", " + city_elem.text.strip()
                        
                        # Check for website
                        website_elem = result.find('a', class_='track-visit-website') or result.find('a', string=re.compile(r'website', re.I))
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
                        print(f"  ✓ Found: {name} | Phone: {phone} | Website: {has_website}")
                        
                    except Exception as e:
                        print(f"  ⚠ Error parsing result {idx}: {e}")
                        continue
            else:
                print(f"  ❌ Failed with status code: {response.status_code}")
                        
        except Exception as e:
            print(f"  ❌ Error scraping Yellow Pages: {e}")
    
    def scrape_yelp(self, category, location="Illinois"):
        """Scrape Yelp for businesses"""
        print(f"\n🔍 Searching Yelp for {category} in {location}...")
        
        try:
            # Yelp search URL
            search_term = quote_plus(category)
            url = f"https://www.yelp.com/search?find_desc={search_term}&find_loc={location}"
            
            print(f"   URL: {url}")
            self.rate_limit()
            response = self.session.get(url, timeout=15)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for business listings
                results = soup.find_all('div', attrs={'data-testid': 'serp-ia-card'}) or soup.find_all('li', class_=re.compile(r'.*lemon.*'))
                
                print(f"   Found {len(results)} potential results")
                
                for idx, result in enumerate(results[:15]):
                    try:
                        # Extract business name
                        name_elem = result.find('a', class_=re.compile(r'.*businessname.*')) or result.find('h3') or result.find('h2')
                        name = name_elem.text.strip() if name_elem else None
                        
                        if not name:
                            continue
                        
                        # Extract phone (Yelp often hides this)
                        phone = "Check Yelp"
                        
                        # Extract address
                        address = "N/A"
                        address_elem = result.find('p', class_=re.compile(r'.*address.*')) or result.find('address')
                        if address_elem:
                            address = address_elem.text.strip()
                        
                        # Website check (usually need to visit business page)
                        has_website = "Unknown"
                        website = "N/A"
                        
                        lead = {
                            'source': 'Yelp',
                            'business_name': name,
                            'phone': phone,
                            'address': address,
                            'has_website': has_website,
                            'website': website,
                            'category': category,
                            'state': 'Illinois'
                        }
                        
                        self.leads.append(lead)
                        print(f"  ✓ Found: {name}")
                        
                    except Exception as e:
                        print(f"  ⚠ Error parsing result {idx}: {e}")
                        continue
                        
        except Exception as e:
            print(f"  ❌ Error scraping Yelp: {e}")
    
    def scrape_google_maps_alternative(self, category, city="Chicago"):
        """Alternative approach using a business directory API-style search"""
        print(f"\n🔍 Searching business directories for {category} in {city}, IL...")
        
        try:
            # This is a placeholder for manual/CSV data entry
            # In production, you'd integrate with Google Places API or similar
            print("  ℹ  For best results, consider using Google Places API")
            print("  ℹ  or manually adding known businesses to a CSV file")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    def add_manual_leads(self):
        """Allow manual entry of leads"""
        print("\n" + "="*60)
        print("Manual Lead Entry")
        print("="*60)
        print("Add leads manually (press Enter on business name to skip)")
        
        while True:
            print("\n")
            name = input("Business Name (or press Enter to finish): ").strip()
            if not name:
                break
            
            phone = input("Phone (optional): ").strip() or "N/A"
            address = input("Address (optional): ").strip() or "N/A"
            website = input("Website (optional): ").strip() or "N/A"
            has_website = "Yes" if website != "N/A" else "No"
            category = input("Category/Industry: ").strip() or "N/A"
            
            lead = {
                'source': 'Manual Entry',
                'business_name': name,
                'phone': phone,
                'address': address,
                'has_website': has_website,
                'website': website,
                'category': category,
                'state': 'Illinois'
            }
            
            self.leads.append(lead)
            print(f"✓ Added: {name}")
    
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
            if no_website > 0:
                print(f"   Without website: {no_website} ({no_website/len(self.leads)*100:.1f}%)")
                print(f"   With website: {len(self.leads) - no_website}")
            
        except Exception as e:
            print(f"\n❌ Error exporting to CSV: {e}")
    
    def run_search(self, categories, cities=["Chicago", "Springfield", "Rockford"]):
        """Run the scraper across multiple sources"""
        print("="*60)
        print("Illinois Business Lead Scraper v2.0")
        print("="*60)
        
        for category in categories:
            print(f"\n{'='*60}")
            print(f"Searching for: {category}")
            print(f"{'='*60}")
            
            # Try Yellow Pages with improved parsing
            self.scrape_yellowpages_new(category)
            
            # Try Yelp
            self.scrape_yelp(category)
        
        # Remove duplicates
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
    
    categories = [
        "medical offices",
        "law firms",
        "accounting firms",
        "dental offices",
        "insurance agencies"
    ]
    
    print("\n🎯 Target Categories:")
    for i, cat in enumerate(categories, 1):
        print(f"   {i}. {cat}")
    
    print("\n" + "="*60)
    print("Options:")
    print("1. Press Enter to scrape with default categories")
    print("2. Type custom categories (comma-separated)")
    print("3. Type 'manual' to add leads manually")
    response = input("\nYour choice: ").strip()
    
    scraper = IllinoisLeadScraper()
    
    if response.lower() == 'manual':
        scraper.add_manual_leads()
    else:
        if response and response.lower() != 'manual':
            categories = [cat.strip() for cat in response.split(',')]
        
        scraper.run_search(categories)
    
    if scraper.leads:
        scraper.export_to_csv()
        print("\n" + "="*60)
        print("✅ Scraping complete!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("⚠️  No leads found via scraping")
        print("="*60)
        print("\nPossible reasons:")
        print("- Website structures have changed")
        print("- Anti-bot protection is active")
        print("- Network connectivity issues")
        print("\nSuggestions:")
        print("1. Use the manual entry mode (run again and type 'manual')")
        print("2. Try using Google Places API (requires API key)")
        print("3. Check individual business directories manually")


if __name__ == "__main__":
    main()
