import requests
from bs4 import BeautifulSoup

def search_linkedin(company, keywords):
    url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}&origin=SWITCH_SEARCH_VERTICAL&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    profiles = soup.find_all("li", class_="search-result")
    
    for profile in profiles:
        name = profile.find("span", class_="name").text.strip()
        company_name = profile.find("p", class_="subline-level-1").text.strip()
        profile_url = profile.find("a", class_="app-aware-link")["href"]
        
        if company.lower() in company_name.lower():
            print(f"Name: {name}")
            print(f"Company: {company_name}")
            print(f"Profile URL: {profile_url}")
            print()
