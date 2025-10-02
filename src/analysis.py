"""PlayStation Data Analysis

This script loads the Video_Games.csv dataset, cleans the data and performs simple
analyses specific to PlayStation platforms. It is intended as an example for
an entry-level data analytics portfolio. To run, ensure the CSV is stored at
Data/Video_Games.csv relative to the repository root.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional


def load_raw(filepath: str) -> pd.DataFrame:
    """Load the raw CSV into a DataFrame without modification."""
    return pd.read_csv(filepath)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw video game DataFrame and keep only PlayStation platforms."""
    # Convert numerics
    df["Year_of_Release"] = pd.to_numeric(df["Year_of_Release"], errors="coerce")
    df["User_Score"] = pd.to_numeric(df["User_Score"], errors="coerce")
    for col in ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Require year + global sales
    df = df.dropna(subset=["Year_of_Release", "Global_Sales"])

    # Trim text
    for col in ["Name", "Platform", "Genre", "Publisher", "Developer"]:
        df[col] = df[col].astype(str).str.strip()

    # Filter PlayStation platforms
    ps_df = df[df["Platform"].str.startswith("PS", na=False)].copy()
    return ps_df


def top_games_by_sales(ps_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top n PlayStation games by global sales."""
    return (
        ps_df.groupby(["Name", "Platform"])["Global_Sales"]
        .sum()
        .reset_index()
        .sort_values("Global_Sales", ascending=False)
        .head(n)
    )


def genre_sales_plot(ps_df: pd.DataFrame, output_path: Optional[str] = None) -> pd.Series:
    """Plot total global sales per genre for PlayStation games."""
    genre_sales = ps_df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 5))
    genre_sales.plot(kind="bar", title="Total Global Sales per Genre (PlayStation)")
    plt.ylabel("Global Sales (millions)")
    plt.xlabel("Genre")
    plt.tight_layout()

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
    return genre_sales


def save_top10_chart(ps_df: pd.DataFrame, output_path: str) -> pd.DataFrame:
    """Save a horizontal bar chart + CSV for top 10 PlayStation games by global sales."""
    top10 = (
        ps_df.groupby(["Name", "Platform"])["Global_Sales"]
        .sum()
        .reset_index()
        .sort_values("Global_Sales", ascending=False)
        .head(10)
    )

    # Save CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    csv_path = os.path.join(os.path.dirname(output_path), "top10_playstation.csv")
    top10.to_csv(csv_path, index=False)

    # Plot horizontal bar (more readable)
    plt.figure(figsize=(10, 5))
    top10_plot = top10.sort_values("Global_Sales", ascending=True)
    labels = top10_plot["Name"] + " (" + top10_plot["Platform"] + ")"
    plt.barh(labels, top10_plot["Global_Sales"])
    plt.title("Top 10 PlayStation Games by Global Sales")
    plt.xlabel("Global Sales (millions)")
    plt.tight_layout()
    plt.savefig(output_path)
    return top10


def main():
    # NOTE: folder name is 'Data' (capital D) to match your actual structure
    data_path = os.path.join(os.path.dirname(__file__), "..", "Data", "Video_Games.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Dataset not found at {data_path}. Please place Video_Games.csv in the Data folder."
        )

    raw_df = load_raw(data_path)
    ps_df = clean_dataframe(raw_df)

    print("Top 10 PlayStation games by global sales:")
    print(top_games_by_sales(ps_df, 10))

    # Genre chart
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    genre_plot_path = os.path.join(results_dir, "genre_sales.png")
    genre_sales_plot(ps_df, genre_plot_path)
    print(f"Genre sales plot saved to {genre_plot_path}")

    # Top 10 chart + CSV
    top10_plot_path = os.path.join(results_dir, "top10_playstation.png")
    save_top10_chart(ps_df, top10_plot_path)
    print(f"Top 10 chart saved to {top10_plot_path}")
    print(f"Top 10 CSV saved to {os.path.join(results_dir, 'top10_playstation.csv')}")


if __name__ == "__main__":
    main()
