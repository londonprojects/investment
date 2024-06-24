import streamlit as st
import pandas as pd

def calculate_investment(initial_investment, monthly_savings, ira_contributions, stock_contributions, bond_contributions, cash_contributions, annual_return_rates, years, inflation_rate, early_withdrawal_age, current_age, income_tax_rate, capital_gains_tax_rate):
    data = {
        "Year": list(range(1, years + 1)),
        "Total IRA Contributions (£)": [0] * years,
        "Total Stock Contributions (£)": [0] * years,
        "Total Bond Contributions (£)": [0] * years,
        "Total Cash Contributions (£)": [0] * years,
        "Total Contributions (£)": [0] * years,
        "Investment Gains (£)": [0] * years,
        "Year-End Balance (£)": [0] * years,
        "Inflation Adjusted Balance (£)": [0] * years,
        "Taxes Paid (£)": [0] * years,
        "Early Withdrawal Penalty (£)": [0] * years
    }
    
    df = pd.DataFrame(data)
    early_withdrawal_penalty_rate = 0.10

    for i in range(years):
        if i == 0:
            contributions = initial_investment + monthly_savings * 12 + ira_contributions + stock_contributions + bond_contributions + cash_contributions
            gains = (initial_investment * annual_return_rates['Total']) + (ira_contributions * annual_return_rates['IRA']) + (stock_contributions * annual_return_rates['Stocks']) + (bond_contributions * annual_return_rates['Bonds']) + (cash_contributions * annual_return_rates['Cash'])
            df.at[i, "Total IRA Contributions (£)"] = ira_contributions
            df.at[i, "Total Stock Contributions (£)"] = stock_contributions
            df.at[i, "Total Bond Contributions (£)"] = bond_contributions
            df.at[i, "Total Cash Contributions (£)"] = cash_contributions
            df.at[i, "Total Contributions (£)"] = contributions
            df.at[i, "Investment Gains (£)"] = gains
            df.at[i, "Year-End Balance (£)"] = contributions + gains
        else:
            previous_balance = df.at[i - 1, "Year-End Balance (£)"]
            contributions = monthly_savings * 12 + ira_contributions + stock_contributions + bond_contributions + cash_contributions
            gains = (previous_balance * annual_return_rates['Total']) + (ira_contributions * annual_return_rates['IRA']) + (stock_contributions * annual_return_rates['Stocks']) + (bond_contributions * annual_return_rates['Bonds']) + (cash_contributions * annual_return_rates['Cash'])
            df.at[i, "Total IRA Contributions (£)"] = df.at[i - 1, "Total IRA Contributions (£)"] + ira_contributions
            df.at[i, "Total Stock Contributions (£)"] = df.at[i - 1, "Total Stock Contributions (£)"] + stock_contributions
            df.at[i, "Total Bond Contributions (£)"] = df.at[i - 1, "Total Bond Contributions (£)"] + bond_contributions
            df.at[i, "Total Cash Contributions (£)"] = df.at[i - 1, "Total Cash Contributions (£)"] + cash_contributions
            df.at[i, "Total Contributions (£)"] = df.at[i - 1, "Total Contributions (£)"] + contributions
            df.at[i, "Investment Gains (£)"] = df.at[i - 1, "Investment Gains (£)"] + gains
            df.at[i, "Year-End Balance (£)"] = previous_balance + contributions + gains
        
        # Adjust for inflation
        df.at[i, "Inflation Adjusted Balance (£)"] = df.at[i, "Year-End Balance (£)"] / ((1 + inflation_rate) ** (i + 1))

        # Calculate taxes and penalties for early withdrawal
        if current_age + i < early_withdrawal_age:
            df.at[i, "Early Withdrawal Penalty (£)"] = df.at[i, "Year-End Balance (£)"] * early_withdrawal_penalty_rate
            df.at[i, "Taxes Paid (£)"] = df.at[i, "Investment Gains (£)"] * capital_gains_tax_rate
        else:
            df.at[i, "Early Withdrawal Penalty (£)"] = 0
            df.at[i, "Taxes Paid (£)"] = df.at[i, "Year-End Balance (£)"] * income_tax_rate

    return df

