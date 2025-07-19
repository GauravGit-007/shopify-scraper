import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_soup(url):
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()
    return BeautifulSoup(res.text, 'html.parser')

def extract_links(soup):
    return [a['href'] for a in soup.find_all('a', href=True)]

def full_url(base, link):
    return urljoin(base, link)

def extract_social_links(soup):
    socials = {}
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'instagram.com' in href:
            socials['instagram'] = href
        elif 'facebook.com' in href:
            socials['facebook'] = href
        elif 'tiktok.com' in href:
            socials['tiktok'] = href
        elif 'youtube.com' in href:
            socials['youtube'] = href
    return socials

def extract_emails_phones(soup):
    text = soup.get_text()
    emails = list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)))
    phones = list(set(re.findall(r"\+?\d[\d\s\-]{7,}\d", text)))
    return {"emails": emails, "phones": phones}

def extract_products_json(base_url):
    try:
        res = requests.get(urljoin(base_url, "/products.json"), headers=HEADERS)
        return res.json().get("products", [])
    except:
        return []

def extract_hero_products(soup):
    hero = []
    for a in soup.find_all('a', href=True):
        if '/products/' in a['href']:
            title = a.get_text(strip=True)
            if title:
                hero.append(title)
    return list(set(hero))

def extract_policies(soup, base_url):
    links = extract_links(soup)
    policy_links = {}
    for link in links:
        if 'privacy' in link.lower():
            policy_links['privacy_policy'] = full_url(base_url, link)
        elif 'refund' in link.lower() or 'return' in link.lower():
            policy_links['return_refund'] = full_url(base_url, link)
        elif 'faq' in link.lower():
            policy_links['faq'] = full_url(base_url, link)
        elif 'contact' in link.lower():
            policy_links['contact'] = full_url(base_url, link)
        elif 'about' in link.lower():
            policy_links['about'] = full_url(base_url, link)
        elif 'track' in link.lower():
            policy_links['order_tracking'] = full_url(base_url, link)
        elif 'blog' in link.lower():
            policy_links['blog'] = full_url(base_url, link)
    return policy_links

def extract_about_text(soup):
    text_blocks = soup.find_all(['section', 'p', 'div'])
    for block in text_blocks:
        text = block.get_text(strip=True).lower()
        if 'about us' in text or 'who we are' in text:
            return block.get_text(strip=True)
    return None

def scrape_shopify_store(url):
    soup = get_soup(url)
    base_url = f"{url.split('/')[0]}//{url.split('/')[2]}"

    return {
        "products": extract_products_json(base_url),
        "hero_products": extract_hero_products(soup),
        "social_links": extract_social_links(soup),
        "policies": extract_policies(soup, base_url),
        "contact": extract_emails_phones(soup),
        "brand_text": extract_about_text(soup)
    }
