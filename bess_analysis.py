import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    return alt, pd


@app.cell
def _(pd):
    load_df = pd.read_csv("./electric_usage_report_09-01-2024_to_09-01-2025.csv")
    load_df["dt"] = pd.to_datetime(load_df["Day"].astype(str) + ' ' + load_df["Hour of Day"], format="%m/%d/%Y %I:%M %p")
    load_df = load_df[load_df["Hourly Total"] != "No Data"]
    load_df["Hourly Total"] = load_df["Hourly Total"].astype(float)
    load_df["Daily Total"] = load_df["Daily Total"].astype(float)
    load_df = load_df[["dt", "Hourly Total", "Daily Total"]]
    return (load_df,)


@app.cell
def _(load_df):
    load_df
    return


@app.cell
def _(pd):
    def time_of_day_short(timestamp: pd.Timestamp, kwh: float) -> float:
        # Weekday
        if timestamp.day_of_week < 5:
            # Off Peak
            if 15 <= timestamp.hour < 19:
                return 0.1764*kwh
            # On Peak
            else:
                if timestamp.month >= 6 and timestamp.month <= 9: # June - Sept
                    return 0.2339 * kwh
                else:
                    return 0.1912 * kwh
        else:
            return 0.1764 * kwh

    def time_of_day_long(timestamp: pd.Timestamp, kwh: float) -> float:
        # Off Peak
        if 11 <= timestamp.hour < 19:
            if 6 <= timestamp.month <= 10:
                return 0.1426 * kwh
            else:
                return 0.1405 * kwh
        else:
            if 6 <= timestamp.month <= 10:
                return 0.2480 * kwh
            else:
                return 0.2233 * kwh

    def overnight_savers(timestamp: pd.Timestamp, kwh: float) -> float:
        # Weekday (Mon 0, Fri 4)
        if timestamp.day_of_week < 5:
            # Super Off Peak
            if 1 <= timestamp.hour < 7:
                return 0.1134 * kwh
            # Off Peak
            elif 7 <= timestamp.hour < 15 or 19 <= timestamp.hour < 1:
                if 6 <= timestamp.month <= 9:
                    return 0.2430 * kwh
                else:
                    return 0.1498 * kwh
            # Peak
            else:
                if 6 <= timestamp.month <= 9:
                    return 0.3406 * kwh
                else:
                    return 0.1816 * kwh
        # Weekend
        else:
            # Super Off Peak
            if 1 <= timestamp.hour < 7:
                return 0.1134 * kwh
            # Off Peak
            else:
                if 6 <= timestamp.month <= 9:
                    return 0.2430 * kwh
                else:
                    return 0.1498 * kwh
    return overnight_savers, time_of_day_long, time_of_day_short


@app.cell
def _(load_df, overnight_savers, time_of_day_long, time_of_day_short):
    load_df["tod_short"] = load_df.apply(lambda x: time_of_day_short(x['dt'], x['Hourly Total']), axis=1)
    load_df["tod_long"] = load_df.apply(lambda x: time_of_day_long(x['dt'], x['Hourly Total']), axis=1)
    load_df["overnight_savers"] = load_df.apply(lambda x: overnight_savers(x['dt'], x['Hourly Total']), axis=1)
    load_df
    return


@app.cell
def _(load_df):
    load_df["tod_short"].sum(), load_df["tod_long"].sum(), load_df['overnight_savers'].sum()
    return


@app.cell
def _(alt, load_df, pd):
    # Calculate totals for each rate plan
    totals_data = pd.DataFrame({
        'Rate Plan': ['Time of Day (Short)', 'Time of Day (Long)', 'Overnight Savers'],
        'Total Cost ($)': [
            load_df["tod_short"].sum(),
            load_df["tod_long"].sum(),
            load_df['overnight_savers'].sum()
        ]
    })

    # Create horizontal bar chart
    chart = alt.Chart(totals_data).mark_bar().encode(
        x=alt.X('Total Cost ($):Q', title='Total Cost ($)'),
        y=alt.Y('Rate Plan:N', title='Rate Plan', sort='-x'),
        color=alt.Color('Rate Plan:N', legend=None)
    ).properties(
        title='Comparison of Total Costs by Rate Plan',
        height=200
    )

    chart
    return


if __name__ == "__main__":
    app.run()
