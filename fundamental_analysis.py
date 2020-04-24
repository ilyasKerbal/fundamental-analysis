from urllib.request import urlopen
import json
import pandas as pd

# Set global printing options
pd.options.display.max_columns = 20
pd.options.display.max_rows = 100

# Fetch the available company profiles
company_profiles = pd.read_csv('company_profiles.csv')


# ---------------------------------
# Select your circle of competence
# ---------------------------------
def select_sector(df, sector):
    """
    :param df: takes a df containing a 'sector' column
    :param sector: takes a string representing a sector
    :return: a df containing only companies in the specified sector
    """
    sector_filter = df['sector'] == sector
    sector_profiles = df[sector_filter]
    print('Found ' + str(len(sector_profiles)) + ' companies in the ' + sector + ' sector!')
    return sector_profiles


tech_companies = select_sector(company_profiles, 'Technology')


def select_industry(df, industry):
    """
    :param df: takes a df containing a 'industry' column
    :param industry: takes a string representing an industry
    :return: a df containing only companies in the specified industry
    """
    industry_filter = df['industry'] == industry
    industry_profiles = df[industry_filter]
    print('Found ' + str(len(industry_profiles)) + ' companies in the ' + industry + ' industry!')
    return industry_profiles


# ---------------------------------
# Fetch Financial Ratios
# ---------------------------------
# Create function to fetch profitability ratios directly from Financial Modeling Prep API

def get_financial_ratios(df):
    """
    :param df: takes a df containing a "symbol" (stock ticker) column as input
    :return: a df of financial ratios for every symbol (stock ticker) with available data
    """
    print('Looking for financial ratios for ' + str(len(df)) + ' companies...')
    financial_ratios = pd.DataFrame()

    for ticker in df['symbol']:
        response = urlopen("https://financialmodelingprep.com/api/v3/financial-ratios/" + ticker)
        data = response.read().decode("utf-8")
        # Select stock tickers don't return any results - appears to be tickers that include a "."
        try:
            data_json = json.loads(data)['ratios']
            flattened_data = pd.json_normalize(data_json)
            flattened_data.insert(0, 'stock.ticker', ticker)
            financial_ratios = financial_ratios.append(flattened_data, ignore_index=True)
        except KeyError:
            continue

    financial_ratios.columns = financial_ratios.columns.str.split('.').str[1]
    financial_ratios.columns.values[1] = "date"

    print('Found financial ratio data for ' + str(financial_ratios['ticker'].nunique()) + ' companies!')

    return financial_ratios


tech_companies_test = tech_companies.iloc[0:10,]
test_ratios = get_financial_ratios(tech_companies_test)



# ------------------------------------------
# Filter #1: Profitability Ratios
# ------------------------------------------
# Filter out companies with negative GPM, OPM, or NPM in 2019

# # Subset df to profitability ratios we're concerned with
# subset_cols = test_ratios[['ticker', 'date', 'grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin']]
#
# # Subset df to latest reported profitability ratios (annual basis)
# subset_rows = subset_cols.groupby('ticker').head(1).drop_duplicates(['ticker'])
#
# # Convert ratios values to floats instead of strings
# subset_rows[['grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin']] \
#     = subset_rows[['grossProfitMargin', 'operatingProfitMargin', 'netProfitMargin']].apply(pd.to_numeric)
#
# # Filter out companies with negative GPM, OPM, or NPM
# keeper_stocks = subset_rows[(subset_rows['grossProfitMargin'] > 0)
#                             & (subset_rows['operatingProfitMargin'] > 0)
#                             & (subset_rows['netProfitMargin'] > 0)]
#
# print(keeper_stocks)

# -----------------------------------------------
# Filter #2: Profitability Ratio Trend
# -----------------------------------------------


# ---------------------------------
# Filter #3: Earnings Manipulation
# ---------------------------------

