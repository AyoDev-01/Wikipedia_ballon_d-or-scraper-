import requests
from bs4 import BeautifulSoup
import pandas as pd


# Website to scrape
url = "https://en.wikipedia.org/wiki/2026_Ballon_d%27Or"

# Identify the request as coming from a browser
headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # Request the webpage
    page = requests.get(url, headers=headers, timeout=10)
    page.raise_for_status()

    # Parse the webpage
    soup = BeautifulSoup(page.text, "html.parser")

    # Find the required table
    tables = soup.find_all("table")

    if len(tables) < 2:
        raise ValueError("The required table was not found.")

    table = tables[1]

    # Extract column headings
    headers = table.find_all("th")
    table_titles = [title.text.strip() for title in headers]

    # Create DataFrame
    df = pd.DataFrame(columns=table_titles)

    # Extract table rows
    rows = table.find_all("tr")

    for row in rows[1:]:
        row_data = row.find_all("td")
        each_row_data = [data.text.strip() for data in row_data]

        if len(each_row_data) == len(table_titles):
            df.loc[len(df)] = each_row_data

    # Save CSV
    output_path = "/storage/emulated/0/pydriod 3 games/ballon dor.csv"
    df.to_csv(output_path, index=False)

    print(f"Successfully scraped {len(df)} rows.")
    print(f"CSV saved to: {output_path}")

except requests.RequestException as error:
    print(f"Error requesting webpage: {error}")

except Exception as error:
    print(f"Error: {error}")