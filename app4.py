import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title = 'This is a decentralized application that facilitates an ecosystem of donors, non-profits, and end users in the distribution of aid',
    page_icon = 'Resources/CommunityConnect_image.png'
)

from utils.contract import load_contract, get_provider
from providers.providerPages import page_addProvider, page_updateProvider, page_viewProviders
from patients.patientPages import page_addPatient, page_updatePatient, page_viewMyPatients, page_viewPatients
from requests2.requestPages import page_newRequest, page_viewRequests
from login_component import login_component



contract = load_contract()
w3, node_provider = get_provider()





# Function to convert USD to wei using yahoo finance api
def usdToWei(dollars):
    eth_df = yf.download(tickers="ETH-USD",period="today")
    eth_usd = eth_df.iloc[0]["Close"]
    to_ether = float(dollars) / float(eth_usd)
    to_wei = w3.toWei(to_ether, 'ether') 

    return to_wei

# Function converting wei to USD
def weiToUSD(wei):
    eth_df = yf.download(tickers="ETH-USD",period="today")
    eth_usd = eth_df.iloc[0]["Close"]
    st.write(eth_usd)
    ether = w3.fromWei(wei, 'ether')
    USD = float(ether) * float(eth_usd)
    
    return USD

if "page" not in st.session_state:
    st.session_state.page = "Login Page"
         
if "requestPageStatus" not in st.session_state:
    st.session_state.requestPageStatus = "makeRequest"

if "sortKey" not in st.session_state:
    st.session_state.sortKey = "Date Submitted"

if 'patientId' not in st.session_state:
    st.session_state.patientId = 0

if 'showPatient' not in st.session_state:
    st.session_state.showPatient = False

if 'userStatus' not in st.session_state:
    st.session_state.userStatus = 'Login'

if 'PAGES' not in st.session_state:
    st.session_state.PAGES = []


def main():

    
    if st.session_state.page == "Login Page":
        st.header('Welcome to Community Connect.  Please Login Below to Get Started:')
        login_component()
        col1, col2, col3 , col4, col5 = st.columns(5)
        with col1:
            pass
        with col2:
            pass
        with col4:
            pass
        with col5:
            pass
        with col3 :
            submitted = st.button('Login')
        if submitted:
            st.session_state.page = "Home"
            st.session_state.userStatus = "Owner"
            st.experimental_rerun()

    else: 
        st.sidebar.title("Welcome to Community Connect App, Owner")
        st.sidebar.subheader("Please select an option on the sidebar to get started")
        st.session_state.page = st.sidebar.radio('', options=tuple(st.session_state.PAGES.keys()))
        st.sidebar.markdown("""---""")
        st.session_state.PAGES[st.session_state.page]()


if st.session_state.userStatus == "Owner" or st.session_state.userStatus == "":    
    st.session_state.PAGES = {

    "Add Patient": page_addPatient,
    "Update Patient": page_updatePatient,
    "View Patients": page_viewPatients,
    "Make Request": page_newRequest,
    "View Open Requests": page_viewRequests,
    "New Provider": page_addProvider, 
    "Update Provider": page_updateProvider,
    "View Providers" : page_viewProviders
}

elif st.session_state.userStatus == 'Provider':

    st.session_state.PAGES = {

    "Add Patient": page_addPatient,
    "Update Patient": page_updatePatient,
    "View My Patients": page_viewMyPatients,
    "Make Request": page_newRequest,
    "View Open Requests": page_viewRequests,
    "Update Provider": page_updateProvider,
    "View Providers" : page_viewProviders
}

elif st.session_state.userStatus == 'Manager':

    st.session_state.PAGES = {

    "Add Patient": page_addPatient,
    "Update Patient": page_updatePatient,
    "View Patients": page_viewPatients,
    "Make Request": page_newRequest,
    "View Open Requests": page_viewRequests,
    "New Provider": page_addProvider,
    "Update Provider": page_updateProvider,
    "View Providers" : page_viewProviders
}

                
if __name__ == "__main__":
    main()








