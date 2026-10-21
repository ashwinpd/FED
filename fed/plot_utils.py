
import matplotlib.pyplot as plt


def plot_gdp(df):
    """Plot annual GDP for each country from 2000 to 2022."""

    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot one line for each country
    for country, country_data in df.groupby("country"):

        country_data = country_data.sort_values("year")

        ax.plot(
            country_data["year"],
            country_data["gdp_usd_trillions"],
            label=country,
            linewidth=2
        )

    # Add chart title and axis labels
    ax.set_title("GDP by Country (2000–2022)")
    ax.set_xlabel("Year")
    ax.set_ylabel("GDP (Current US$, Trillions)")

    # Add legend and grid
    ax.legend(title="Country")
    ax.grid(True, alpha=0.3)

    # Improve spacing
    fig.tight_layout()

    return fig, ax