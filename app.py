import requests
import pandas as pd
import streamlit as st
from pathlib import Path

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Business Scraper",
    layout="wide"
)

# -----------------------------
# LOGO
# -----------------------------

logo_path = Path(__file__).with_name("logo.png")
if logo_path.exists():
    st.image(str(logo_path), width=120)

# -----------------------------
# TITLE
# -----------------------------

st.title("Business Scraper Dashboard")
st.write("Search businesses by type and location.")

# -----------------------------
# USER INPUTS
# -----------------------------

business_type = st.text_input("Business Type", "hotel")
location = st.text_input("Location", "Delhi")

# -----------------------------
# SEARCH BUTTON
# -----------------------------

if st.button("Search"):
    # API URL
    url = "https://overpass-api.de/api/interpreter"

    # Dynamic Query
    query = f"""
[out:json][timeout:25];

area["name"="{location}"]->.searchArea;

(
  node["name"](area.searchArea);
  way["name"](area.searchArea);
  relation["name"](area.searchArea);
);

out tags 50;
"""

    # Headers
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        # Request
        response = requests.get(
            url,
            params={"data": query},
            headers=headers,
            timeout=350
        )

        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.stop()

        try:
            data = response.json()
        except Exception:
            st.error("Invalid response from API")
            st.stop()

        # Empty list
        businesses = []

        # Loop through results
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name", "")

            if business_type.lower() in name.lower():
                businesses.append({
                    "Name": name,
                    "Phone": tags.get("phone"),
                    "Website": tags.get("website"),
                    "City": tags.get("addr:city")
                })

        # DataFrame
        df = pd.DataFrame(businesses)

        # Remove duplicates
        df = df.drop_duplicates()

        # Remove empty rows
        df = df.dropna(how="all")

        if len(df) == 0:
            st.warning("No businesses found.")

        # Success message
        st.success(f"Found {len(df)} businesses")

        # Show table
        st.dataframe(df)

        # CSV Download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{business_type}_{location}.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
