# %%
# Initial Imports
import pandas as pd
from pathlib import Path
from PIL import Image

import holoviews as hv
hv.notebook_extension('bokeh')
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
clusters_esg_df = pd.read_csv(Path('./dataframes/clusters_with_crypto.csv'), infer_datetime_format=True, parse_dates=True, index_col=[0]) 


# Plotting a scatter plot with sharpe ratios
total_esg_plot = ret_var_new.hvplot.scatter(by='clusters', y='sharpe', x='', hover_cols = ['Name', 'Returns', 'Variance'], title = 'Asset Clusters and Sharpe Ratios')

# Beginning the script to format our Streamlit App

st.set_page_config(
    layout = 'wide'
)

def main():

    # Adding radio buttons to sidebar for site navigation
    st.sidebar.title('Explore')
    pages = st.sidebar.radio(label = '', options=['Home', 'Methodology', 'Find and Compare Stocks', 'Data and Tables', 'Plots'])

    if "page" not in st.session_state:
        st.session_state.page = 'Home'
    if "current_ticker" not in st.session_state:
        st.session_state.current_ticker = ''
    if "cluster_view" not in st.session_state:
        st.session_state.cluster_view = False
    if "ticker_cluster" not in st.session_state:
        st.session_state.ticker_cluster = 0
        
    
    
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
                visualize the possibilities of enhancing the ESG impacts of assets within those indices.  **In this application we focus\
                on environment scores, but these methods could easily be applied to social or governance scores.**\
                To explore further select an option from the sidebar menu.")
    
    
    elif pages == 'Methodology':
        # Brief overview of the tools and methods used in the application
        st.session_state.page = 'Methodology'
        st.subheader('Tools and Methodology')
        st.markdown('#### KMeans Clustering')
        st.markdown('In order to group our stocks according to their return profiles, we\
        pulled historical price data going back 720 days from the Alpaca Trade API.\
        We then converted our dataframe to percent change of returns in order to normalize\
        the data so it could be clustered.  **It should be noted that typically KMeans\
        takes in multiple features from each item to be clustered, thus this is in no way\
        meant to be an example of what someone might ultimately feed the ML model to produce\
        the most accurate predictions.**  It is simply a way to visualize and illustrate the\
        possibilities that exist when using unsupervised learning to cluster stock data.\
        For more information on KMeans clustering from sci-kit learn, please visit their\
        [website]("https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html").')
        
        st.markdown('In order to find the optimal number of clusters to use for our KMeans model,\
        we utilized the elbow method.  The code can be found in the repository, but as illustrated below, the chart\
        that is generated from this approach is assessed to find the "elbow" or point at which adding more clusters is\
        no longer contributing to the accuracy or relevance of the model.  After charting we noticed an outlier,\
        GE, and thus removed it from the dataset and re-ran the model to produce the clusters that were not skewed by it.')

        # KMeans elbow plot
        image = Image.open(Path('./charts/elbow_plot.png'))
        st.image(image, caption='KMeans Elbow Plot')

        st.markdown('#### ESG Scores')
        st.markdown('In order to retrieve ESG data for our stocks, we utilized a [rapid API]("esg-environmental-social-governance-data.p.rapidapi.com").\
        This is by no means an authoritative list and should not be regarded as such.  Again, these tools\
        are just for illustrative purposes.')

        # Description of Sharpe Ratio
        st.markdown('#### About Sharpe Ratios')
        st.markdown("In order to assess risk / return profiles of our assets, we utilize a common metric\
        known as a **Sharpe Ratio**.  To learn more about Sharpe Ratios and how they are used and calculated\
        visit Investopedia's Sharpe Ratio Page found [here.](https://www.investopedia.com/terms/s/sharperatio.asp)")


    elif pages == 'Find and Compare Stocks':
        st.session_state.page = 'Find and Compare Stocks'
        ticker_list = list(ret_var_new.index)
        if st.session_state.cluster_view == False:

            # Displaying a chart of all of our stocks clustered and plotted by Sharpe ratios
            st.bokeh_chart(hv.render(total_esg_plot, backend='bokeh'), use_container_width=True)  

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('The above chart is obviously very crowded, but illustrates the way that the assets\
                are clustered together, with the y-axis being their Sharpe ratios.  **In this application we focus\
                on environment scores, but these methods could easily be applied to social or governance scores.**\
                Select a stock or cryptocurrency in the adjacent selectbox to drill down and compare\
                it to others within its cluster.')

            with col2:
               
                # Create a form that takes in ticker, sets session state with ticker data, and then
                # refreshes page with relevant populated data
                with st.form('tickerSelect'):
                    input_ticker = st.selectbox(label = 'Select a ticker to compare', options = ticker_list)
                    lookup_ticker = st.form_submit_button('Lookup Ticker')
                    if lookup_ticker:
                        st.session_state.current_ticker = input_ticker
                        st.session_state.cluster_view = True
                        ticker_cluster = ret_var_new.loc[st.session_state.current_ticker]['clusters'].astype(int)
                        st.session_state.ticker_cluster = ticker_cluster
                        st.experimental_rerun()
                    
        elif st.session_state.cluster_view == True:
            # Displaying env score and sharpe ratio for current ticker as well as plotting
            # current cluster data via scatter plot

            # Create form to allow the user to change to a different ticker
            with st.form('clusterDisplay'):

                # Create a button to allow the user to compare another stock
                input_ticker = st.selectbox(label = 'Compare a different asset:', options = ticker_list)
                lookup_ticker = st.form_submit_button('Lookup Ticker')
                if lookup_ticker:
                    st.session_state.current_ticker = input_ticker
                    ticker_cluster = ret_var_new.loc[st.session_state.current_ticker]['clusters'].astype(int)
                    st.session_state.ticker_cluster = ticker_cluster
                    st.experimental_rerun()
          
            # Retrieving Sharpe Ratio and Return data for selected ticker
            cluster_df = pd.DataFrame(clusters_esg_df.loc[clusters_esg_df['clusters'] == st.session_state.ticker_cluster])
            ticker_env_score = cluster_df.loc[st.session_state.current_ticker]['environment_score']
            ticker_sharpe = cluster_df.loc[st.session_state.current_ticker]['sharpe']
            ticker_returns = cluster_df.loc[st.session_state.current_ticker]['Returns']

            # Displaying Sharpe and Return data, creating select box to filter by Sharpe or Returns
            st.markdown(f"Current ticker **{st.session_state.current_ticker}** is in Cluster  # **{st.session_state.ticker_cluster}**\
            .  Its environment rating is {ticker_env_score}.  Its Sharpe Ratio is {ticker_sharpe.round(2)} and Cumulative Returns are\
            {ticker_returns.round(2)}.")
            risk_return_choice = st.selectbox('Select a metric to filter by:', options=['Sharpe Ratio',\
            'Cumulative Returns'])

            if risk_return_choice == 'Sharpe Ratio':

                # Scatter plot of the cluster that the selected asset is in... env score and sharpe ratio
                cluster_scatter_sharpe = cluster_df.hvplot.scatter(y='sharpe', x='environment_score', height = 350, width=750,\
                hover_cols = ['Name', 'environment_score', 'Returns'], rot=90, color='green',\
                title = f'Cluster # {st.session_state.ticker_cluster} Environment Scores and Sharpe Ratios')
                st.bokeh_chart(hv.render(cluster_scatter_sharpe, backend='bokeh'))  

                # Scatter of all assets' Sharpe Ratios with an env score over 500
                st.markdown('**Below we drill down to those companies with environment scores over 500:**')
                env_df = cluster_df.loc[cluster_df['environment_score'] >= 500]
                env_cluster_scatter = env_df.hvplot.scatter(x='environment_score', y='sharpe', hover_color='red', hover_cols = ['Name', 'environment_score', 'Returns'], rot=90, title=f'Cluster {st.session_state.ticker_cluster} Environment Scores sorted by Sharpe ratios',\
                height=350, width=750, legend=True)
                st.bokeh_chart(hv.render(env_cluster_scatter, backend='bokeh'))

                # Display dataframe with asset's cluster
                st.markdown('**Below is a table of all assets within this cluster.  Click on column headers to sort\
                values by that column:**')
                st.dataframe(cluster_df)

            elif risk_return_choice == 'Cumulative Returns':

                # Scatter plot of the cluster that the selected asset is in... env score and Cumulative Returns
                cluster_scatter_returns = cluster_df.hvplot.scatter(y='Returns', x='environment_score', height = 350, width=750,\
                hover_cols = ['Name', 'environment_score', 'Returns'], rot=90, color='red',\
                title = f'Cluster # {st.session_state.ticker_cluster} Environment Scores and Returns')
                st.bokeh_chart(hv.render(cluster_scatter_returns, backend='bokeh'))  

                # Scatter of all assets' Cumulative Returns with an env score over 500
                st.markdown('**Below we drill down to those companies with environment scores over 500:**')
                env_df = cluster_df.loc[cluster_df['environment_score'] >= 500]
                env_cluster_scatter = env_df.hvplot.scatter(x='environment_score', y='sharpe', hover_color='red', hover_cols = ['Name', 'environment_score', 'Returns'], rot=90, title=f'Cluster {st.session_state.ticker_cluster} Environment Scores sorted by Sharpe ratios',\
                height=350, width=750, legend=True)
                st.bokeh_chart(hv.render(env_cluster_scatter, backend='bokeh'))

                # Display dataframe with asset's cluster
                st.markdown('**Below is a table of all assets within this cluster.  Click on column headers to sort\
                values by that column:**')
                st.dataframe(cluster_df)

            

    elif pages == 'Data and Tables':
        # Establish page state, introduce page layout
        st.session_state.page = 'Data and Tables'
        st.subheader('Data and Tables')
        st.markdown('It is important to keep in mind that some of this data may be **archived**, so do not assume that all data is current.')

        # Overview and select box with data choices
        data_choice = st.selectbox('Select a dataset to display below:', options = ['Stock and Crypto Price Data', 'Risk / Return Metrics with Clusters',\
        'ESG Scores', 'Returns Percent Change', 'Cluster 0 Data', 'Cluster 1 Data', 'Cluster 2 Data',\
        'Cluster 3 Data', 'Cluster 4 Data'])
        
        if data_choice == 'Stock and Crypto Price Data':
            st.dataframe(combined_returns_df)
        elif data_choice == 'Risk / Return Metrics with Clusters':
            st.dataframe(ret_var_new)
        elif data_choice == 'ESG Scores':
            st.dataframe(clusters_esg_df)
        elif data_choice == 'Returns Percent Change':
            st.dataframe(pct_change_df)
        elif data_choice == 'Cluster 0 Data':
            st.dataframe(cluster0_df)
        elif data_choice == 'Cluster 1 Data':
            st.dataframe(cluster1_df)
        elif data_choice == 'Cluster 2 Data':
            st.dataframe(cluster2_df)
        elif data_choice == 'Cluster 3 Data':
            st.dataframe(cluster3_df)
        elif data_choice == 'Cluster 4 Data':
            st.dataframe(cluster4_df)

    elif pages == 'Plots':
        st.session_state.page = 'Plots'
        # Establishing plot variables
        cluster0_plot = Image.open(Path('./charts/cluster0_plot.png'))
        cluster1_plot = Image.open(Path('./charts/cluster1_plot.png'))
        cluster2_plot = Image.open(Path('./charts/cluster2_plot.png'))
        cluster3_plot = Image.open(Path('./charts/cluster3_plot.png'))
        cluster4_plot = Image.open(Path('./charts/cluster4_plot.png'))
        initial_esg_plot = Image.open(Path('./charts/initial_esg_scatter.png'))
        initial_sharpe_plot = Image.open(Path('./charts/initial_sharpe_cluster.png'))
        plot_list = ['Cluster 0 Plot', 'Cluster 1 Plot', 'Cluster 2 Plot', 'Cluster 3 Plot', 'Cluster 4 Plot', 'Initial ESG Plot', 'Initial Sharpe Plot']

        # Multiselect to display plots
        plot_select = st.selectbox('Select which plot(s) to display', options = plot_list)
        if plot_select == 'Cluster 0 Plot':
            st.image(cluster0_plot)
        elif plot_select == 'Cluster 1 Plot':
            st.image(cluster1_plot)
        elif plot_select == 'Cluster 2 Plot':
            st.image(cluster2_plot)
        elif plot_select == 'Cluster 3 Plot':
            st.image(cluster3_plot)
        elif plot_select == 'Cluster 4 Plot':
            st.image(cluster4_plot)
        elif plot_select == 'Initial ESG Plot':
            st.image(initial_esg_plot)
        else:
            st.image(initial_sharpe_plot)
        
if __name__ == "__main__":
    main()




# %%
