
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from main import scrape_category

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=9247920371F5F8DA3544167CAC3F0FD0.METS; visid_incap_2542910=dx2Kmx/KR46Jd23pdepsCCsjdGQAAAAAQUIPAAAAAAAIcWVTMx8A5EUp94j5vFIx; nlbi_2542910=xi2eQEu0+DciSmbD78jW8wAAAAAXeUPFTgkCigvLM36hcdfR; incap_ses_969_2542910=XFYzMQ6IrlN3ydqVOJVyDSsjdGQAAAAAB7JrJ4kStOS0zPdKt1LK6g==; AWSALB=msHTwDBhsW3FiqePxevzYKBSu0HvRik9yw42xVGl7f44aQkZBCQSVBcw/EkSQXOKZSJ/fgfMgAYjSJYMIIzmpFxmKizqkuvRr4sP7eJr2yoXQHnQys91ZZOpUvHQ; AWSALBCORS=msHTwDBhsW3FiqePxevzYKBSu0HvRik9yw42xVGl7f44aQkZBCQSVBcw/EkSQXOKZSJ/fgfMgAYjSJYMIIzmpFxmKizqkuvRr4sP7eJr2yoXQHnQys91ZZOpUvHQ',
    'Host': 'www.merx.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
main_url = 'https://www.merx.com/public/solicitations/edp-hardware-and-software-10034'

response = requests.get(main_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

raw_links = soup.find_all('td', {'class': 'mainCol'})
solicitations_endpoints = []
for raw_link in raw_links:
    raw_link = raw_link.find('a', {'class': 'solicitation-link'}).get("href")
    solicitations_endpoints.append(raw_link)

with ThreadPoolExecutor() as executor:
    executor.map(scrape_category, solicitations_endpoints)