import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_education_and_awards(scientist_url):
    response = requests.get(scientist_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the education paragraph
    education = soup.find('span', {'id': 'Education'})
    if education:
        education_paragraph = education.find_next('p')
    else:
        education_paragraph = None

    # Find the awards section
    awards = soup.find('span', {'id': 'Awards_and_honors'}) or soup.find('span', {'id': 'Awards'}) or soup.find('span', {'id': 'Honors_&_Awards'}) or soup.find('span', {'id': 'Honours_and_awards'})  or soup.find('span', {'id': 'Awards_and_recognition'})   or soup.find('span', {'id': 'Honors_and_awards'}) or soup.find('span', {'id': 'Awards_and_honors_list'}) or soup.find('span', {'id': 'Awards_and_honours'})
    if awards:
        awards_paragraph = awards.find_next('ul')
        awards_list = awards_paragraph.find_all('li')
        num_awards = len(awards_list)
    else:
        num_awards = None

    return education_paragraph.text.strip() if education_paragraph else None, num_awards

url = "https://en.wikipedia.org/wiki/List_of_computer_scientists"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize lists to store data
scientists_data = []

# Find all sections with names
sections = soup.find_all('span', {'class': 'mw-headline'})

# Counter to limit to the first 100 scientists
count = 0

for section in sections:
    current_element = section.find_next('li')

    while current_element and current_element.find('a') and count < 100:
        name = current_element.find('a').text.strip()
        scientist_url = "https://en.wikipedia.org" + current_element.find('a')['href']

        # Get education and awards information for the current scientist
        education, num_awards = get_education_and_awards(scientist_url)

        # Append data to the list
        scientists_data.append({'Name': name, 'Education': education, 'Awards': num_awards})

        current_element = current_element.find_next('li')
        count += 1

# Create a DataFrame using pandas
df = pd.DataFrame(scientists_data)

# Save the DataFrame to an Excel file
df.to_excel('64.xlsx', index=False)
