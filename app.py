import requests
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Business Scraper",
    layout="wide"
)
logo_path = Path(__file__).with_name("logo.png")
if logo_path.exists():
else:
    st.warning("Logo file not found; continuing without image.")

st.title("Business Scraper Dashboard")

# User Inputs
business_type = st.text_input("Business Type", "hotel")
location = st.text_input("Location", "Delhi")

# Search Button
if st.button("Search"):

    url = "https://overpass.kumi.systems/api/interpreter"

    # Dynamic query
    query = f"""
    [out:json];

    area["name"="{location}"]->.searchArea;

    (
      node["tourism"="{business_type}"](area.searchArea);
      way["tourism"="{business_type}"](area.searchArea);
      relation["tourism"="{business_type}"](area.searchArea);
    );

    out center;
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            params={'data': query},
            headers=headers,
            timeout=60
        )

        data = response.json()

        businesses = []

        for element in data['elements']:

            tags = element.get('tags', {})

            businesses.append({
                "Name": tags.get("name"),
                "Phone": tags.get("phone"),
                "We"
                "bsite": tags.get("website"),
                "City": tags.get("addr:city")
            })

        df = pd.DataFrame(businesses)

        df = df.drop_duplicates()

        st.success(f"Found {len(df)} businesses")

        st.dataframe(df)

        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            "Download CSV",
            csv,
            file_name=f"{business_type}_{location}.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(f"Error: {e}")