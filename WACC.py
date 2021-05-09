#wacc = kd * (1-Tc) * (D/D+E) + Ke * (E/D+E)

# Kd = Cost of debt
# Tc = Tax effective rate
# Ke = Cost of equity

import pandas_datareader as web
import datetime
import requests
import yfinance as yf
from config import *
from testfile import *
pd.set_option('display.max_column',None)
pd.set_option('display.max_rows',None)

# kd = RF + credit spread
# RF = risk free


def cost_of_debt(is_df, bs_df):
    CoD = is_df['Interest Expense'][1]*(1-0.21) / bs_df['Total Debt'][1]
    return CoD


def cost_of_equity(company):
    # RF
    RF = 0.025 # using bonds, in sweden they give 3% on 10 years

    # Beta
    stock = yf.Ticker(company)
    beta = stock.info['beta']

    # Market Return
    yearlyreturn = 0.077 # taken from a report from PwC

    cost_of_equity = RF + (beta * (yearlyreturn - RF))
    return cost_of_equity


#effective tax rate and capital structure
def wacc(company, is_df, bs_df):
    CoD = cost_of_debt(is_df, bs_df)
    CoE = cost_of_equity(company)
    #effective tax rate
    ETR = is_df['Tax Provision'][1]/is_df['Pretax Income'][1]
    #capital structure

    debt_to = bs_df['Total Debt'][1]/(bs_df['Common Stock Equity'][1] + bs_df['Total Debt'][1])
    equity_to = bs_df['Common Stock Equity'][1]/(bs_df['Common Stock Equity'][1] + bs_df['Total Debt'][1])

    #wacc
    WACC = (CoD*(1-ETR)*debt_to) + (CoE*equity_to)
    print(WACC,equity_to,debt_to)
    return WACC



