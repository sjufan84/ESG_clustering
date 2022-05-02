# Module to define Monte Carlo functions that will be utilized repeatedly throughout the project

from utils.MCForecastTools import MCSimulation
import pandas as pd
import numpy as np



# Monte Carlo functions
def configure_monte_carlo(dataframe, weights = '', num_simulations, num_trading_days):
    simulation_input_df = MCSimulation(
    portfolio_data = dataframe,
    weights = '',
    num_simulation = num_simulations,
    num_trading_days = num_trading_days
    )
    return simulation_input_df

def run_monte_carlo(simulation_input_df):
    simulation_returns_df = simulation_input_df.calc_cumulative_return()
    return simulation_returns_df

def plot_simulation_outcomes(simulation_input_df):
    simulation_plot = simulation_input_df.plot_simulation()
    return simulation_plot

def plot_distribution(simulation_input_df):
    sim_dist_plot = simulation_input_df.plot_distribution()
    return sim_dist_plot

def get_monte_summary(simulation_input_df):
    summary_stats = simulation_input_df.summarize_cumulative_return()
    return summary_stats

def get_daily_returns(simulation_input_df, ticker):
    daily_returns = simulation_input_df.portfolio_data[ticker]['daily_return'].rename_axis(mapper = ticker, axis = 1)
    return daily_returns
    