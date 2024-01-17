import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pandas_market_calendars as mcal
from pandas.tseries.offsets import CustomBusinessDay
import streamlit as st
import hydralit_components as hc
import time
import hydralit as hy
import plotly.express as px

# List of 5 example stock tickers
stocks = [
    'FIS', 'AR', 'CNC', 'IBKR', 'WBD', 'KIM', 'WCC', 'FG', 'CWEN', 'AWK', 'ZM', 'AIRC', 'EMR', 'BRX', 'BC', 'MTG', 'WTFC',
    'ICE', 'PSX', 'GM', 'ET', 'AEP', 'BK', 'EXC', 'CEG', 'YUM', 'ALL', 'XEL', 'VICI', 'GPN', 'LYB', 'DVN', 'FANG', 'DAL',
    'XYL', 'RKT', 'TROW', 'FWONK', 'CUK', 'EQR', 'PHM', 'ETR', 'WAB', 'CTRA', 'RF', 'NTRS', 'CMS', 'SUI', 'J', 'SNA'
]

app = hy.HydraApp(title='Sokat Portfolio Analysis App')

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image('sokat.jpg')

@app.addapp(is_home=True)
def my_home():
    hy.info('Hello from Home!')

@app.addapp(title='The Portfolio')
def app2():
    with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[3,0,5]):
        time.sleep(5)

    def color_gain_loss(val):
        color = '#9fe2bf' if val >= 0 else '#fa8072'
        return f'background-color: {color}'


    nyse = mcal.get_calendar('NYSE')


    # Function to fetch stock data for a given ticker symbol
    def get_stock_data(ticker, start_date, end_date):
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        return data

    # Dates for analysis
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date_day = (
        (pd.to_datetime((datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')) -
        pd.tseries.offsets.CustomBusinessDay(1, holidays=nyse.holidays().holidays)).to_pydatetime()).strftime('%Y-%m-%d')
    start_date_week = (
        (pd.to_datetime((datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')) -
        pd.tseries.offsets.CustomBusinessDay(1, holidays=nyse.holidays().holidays)).to_pydatetime()).strftime('%Y-%m-%d')
    start_date_month = (
        (pd.to_datetime((datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')) -
        pd.tseries.offsets.CustomBusinessDay(1, holidays=nyse.holidays().holidays)).to_pydatetime()).strftime('%Y-%m-%d')
    start_date_quarter = (
        (pd.to_datetime((datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')) -
        pd.tseries.offsets.CustomBusinessDay(1, holidays=nyse.holidays().holidays)).to_pydatetime()).strftime('%Y-%m-%d')
    inception_date = '2023-12-19'

    # Empty lists to store results
    day_returns = []
    week_returns = []
    month_returns = []
    quarter_returns = []
    since_inception_returns = []

    # Fetching data and calculating returns
    for stock in stocks:
        data = get_stock_data(stock, start_date_quarter, end_date)
        day_return = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
        week_return = ((data['Close'].iloc[-1] - data['Close'].loc[start_date_week]) / data['Close'].loc[start_date_week]) * 100
        month_return = (
                (data['Close'].iloc[-1] - data['Close'].loc[start_date_month]) / data['Close'].loc[start_date_month]) * 100
        quarter_return = (
                (data['Close'].iloc[-1] - data['Close'].loc[start_date_quarter]) / data['Close'].loc[start_date_quarter]) * 100
        since_inception_return = (
                (data['Close'].iloc[-1] - data['Close'].loc[inception_date]) / data['Close'].loc[inception_date]) * 100        

        day_returns.append(round(day_return, 2))
        week_returns.append(round(week_return, 2))
        month_returns.append(round(month_return, 2))
        quarter_returns.append(round(quarter_return, 2))
        since_inception_returns.append(round(since_inception_return, 2))

    # Creating DataFrame
    data = {
        'Stock': stocks,
        'Day-over-Day': day_returns,
        'Week-over-Week': week_returns,
        'Month-over-Month': month_returns,
        'Quarter-over-Quarter': quarter_returns,
        'Since Inception': since_inception_returns
    }

    df = pd.DataFrame(data)

    # Streamlit web app
    st.header('Stock Portfolio Performance', divider='blue')
    st.write('* All values are in percent')
    st.write('* Inception date is 19th December 2023')
    st.dataframe(df.style.format(precision=2).background_gradient(cmap='RdYlGn',
                                                    subset=['Day-over-Day', 'Week-over-Week', 'Month-over-Month',
                                                            'Quarter-over-Quarter', 'Since Inception'], axis=None), hide_index=True, height=1800)

@app.addapp(title='Portfolio vs Benchmark')
def app3():
    portfolio_val = pd.read_csv('portfolio_val.csv')
    # plt.figure(figsize=(10, 6))

    # plt.plot(portfolio_val['Date'], portfolio_val['Sokat_portfolio_val'], label='Sokat Portfolio Value', marker='o')
    # plt.plot(portfolio_val['Date'], portfolio_val['IWS_Portfolio_Val'], label='IWS Portfolio Value', marker='o')

    # # Formatting the axes and legends
    # plt.title('Visualization of Portfolio Values Over Time')
    # plt.xlabel('Date')
    # plt.ylabel('Portfolio Value')
    # plt.xticks(rotation=45)
    # plt.grid(True)
    # plt.legend()

    # # Formatting y-axis to display dollar values
    # plt.gca().yaxis.set_major_formatter('${x:,.0f}')

    # st.pyplot(plt.gcf())

    # Create a Plotly line chart
    fig = px.line(portfolio_val, x='Date', y=['Sokat_portfolio_val', 'IWS_Portfolio_Val'],
                labels={'value': 'Portfolio Value'},
                title='Portfolio Values Over Time',
                line_shape="linear",  # Choose line shape (linear, spline, hv, vh, hvh, or vhv)
                line_dash_sequence=['solid', 'dot'],  # Set line dash sequence
                )

    # Format axes and legends
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Portfolio Value',
        legend_title='Columns',
        hovermode='x unified',  # Display hover information for both lines at the same time
        xaxis=dict(
            tickformat='%b %d, %Y',  # Format x-axis date display
            tickmode='auto',
            nticks=10,
        ),
    )

    st.plotly_chart(fig, theme='streamlit')

app.run()