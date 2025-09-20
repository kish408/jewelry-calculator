import streamlit as st
import requests
from bs4 import BeautifulSoup

# -----------------------------
# Function to fetch live prices
# -----------------------------
def fetch_prices():
    url = "https://www.grtjewels.com/"
    prices = {}
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        # Find the first table that contains rates
        table = soup.find("table")
        if table:
            for row in table.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 2:
                    key = cols[0].get_text(strip=True)
                    value_text = cols[1].get_text(strip=True).replace("₹", "").replace("/gm", "").replace(",", "")
                    try:
                        prices[key] = float(value_text)
                    except:
                        continue

        if not prices:
            raise ValueError("No prices found from live site")

    except Exception as e:
        st.warning(f"Using fallback prices. Error fetching live data: {e}")
        # fallback defaults
        prices = {
            "24K Gold": 11200.0,
            "22K Gold": 10280.0,
            "18K Gold": 8200.0,
            "14K Gold": 6500.0,
            "Platinum": 3400.0,
            "Silver": 75.5
        }
    return prices

# -----------------------------
# Calculation logic
# -----------------------------
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

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Jewelry Price Calculator", layout="centered")
st.title("💎 Jewelry Price Calculator")

# Fetch and display prices
prices = fetch_prices()
st.subheader("📊 Today's Prices (per gram)")
st.table(prices)

# Default rate = 22K Gold
default_rate = prices.get("22K Gold", 10280.0)

# -----------------------------
# Input Form
# -----------------------------
st.subheader("🧮 Calculate Price")
with st.form("calc_form"):
    weight = st.number_input("Weight (grams)", min_value=0.01, step=0.01, value=0.01)
    rate = st.number_input("Rate (per gram)", value=float(default_rate), step=1.0)
    making_charges = st.number_input("Making Charges (%)", min_value=0.0, step=0.1, value=0.0)
    gst = st.number_input("GST (%)", min_value=0.0, step=0.1, value=0.0)

    submitted = st.form_submit_button("Calculate")

# Only calculate if user pressed the button
if submitted:
    result = calculate_price(weight, rate, making_charges, gst)
    st.success("✅ Calculation Result")
    st.table(result)
