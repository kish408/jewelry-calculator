import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to fetch live prices from GRT Jewels
def fetch_prices():
    url = "https://www.grtjewels.com/"
    prices = {}
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        for div in soup.find_all("div", class_="gold_silver_price"):
            text = div.get_text(" ", strip=True)
            if "Gold" in text or "Platinum" in text or "Silver" in text:
                key = text.split("Rate")[0].strip()  # e.g. "22K Gold"
                value = text.split("Rs.")[-1].replace("/gm", "").replace(",", "").strip()
                try:
                    prices[key] = float(value)
                except:
                    pass
    except Exception as e:
        st.error(f"Error fetching prices: {e}")

    return prices

# Calculation logic
def calculate_price(weight, rate, making_percent, gst_percent):
    base_price = weight * rate
    making = (making_percent / 100) * base_price
    subtotal = base_price + making
    gst = (gst_percent / 100) * subtotal
    total = subtotal + gst
    return {
        "Base Price": round(base_price, 2),
        "Making Charges": round(making, 2),
        "GST": round(gst, 2),
        "Total": round(total, 2),
    }

# Streamlit UI
st.set_page_config(page_title="Jewelry Price Calculator", layout="centered")
st.title("💎 Jewelry Price Calculator")

# Fetch and display live prices
prices = fetch_prices()
if prices:
    st.subheader("📊 Today's Prices (per gram)")
    st.table(prices)

# Default rate = 22K Gold
default_rate = prices.get("22K Gold", 6000)

# Input Form
st.subheader("🧮 Calculate Price")
with st.form("calc_form"):
    weight = st.number_input("Weight (grams)", min_value=0.01, step=0.01)
    rate = st.number_input("Rate (per gram)", value=default_rate, step=1.0)
    making_charges = st.number_input("Making Charges (%)", min_value=0.0, step=0.1)
    gst = st.number_input("GST (%)", min_value=0.0, step=0.1)
    submitted = st.form_submit_button("Calculate")

if submitted:
    result = calculate_price(weight, rate, making_charges, gst)
    st.success("✅ Calculation Result")
    st.table(result)
