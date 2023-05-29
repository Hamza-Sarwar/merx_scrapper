

from bs4 import BeautifulSoup
import requests
import pandas as pd
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



def scrape_category(solicitation_endpoint):
    try:
        solicitation_url = f"https://www.merx.com{solicitation_endpoint}"
        response = requests.get(solicitation_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract basic information
        form_data = soup.find("form", {"class": "current-form"})
        raw_data = form_data.find_all('div', {'class': 'mets-field'})

        data = {}
        for field in raw_data:
            labels = field.find('span', {'class': 'mets-field-label'}).text.strip()
            contents = field.find('div', {'class': 'mets-field-body'}).text.strip()
            data['URL'] = solicitation_url
            data[labels] = contents
        print(data.keys())
        selected_keys = ['URL', 'Reference Number', 'Issuing Organization', 'Solicitation Type', 'Solicitation Number',
                         'Title', 'Publication', 'Questions are submitted online', 'Closing Date']
        selected_values = [data[key] for key in selected_keys if key in data]
        print(selected_values)
        if 'Project Number' in data:
            with open('project.csv', 'a') as f:
                f.write(','.join(selected_values) + '\n')
        else:
            with open('solicitation.csv', 'a') as f:
                f.write(','.join(selected_values) + '\n')

    except Exception as e:
        print(e)



