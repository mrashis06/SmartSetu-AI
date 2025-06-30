# charts.py

import matplotlib.pyplot as plt

# 1. Bar Chart (Top N Vendors by Credit and Risk Score)
def draw_bar_chart(score_df, top_n):
    top_df = score_df.sort_values("Credit Score", ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(max(10, top_n * 0.6), 6))
    x = range(len(top_df))
    bar_width = 0.35
    ax.bar([i - 0.2 for i in x], top_df["Credit Score"], width=bar_width, label="Credit", color="royalblue")
    ax.bar([i + 0.2 for i in x], top_df["Risk Score"], width=bar_width, label="Risk", color="salmon")
    ax.set_xticks(x)
    ax.set_xticklabels(top_df["Vendor"], rotation=45)
    ax.legend()
    return fig

# 2. Scatter Plot (Credit vs Risk Score)
def draw_scatter_plot(score_df):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(score_df["Credit Score"], score_df["Risk Score"], c="purple", s=100)
    for i, row in score_df.iterrows():
        ax.text(row["Credit Score"] + 0.5, row["Risk Score"] + 0.5, row["Vendor"], fontsize=8)
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Risk Score")
    ax.set_title("Credit Score vs Risk Score")
    return fig

# 3. Vendor Pie Chart (Credit Share)
def draw_vendor_pie_chart(row):
    # Single vendor pie chart: Show Credit Score vs Remaining
    credit = row["Credit Score"]
    remaining = 100 - credit if credit <= 100 else 0
    labels = ["Credit Score", "Remaining"]
    values = [credit, remaining]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    return fig


# 4. Credit Score Distribution Histogram
def draw_credit_score_distribution(score_df):
    scores = score_df["Credit Score"]
    fig, ax = plt.subplots()
    ax.hist(scores, bins=10, color="#4DC4D2", edgecolor="black")
    ax.set_title("Credit Score Distribution")
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Number of Vendors")
    return fig
