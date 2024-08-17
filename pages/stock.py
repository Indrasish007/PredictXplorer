
import streamlit as st
import datetime as dt
import yfinance as yf 
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly  import graph_objs as go
import pandas as pd

# Custom CSS to style the page
st.markdown("""
    <style>
        .main {
            background-color: Black;
        }
        h1 {
            color: #87CEEB;
            text-align: center;
            font-family: 'Trebuchet MS', sans-serif;
            font-size: 3em;
        }
        .stButton>button {
            background-color: #87CEEB;
            color: Black;
            font-size: 1.2em;
            font-family: 'Trebuchet MS', sans-serif;
            border-radius: 12px;
        }
        .stButton>button:hover {
            background-color: #357ABD;
            color: white;
        }
        .css-18e3th9 {
            padding-top: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

empty_col,col1,col2,col3,col4=st.columns([0.15,1,1,1,1])
with col1:
    if st.button("Home Page"):
        st.switch_page("app.py")
with col2:
     if st.button("Whatsapp Chat Analyzer"):
        st.switch_page("pages/whatsapp.py")
with col3:
    if st.button("Car Price Prediction"):
        st.switch_page("pages/car.py")
with col4:
    if st.button("Stock Price Prediction"):
        st.switch_page("pages/stock.py")

START="2015-01-01"
TODAY=dt.date.today().strftime("%Y-%m-%d")


# Load popular stock tickers and names
@st.cache_data
def load_popular_stocks():
    df = pd.read_csv('stocks.csv', header=None)
    stock_list = []
    for ticker in df[0].tolist():
        stock_info = yf.Ticker(ticker)
        stock_name = stock_info.info.get('longName', ticker)
        stock_list.append((stock_name, ticker))
    return stock_list

stocks = load_popular_stocks()

st.title("Stock prediction app")
selected_stock_name, selected_ticker = st.selectbox(
    "Select dataset for prediction", stocks, format_func=lambda x: x[0]
)

n_years=st.slider("Years of prediction:", 1, 4)
period=n_years*365

@st.cache_data
def load_data(ticker):
    data=yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state=st.text("Loading data...")
data=load_data(selected_ticker)
data_load_state.text("Loading data... done!")

st.subheader("Raw data")
st.write(data.tail())

def plot_raw_data():
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='stock_close'))
    fig.update_layout(title_text="Time Series Data",xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting
df_train=data[['Date','Close']]
df_train=df_train.rename(columns={"Date":"ds","Close":"y"})
m=Prophet()
m.fit(df_train)
#make future dataframe and predict
future=m.make_future_dataframe(periods=period)
forecast=m.predict(future)

st.subheader("Forecast data")
st.write(forecast.tail())
st.write('Forecast data')
fig1=plot_plotly(m,forecast)
fig1.update_traces(line=dict(color='cyan'))
fig1.update_layout(
    plot_bgcolor='white',  # Set plot background color
    paper_bgcolor='black',  # Set the surrounding background color
    font=dict(color='yellow')  # Set font color
)
st.plotly_chart(fig1)
st.write("Forecast components")
fig2=m.plot_components(forecast)
st.write(fig2)

# import streamlit as st
# import datetime as dt
# import yfinance as yf 
# from prophet import Prophet
# from prophet.plot import plot_plotly
# from plotly  import graph_objs as go
# import pandas as pd

# # Custom CSS to style the page
# st.markdown("""
#     <style>
#         .main {
#             background-color: Black;
#         }
#         h1 {
#             color: #87CEEB;
#             text-align: center;
#             font-family: 'Trebuchet MS', sans-serif;
#             font-size: 3em;
#         }
#         .stButton>button {
#             background-color: #87CEEB;
#             color: Black;
#             font-size: 1.2em;
#             font-family: 'Trebuchet MS', sans-serif;
#             border-radius: 12px;
#         }
#         .stButton>button:hover {
#             background-color: #357ABD;
#             color: white;
#         }
#         .css-18e3th9 {
#             padding-top: 1.5rem;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# col1,col2,col3,col4=st.columns([1,1,1,1])
# with col1:
#     if st.button("Home Page"):
#         st.switch_page("app.py")
# with col2:
#      if st.button("Whatsapp Chat Analyzer"):
#         st.switch_page("pages/whatsapp.py")
# with col3:
#     if st.button("Car Price Prediction"):
#         st.switch_page("pages/car.py")
# with col4:
#     if st.button("Stock Price Prediction"):
#         st.switch_page("pages/stock.py")

# START="2015-01-01"
# TODAY=dt.date.today().strftime("%Y-%m-%d")



# def load_popular_stocks():
#     df = pd.read_csv('stocks.csv', header=None)
#     return df[0].tolist()

# stocks = load_popular_stocks()


# st.title("Stock prediction app")
# # stocks=("AAPL","GOOG","MSFT","GME")
# selected_stocks=st.selectbox("Select datasert for prediction ",stocks)

# n_years=st.slider("Years of prediction :",1,4)
# period=n_years*365

# @st.cache_data
# def load_data(ticker):
#     data=yf.download(ticker,START,TODAY)
#     data.reset_index(inplace=True)
#     return data
# data_load_state=st.text("load data...")
# data=load_data(selected_stocks)
# data_load_state.text("loading data... done!")

# st.subheader("Raw data")
# st.write(data.tail())

# def plot_raw_data():
#     fig=go.Figure()
#     fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='stock_open'))
#     fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='stock_close'))
#     fig.update_layout(title_text="Time Series Data",xaxis_rangeslider_visible=True)
#     st.plotly_chart(fig)
# plot_raw_data()

# #Forecasting
# df_train=data[['Date','Close']]
# df_train=df_train.rename(columns={"Date":"ds","Close":"y"})
# m=Prophet()
# m.fit(df_train)
# future=m.make_future_dataframe(periods=period)
# forecast=m.predict(future)

# st.subheader("Forecast data")
# st.write(forecast.tail())
# st.write('Forecast data')
# fig1=plot_plotly(m,forecast)
# st.plotly_chart(fig1)
# st.write("Forecast components")
# fig2=m.plot_components(forecast)
# st.write(fig2)