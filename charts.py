# charts.py (Updated for Individual Vendor Only)

import matplotlib.pyplot as plt

#  1. Vendor Pie Chart (Credit Score vs Remaining)
def draw_vendor_pie_chart(row):
    credit = row["Credit Score"]
    remaining = 100 - credit if credit <= 100 else 0
    labels = ["Credit Score", "Remaining"]
    values = [credit, remaining]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    return fig

#  2. Vendor Line Chart (Income vs Expense Over 3 Months)
def draw_vendor_line_chart(row):
    months = ["Month 1", "Month 2", "Month 3"]
    income = [row["Monthly Income - Month 1"], row["Monthly Income - Month 2"], row["Monthly Income - Month 3"]]
    expense = [row["Spending Variance - Month 1"], row["Spending Variance - Month 2"], row["Spending Variance - Month 3"]]

    fig, ax = plt.subplots()
    ax.plot(months, income, label="Income", marker='o', color="green")
    ax.plot(months, expense, label="Expense", marker='o', color="red")
    ax.set_title("Income vs Expense Trend")
    ax.set_ylabel("Amount (₹)")
    ax.legend()
    return fig

#  3. Vendor Bar Chart (Credit Score Components)
def draw_vendor_bar_chart(row):
    labels = ["Transactions", "Consistency", "Supplier Verified", "Testimonials"]
    values = [
        row["Monthly Transactions"],
        row["Consistency Score"],
        100 if str(row["Supplier Verified"]).strip().lower() == "yes" else 0,
        (row["Customer Testimonial"] / 10) * 100
    ]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color="skyblue")
    ax.set_ylim(0, 100)
    ax.set_title("Credit Score Component Breakdown")
    return fig
