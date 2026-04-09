import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simple Budget Tracker", layout="centered")

# Load or create CSV
@st.cache_data
def load_data():
    try:
        return pd.read_csv("budget_data.csv")
    except:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])

budget_df = load_data()

# UI Title
st.title("💵 Simple & Free Budget Tracker")
st.write("Track income, expenses, and visualize your monthly spending.")

# Input Form
with st.form("entry_form", clear_on_submit=True):
    date = st.text_input("Date (YYYY-MM-DD)")
    ttype = st.selectbox("Type", ["Income", "Expense"])
    category = st.selectbox(
        "Category",
        ["Food", "Rent", "Bills", "Gas", "Shopping", "Travel", "Entertainment", "Medical", "Other"]
    )
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Entry")

if submitted:
    new_row = {"Date": date, "Type": ttype, "Category": category, "Amount": amount}
    budget_df = pd.concat([budget_df, pd.DataFrame([new_row])], ignore_index=True)
    budget_df.to_csv("budget_data.csv", index=False)
    st.success("Transaction added ✔")

# Month filter
month = st.selectbox(
    "Filter by month",
    ["All"] + [f"{i:02d}" for i in range(1, 13)]
)

if month != "All":
    filtered_df = budget_df[budget_df["Date"].str[5:7] == month]
else:
    filtered_df = budget_df

st.subheader("📊 Transactions")
st.dataframe(filtered_df)

# Summary
income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
remaining = income - expense

st.subheader("💰 Summary")
st.write(f"Total Income: ${income:.2f}")
st.write(f"Total Expense: ${expense:.2f}")
st.write(f"Remaining Budget: ${remaining:.2f}")

# Pie chart
expense_df = filtered_df[filtered_df["Type"] == "Expense"]
if not expense_df.empty:
    st.subheader("🍕 Expense Breakdown")
    fig, ax = plt.subplots()
    pie_data = expense_df.groupby("Category")["Amount"].sum()
    ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
    st.pyplot(fig)
else:
    st.info("No expenses to show.")
    import zipfile
import io

def create_zip():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        z.write("app.py")
        z.write("requirements.txt")
        # Include CSV only if exists
        try:
            z.write("budget_data.csv")
        except:
            pass
    buffer.seek(0)
    return buffer

st.subheader("📥 Download the Entire App")
zip_file = create_zip()

st.download_button(
    label="Download Budget Tracker ZIP",
    data=zip_file,
    file_name="budget_tracker_app.zip",
    mime="application/zip"
)
