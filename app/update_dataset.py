import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website containing the data
url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'

# Define the category mapping
category_map = {
    "Танки": "tanks",
    "ББМ": "bbm",
    "Артилерійські системи": "artillery_systems",
    "РСЗВ": "rszv",
    "Засоби ППО": "air_defense",
    "Літаки": "aircraft",
    "Гелікоптери": "helicopters",
    "БПЛА": "uavs",
    "Крилаті ракети": "cruise_missiles",
    "Кораблі (катери)": "ships",
    "Підводні човни": "submarines",
    "Автомобілі та автоцистерни": "vehicles",
    "Спеціальна техніка": "special_equipment",
    "Особовий склад": "personnel"
}

# Function to parse the casualties data from the webpage
def parse_casualties(soup):
    data = []
    dates = soup.find_all('h4')
    print(dates)
    tables = soup.find_all('table')

    for date, table in zip(dates, tables):
        date_str = date.text.strip()
        rows = table.find_all('tr')
        row_data = {'date': date_str}

        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                category = cells[0].text.strip()
                value = cells[1].text.strip().split(' ')[0].replace(',', '')
                english_category = category_map.get(category, None)
                if english_category:
                    row_data[english_category] = int(value)
                else:
                    # Debugging: Print unmapped category
                    print(f"Unmapped category: {category}")

        # Debugging: Print row_data to see what's being parsed
        print(f"Parsed row for date {date_str}: {row_data}")
        
        if len(row_data) > 1:  # Ensure there are values other than the date
            data.append(row_data)
    
    # Debugging: Print all parsed data
    print("Parsed Data:", data)
    
    return pd.DataFrame(data)

# Main function to add new data to the existing dataset
def add_new_data(existing_file_path):
    # Load existing dataset
    existing_df = pd.read_csv(existing_file_path)

    # Fetch and parse new data from the website
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    new_df = parse_casualties(soup)

    # Combine the existing and new data
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Remove duplicates based on the 'date' column
    combined_df = combined_df.drop_duplicates(subset=['date'])

    # Sort by date to maintain order
    combined_df['date'] = pd.to_datetime(combined_df['date'], format='%d.%m.%Y')
    combined_df = combined_df.sort_values(by='date')
    combined_df['date'] = combined_df['date'].dt.strftime('%d.%m.%Y')

    # Save the updated dataset back to the CSV file
    combined_df.to_csv(existing_file_path, index=False)

    print("Data successfully updated.")

# Paths to the existing dataset
existing_file_path = '../data/parsed_data.csv'

# Add new data to the existing dataset
add_new_data(existing_file_path)
