# Illinois Business Lead Scraper

A multi-source web scraper designed to find Illinois businesses that may need IT services or penetration testing. This tool searches multiple business directories to build a lead list with contact information.

## 🎯 Target Industries

The scraper focuses on businesses that typically need IT/security services:
- Medical offices & dental clinics
- Law firms
- Accounting firms
- Insurance agencies
- Financial advisors
- Real estate offices
- Manufacturing companies
- Retail stores
- Restaurants

## 📋 Features

- **Multi-Source Scraping**: Searches Yellow Pages, Manta, and Superpages
- **Illinois Focused**: Specifically targets Illinois businesses
- **Website Detection**: Identifies businesses without websites (prime prospects!)
- **Duplicate Removal**: Automatically removes duplicate entries
- **CSV Export**: Exports results to CSV for easy follow-up
- **Rate Limiting**: Respectful scraping with built-in delays
- **Statistics**: Shows summary of leads found

## 🚀 Installation

1. **Install Python** (3.7 or higher)

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests beautifulsoup4 lxml
```

## 💻 Usage

### Basic Usage

Simply run the script:
```bash
python illinois_lead_scraper.py
```

The script will:
1. Show default target categories
2. Search all directories for each category
3. Remove duplicates
4. Export to CSV with timestamp

### Custom Categories

When prompted, enter your own categories (comma-separated):
```
Press Enter to start scraping, or type custom categories (comma-separated): 
chiropractors, veterinarians, auto repair shops
```

### Output

The scraper creates a CSV file named: `illinois_leads_YYYYMMDD_HHMMSS.csv`

**CSV Columns:**
- `source` - Which directory the lead came from
- `business_name` - Name of the business
- `phone` - Contact phone number
- `address` - Business address
- `has_website` - Yes/No indicator
- `website` - Website URL (if available)
- `category` - Search category used
- `state` - Illinois

## 📊 Example Output

```
============================================================
Illinois Business Lead Scraper
============================================================

🔍 Searching Yellow Pages for medical offices in Illinois...
  ✓ Found: Springfield Family Medicine | Website: No
  ✓ Found: Advanced Care Clinic | Website: Yes
  ✓ Found: Downtown Medical Center | Website: No

🔍 Searching Manta for medical offices in Illinois...
  ✓ Found: Premier Health Associates | Website: No
  ...

✅ Exported 147 leads to illinois_leads_20241104_143022.csv

📊 Statistics:
   Total leads: 147
   Without website: 89 (60.5%)
   With website: 58
```

## 🎓 Why These Businesses Need IT Services

**Businesses without websites:**
- Need web presence development
- May lack IT infrastructure
- Often have outdated systems
- Prime candidates for managed IT services

**Industries with compliance needs:**
- Healthcare (HIPAA compliance)
- Legal (client confidentiality)
- Financial (PCI-DSS, data security)
- All need penetration testing & security audits

## ⚡ Pro Tips

1. **Focus on "No Website" leads first** - They're most likely to need services
2. **Call during business hours** - Better connection rates
3. **Research before calling** - Google the business for context
4. **Lead with value** - "I noticed you don't have a website..."
5. **Mention compliance** - Healthcare/legal firms need HIPAA/security

## 🛡️ Best Practices

1. **Respectful scraping**: Built-in rate limiting (2-5 seconds between requests)
2. **Check robots.txt**: The scraper respects standard web scraping etiquette
3. **Ethical usage**: Use leads for legitimate business outreach only
4. **CAN-SPAM compliance**: Follow email marketing laws when contacting leads
5. **Do Not Call**: Check DNC registry before cold calling

## 🔧 Customization

### Add More Directories

Add new scraping methods to the `IllinoisLeadScraper` class:

```python
def scrape_new_directory(self, category, location="Illinois"):
    """Scrape another directory"""
    # Your scraping logic here
    pass
```

### Change Search Location

Modify the `location` parameter in the `run_search()` method or individual scrape functions.

### Adjust Rate Limiting

Change the `rate_limit()` parameters:
```python
self.rate_limit(min_seconds=3, max_seconds=7)  # Slower
```

## ⚠️ Important Notes

- **Terms of Service**: Ensure your usage complies with each website's ToS
- **Rate Limiting**: Don't overwhelm servers - the built-in delays are important
- **Data Accuracy**: Always verify contact information before outreach
- **Legal Compliance**: Follow all applicable laws for business solicitation
- **API Alternatives**: Consider using official APIs where available

## 🐛 Troubleshooting

**No results found:**
- Website structure may have changed
- Try different category keywords
- Check your internet connection

**Timeout errors:**
- Increase timeout in requests (default: 15 seconds)
- Check if website is blocking automated requests

**Missing data:**
- Not all directories have complete information
- Some fields may show "N/A"

## 📈 Scaling Up

For larger scraping operations:
1. Use proxies to avoid rate limiting
2. Implement concurrent requests (carefully!)
3. Store results in a database instead of CSV
4. Add email discovery tools
5. Integrate with CRM systems

## 📝 License

This tool is for educational and legitimate business purposes only. Use responsibly and ethically.

## 🤝 Support

For issues or questions:
1. Check website structures haven't changed
2. Verify dependencies are installed
3. Ensure you have internet connectivity
4. Review error messages for specific issues

---

**Happy Lead Hunting! 🎯**

Remember: Quality > Quantity. A smaller list of well-researched prospects beats a huge list of cold contacts every time.
