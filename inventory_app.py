import streamlit as st
import pandas as pd

st.set_page_config(page_title="Inventory Comparison Tool")
st.title("📦 Inventory Change Tracker")

st.markdown("Upload two CSV files with the following structure:")
st.markdown("""
- Column A: **Item Name**  
- Column E: **Quantity**  
- Column G: **Item ID**
""")

last_file = st.file_uploader("📂 Upload Last Week's Inventory", type="csv")
this_file = st.file_uploader("📂 Upload This Week's Inventory", type="csv")

def load_inventory(file):
    df = pd.read_csv(file, header=None)
    df = df[[0, 4, 6]]
    df.columns = ["Item Name", "Quantity", "Item ID"]
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df = df.dropna(subset=["Item ID"])
    return df

if last_file and this_file:
    df_last = load_inventory(last_file)
    df_this = load_inventory(this_file)

    merged = pd.merge(df_last, df_this, on="Item ID", how="outer", suffixes=("_LastWeek", "_ThisWeek"))
    merged["Quantity_LastWeek"] = merged["Quantity_LastWeek"].fillna(0)
    merged["Quantity_ThisWeek"] = merged["Quantity_ThisWeek"].fillna(0)
    merged["Change"] = merged["Quantity_ThisWeek"] - merged["Quantity_LastWeek"]

    st.success("✅ Inventory comparison complete!")
    st.dataframe(merged)

    csv = merged.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Report as CSV", csv, "inventory_changes.csv", "text/csv")
