# DTE TOU Rate Analyzer

This notebook allows you to (roughly) estimate how much you would save when using different time-of-use plans offered to DTE residential customers. 


__Note__: I am not affiliated with DTE. This is my interpretation of DTE's tariff structure and may have errors or may not be up to date.

__Another Note__: You are unlikely to get a perfect 1:1 match between your energy cost on your bill and the output of this tool (for the TOU plan you currently use). This is best used to understand the *relative* difference between plans.



## How to use:

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Run `uv run marimo run`
3. Download a CSV of your hourly load data from DTEs [usage portal](usage.dteenergy.com)
4. Select the downloaded file for analysis

