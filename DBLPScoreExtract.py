import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to search DBLP for a given name and return the number of matches as a string
def search_dblp(name):
    base_url = "https://dblp.org/search?q=" + name.replace(" ", "+")
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        matches_element = soup.find(id="completesearch-info-matches")

        if matches_element:
            matches_text = matches_element.get_text(strip=True)
            # Extract the number from the "found X matches" text
            if "found one match" in matches_text:
                return "1"
            elif "found 1 match" in matches_text:
                return "1"
            elif "no matches" in matches_text:
                return "0"
            else:
                matches_count = matches_text.split()[1]
                return matches_count

    return "0"

# Read the Excel file
excel_file_path = "C:\\Users\\Koukounaras\\Desktop\\python2\\fulexcel3.xlsx"
df = pd.read_excel(excel_file_path)

# Apply the search_dblp function to each row in the "Name" column and create a new column "DBLP_Record"
df["DBLP_Record"] = df["Name"].apply(search_dblp)

# Save the updated DataFrame to the same Excel file
df.to_excel(excel_file_path, index=False)

# Print the updated DataFrame
print(df)