def display_summary(df):
    total_contributions = df["Total Contributions (£)"].iloc[-1]
    total_gains = df["Investment Gains (£)"].iloc[-1]
    final_balance = df["Year-End Balance (£)"].iloc[-1]
    final_inflation_adjusted_balance = df["Inflation Adjusted Balance (£)"].iloc[-1]
    total_taxes_paid = df["Taxes Paid (£)"].sum()
    total_early_withdrawal_penalty = df["Early Withdrawal Penalty (£)"].sum()
    st.write(f"### Summary")
    st.write(f"After {len(df)} years, your investment will be worth approximately **£{final_balance:,.2f}**.")
    st.write(f"Adjusted for inflation, the value is approximately **£{final_inflation_adjusted_balance:,.2f}**.")
    st.write(f"Total Contributions: **£{total_contributions:,.2f}**")
    st.write(f"Total Gains: **£{total_gains:,.2f}**")
    st.write(f"Total Taxes Paid: **£{total_taxes_paid:,.2f}**")
    st.write(f"Total Early Withdrawal Penalty: **£{total_early_withdrawal_penalty:,.2f}**")
    st.write(f"Average Annual Return: **{((final_balance / total_contributions) ** (1 / len(df)) - 1) * 100:.2f}%**")

st.title("Investment Projection App")

st.sidebar.header("Personal Financial Parameters")
annual_salary = st.sidebar.number_input("Annual Salary (£)", min_value=0, value=220000, step=1000)
estimated_take_home_pay = st.sidebar.number_input("Estimated Take-Home Pay (£)", min_value=0, value=131906, step=1000)
annual_amount_left_for_living = st.sidebar.number_input("Annual Amount Left for Living Expenses (£)", min_value=0, value=71906, step=1000)
monthly_amount_left_for_living = annual_amount_left_for_living / 12

st.sidebar.write(f"Monthly Amount Left for Living Expenses: **£{monthly_amount_left_for_living:,.2f}**")

st.sidebar.header("Investment Parameters")
initial_investment = st.sidebar.number_input("Initial Investment (£)", min_value=0, value=100000, step=1000, help="Enter the initial amount you are investing.")
years = st.sidebar.number_input("Investment Period (Years)", min_value=1, value=30, step=1, help="Enter the number of years you plan to invest.")
monthly_savings = st.sidebar.number_input("Monthly Savings (£)", min_value=0, value=5000, step=100, help="Enter the amount you will save monthly.")

st.sidebar.subheader("Savings Allocation")
ira_contributions = st.sidebar.number_input("IRA Contributions (£)", min_value=0, value=12000, step=1000)
stock_contributions = st.sidebar.number_input("Stock Investments (£)", min_value=0, value=24000, step=1000)
bond_contributions = st.sidebar.number_input("Bond Investments (£)", min_value=0, value=12000, step=1000)
cash_contributions = st.sidebar.number_input("Cash Savings (£)", min_value=0, value=12000, step=1000)

st.sidebar.subheader("Return Rates")
annual_return_rates = {
    'IRA': st.sidebar.number_input("IRA Return Rate (%)", min_value=0.0, value=6.0, step=0.1) / 100,
    'Stocks': st.sidebar.number_input("Stocks Return Rate (%)", min_value=0.0, value=8.0, step=0.1) / 100,
    'Bonds': st.sidebar.number_input("Bonds Return Rate (%)", min_value=0.0, value=4.0, step=0.1) / 100,
    'Cash': st.sidebar.number_input("Cash Return Rate (%)", min_value=0.0, value=1.0, step=0.1) / 100,
    'Total': 0.06  # Overall return rate can be calculated dynamically if needed
}

inflation_rate = st.sidebar.number_input("Inflation Rate (%)", min_value=0.0, value=2.0, step=0.1)
early_withdrawal_age = st.sidebar.number_input("Early Withdrawal Age", min_value=0, value=59, step=1)
current_age = st.sidebar.number_input("Current Age", min_value=0, value=30, step=1)
income_tax_rate = st.sidebar.number_input("Income Tax Rate (%)", min_value=0.0, value=25.0, step=0.1) / 100
capital_gains_tax_rate = st.sidebar.number_input("Capital Gains Tax Rate (%)", min_value=0.0, value=20.0, step=0.1) / 100

if st.sidebar.button("Calculate"):
    df = calculate_investment(
        initial_investment, monthly_savings, ira_contributions, stock_contributions, bond_contributions, cash_contributions, 
        annual_return_rates, years, inflation_rate, early_withdrawal_age, current_age, income_tax_rate, capital_gains_tax_rate
    )
    st.write("## Investment Projections")
    st.write(df)
    st.line_chart(df.set_index("Year")[["Year-End Balance (£)", "Inflation Adjusted Balance (£)"]])
    display_summary(df)
    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv().encode('utf-8'),
        file_name='investment_projection.csv',
        mime='text/csv'
    )

st.sidebar.write("Adjust the inputs to see how different investment strategies affect your total investment over time.")
