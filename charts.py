# charts.py

import matplotlib.pyplot as plt

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

def draw_scatter_plot(score_df):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(score_df["Credit Score"], score_df["Risk Score"], c="purple", s=100)
    for i, row in score_df.iterrows():
        ax.text(row["Credit Score"] + 0.5, row["Risk Score"] + 0.5, row["Vendor"], fontsize=8)
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Risk Score")
    ax.set_title("Credit Score vs Risk Score")
    return fig
