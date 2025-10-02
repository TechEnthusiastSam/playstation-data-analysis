"""PlayStation Data Analysis

This script loads the Video_Games.csv dataset, cleans the data and performs simple
analyses specific to PlayStation platforms.  It is intended as an example for
an entry‑level data analytics portfolio.  To run, ensure the CSV is stored at
data/Video_Games.csv relative to the repository root.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional


def load_raw(filepath: str) -> pd.DataFrame:
    """Load the raw CSV into a DataFrame without modification.

    :param filepath: Path to the Video_Games.csv dataset
    :return: DataFrame containing the raw dataset
    """
    return pd.read_csv(filepath)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw video game DataFrame.

    This function converts numeric columns, drops rows with missing key values
    and filters to rows where the Platform begins with 'PS'.  Modify this
    function if you wish to analyse other platforms or perform additional
    cleaning.

    :param df: Raw DataFrame
    :return: Cleaned DataFrame containing only PlayStation games
    """
    # Convert year and scores to numeric
    df['Year_of_Release'] = pd.to_numeric(df['Year_of_Release'], errors='coerce')
    df['User_Score'] = pd.to_numeric(df['User_Score'], errors='coerce')
    # Convert sales columns to numeric
    for col in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # Drop rows missing release year or global sales
    df = df.dropna(subset=['Year_of_Release', 'Global_Sales'])
    # Trim text fields
    for col in ['Name', 'Platform', 'Genre', 'Publisher', 'Developer']:
        df[col] = df[col].astype(str).str.strip()
    # Filter to PlayStation platforms
    ps_df = df[df['Platform'].str.startswith('PS', na=False)].copy()
    return ps_df


def top_games_by_sales(ps_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top n PlayStation games by global sales.

    :param ps_df: Cleaned DataFrame filtered to PlayStation games
    :param n: Number of top games to return
    :return: DataFrame with Name, Platform and Global_Sales columns
    """
    grouped = (ps_df.groupby(['Name', 'Platform'])['Global_Sales']
                     .sum()
                     .reset_index()
                     .sort_values('Global_Sales', ascending=False)
                     .head(n))
    return grouped


def genre_sales_plot(ps_df: pd.DataFrame, output_path: Optional[str] = None) -> pd.Series:
    """Plot total global sales per genre for PlayStation games.

    :param ps_df: Cleaned DataFrame filtered to PlayStation games
    :param output_path: Optional path to save the plot as a PNG
    :return: Series of total sales per genre
    """
    genre_sales = ps_df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
    # Plot
    plt.figure(figsize=(10, 5))
    genre_sales.plot(kind='bar', title='Total Global Sales per Genre (PlayStation)')
    plt.ylabel('Global Sales (millions)')
    plt.xlabel('Genre')
    plt.tight_layout()
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
    return genre_sales


def main():
    """Main function for script execution."""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Video_Games.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Dataset not found at {data_path}. Please download Video_Games.csv and place it in the data folder."
        )
    raw_df = load_raw(data_path)
    ps_df = clean_dataframe(raw_df)
    # Print top games
    print("Top 10 PlayStation games by global sales:")
    print(top_games_by_sales(ps_df, 10))
    # Create a sales plot
    plot_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'genre_sales.png')
    genre_sales_plot(ps_df, plot_path)
    print(f"Genre sales plot saved to {plot_path}")


if __name__ == '__main__':
    main()