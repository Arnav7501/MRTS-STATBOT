import requests
from bs4 import BeautifulSoup


def scrape_wiki(unitName):
    try:
        url = f"https://mrts.fandom.com/wiki/{unitName}"

    # Send a GET request to fetch the HTML content
        response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.content, "html.parser")

# Extract the desired information


# Print the extracted information

        td_tag = soup.find("div", class_="mw-parser-output")

# Extract the text content of the td tag
        content = td_tag.text.strip() if td_tag else None

        array = [line for line in content.split("\n") if line.strip()]
        images = soup.find_all('img')
        image = images[1].get('src')
        array.append(image)
        return array

    except Exception as e:
        return 1
