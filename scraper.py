import requests
import pandas as pd

# API endpoint
url = "https://overpass.kumi.systems/api/interpreter"

# Query for hotels in Delhi
query = """
[out:json];

area["name"="Delhi"]->.searchArea;

(
  node["tourism"="hotel"](area.searchArea);
  way["tourism"="hotel"](area.searchArea);
  relation["tourism"="hotel"](area.searchArea);
);

out center;
"""

# Headers make request look like a real browser
# Headers
headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # Send request
    response = requests.get(
        url,
        params={'data': query},
        headers=headers,
        timeout=60
    )

    # Print status code
    print("Status Code:", response.status_code)

    # Check if request successful
    response.raise_for_status()

    # Convert to JSON
    data = response.json()

except requests.exceptions.RequestException as e:
    print("Request Error:", e)
    exit()

except ValueError:
    print("Failed to decode JSON.")
    print(response.text)
    exit()
# Empty list to store hotels
hotels = []

# Loop through all returned hotels
for element in data['elements']:

    # Get tags safely
    tags = element.get('tags', {})

    # Add hotel data into list
    hotels.append({
        "Hotel Name": tags.get("name"),
        "Phone": tags.get("phone"),
        "Website": tags.get("website"),
        "City": tags.get("addr:city")
    })

# Convert list into table
df = pd.DataFrame(hotels)

# Remove empty rows
df = df.dropna(how='all')

# Save to CSV
df.to_csv("hotels.csv", index=False)
pip install streamlit
# Print success message
print("\nDone! Hotels saved successfully.\n")

# Show first 5 rows
print(df.head())