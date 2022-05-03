# %%
# Initial Imports
import pandas as pd
import hvplot.pandas
from pathlib import Path
import datetime as dt
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from utils.AlpacaFunctions import get_historical_dataframe, get_crypto_bars

import hvplot.pandas
import matplotlib.pyplot as plt
import plotly as pty
import plotly.express as px
import holoviews as hv
hv.notebook_extension('bokeh')
import matplotlib.pyplot as plt
import streamlit as st


# Since we will use archived data for demonstration purposes, we will go ahead and read in our saved .csv files
# Combined returns
combined_returns_df = pd.read_csv(Path('./dataframes/combined_returns.csv'), infer_datetime_format=True, index_col = 'timestamp')

# Combined Percent Change
pct_change_df = pd.read_csv(Path('./dataframes/combined_pct_change.csv'), infer_datetime_format=True, index_col = 'timestamp')

# Returns / variance
ret_var_new = pd.read_csv(Path('./dataframes/ret_var_new_df.csv'), infer_datetime_format=True, index_col = [0])

# Cluster 0 Data
cluster0_df = pd.read_csv(Path('./dataframes/cluster0_df.csv'), infer_datetime_format=True, parse_dates=True, index_col=[0])

# Cluster 1 Data
cluster1_df = pd.read_csv(Path('./dataframes/cluster1_df.csv'), infer_datetime_format=True, parse_dates=True, index_col=[0])

# Cluster 2 Data
cluster2_df = pd.read_csv(Path('./dataframes/cluster2_df.csv'), infer_datetime_format=True, parse_dates=True, index_col=[0])

# Cluster 3 Data
cluster3_df = pd.read_csv(Path('./dataframes/cluster3_df.csv'), infer_datetime_format=True, parse_dates=True, index_col=[0])

# Cluster 4 Data
cluster4_df = pd.read_csv(Path('./dataframes/cluster4_df.csv'), infer_datetime_format=True, parse_dates=True, index_col=[0])

# Combined ESG with clusters, sharpe, std, annual returns
clusters_esg_df = pd.read_csv(Path('./dataframes/clusters_esg_df.csv'), infer_datetime_format=True, parse_dates=True, index_col=[0]) 


# Plotting a scatter plot with sharpe ratios
ret_var_new.hvplot.scatter(by='clusters', y='sharpe', hover_cols = ['Returns', 'Variance'])


# Now we can plot our dataframe grouping by clusters and env, social scores, etc.
clusters_esg_df.hvplot.scatter(by='clusters', y='sharpe', hover_cols = ['Name', 'environment_score', 'social_score', 'governance_score', 'Returns'], rot=90)

# Below we plot our cluster 0 assets using their environment scores and sharpe ratios... this will help us visualize 
# and compare the cluster assets to find higher sharpe ratios combined with higher environent scores.  We could 
# easily do the same with social scores and governance scores.

cluster0_df.hvplot.scatter(y='sharpe', x='environment_score', hover_cols = ['Name', 'environment_score', 'Returns'], rot=90)

# Repeating the above process for cluster 1

cluster1_df.hvplot.scatter(y='sharpe', x='environment_score', hover_cols = ['Name', 'environment_score', 'Returns'], rot=90)

# Cluster 2 plot, bearing in mind ETH is in this cluster but does not have an env score 
cluster2_df.hvplot.scatter(y='sharpe', x='environment_score', hover_cols = ['Name', 'environment_score', 'Returns'], rot=90)

# Cluster 3 plot
cluster3_df.hvplot.scatter(y='sharpe', x='environment_score', hover_cols = ['Name', 'environment_score', 'Returns'], rot=90)

# Cluster 4 plot
cluster4_df.hvplot.scatter(y='sharpe', x='environment_score', hover_cols = ['Name', 'environment_score', 'Returns'], rot=90)


# Beginning the script to format our Streamlit App

def main():

    # Adding radio buttons to sidebar for site navigation
    st.sidebar.title('Explore')
    pages = st.sidebar.radio(label = '', options=['Home', 'Methodology', 'Find and Compare Stocks', 'Data and Tables', 'Plots'])

    if "page" not in st.session_state:
        st.session_state.page = 'Home'
    
    
    if pages == 'Home':
        st.session_state.page = 'Home'
        st.title("ESG Stock and Crypto Clustering")
        st.subheader("A tool for clustering stocks and cryptocurrencies, comparing their ESG scores vs. risk / return metrics.")

        # Disclaimer
        
        st.markdown('**Disclaimer: This tool should not in any way be considered financial advice.  It is for demonstration only.**')
        
        st.markdown("ESG (Environment, Social, Governance) investing has become a very important tool\
                for those seeking to invest in companies that are, or seeking to become, more conscious of their\
                impact in these areas.  This tool is designed to cluster stocks with similar risk / returns metrics\
                and compare their ESG scores along with their return profiles.  We have also included two **cryptocurrencies**\
                (Ethereum and Bitcoin) to our clusters.  While crypto investing has become extraordinarily\
                popular, there are concerns about crypto mining's impact on the environment.  Theoretically these\
                impacts could be mitigated by shifting other asset allocation to more environmentally friendly ones.\
                By utilizing KMeans clustering, ESG scores, and historical price data for the Nasdaq and S&P 500 stocks, we can investigate and\
                visualize the possibilities of enhancing the ESG impacts of assets within those indices.  To explore further\
                select an option from the sidebar menu.")
    
    
    elif pages == 'Methodology':
        st.session_state.page = 'Methodology'
        ''

    elif pages == 'Find and Compare Stocks':
        ''
                
if __name__ == "__main__":
    main()



