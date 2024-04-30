# https://realpython.com/python-dash/
# cd C:\Users\ngoun\Downloads\python_cours\pratique_bambei\dash_test
# python311 -m virtualenv C:\Users\ngoun\Documents\dev_ops_all\python_soft\mes_envs\env_plotly_311
# C:\Users\ngoun\Documents\dev_ops_all\python_soft\mes_envs\env_plotly_311\Scripts\activate.ps1
# python -m pip install --upgrade pip
# pip install --no-cache-dir -r C:\Users\ngoun\OneDrive\devops\let_python_be\mes_envs\requirements_plotly_311.txt
# C:\Users\ngoun\Documents\dev_ops_all\python_soft\mes_envs\env_plotly_311\Scripts\deactivate.ps1

# data.year.value_counts()

# local code
# push to git
# git clone to server
# set env base on requirements.txt
# run code on server
# expose 8090 port -> 


import pandas as pd
from dash import Dash, dcc, html

## Code Python
data = (
    pd.read_csv(
        "datas\\avocado.csv",
        index_col=False,
        usecols=["Date", "AveragePrice", "Total Volume", "Total Bags", "Small Bags", "Large Bags","XLarge Bags", "type","year", "region"]
    )
    #.query("type == 'conventional' and region == 'Albany'")
    .query("type == 'conventional' and region == 'Atlanta'")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)

data_group = data[["Total Volume", "year"]].groupby(['year']).sum()

## code Web
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Avocado Analytics"),
        html.P(
            children=(
                "Analyze the behavior of avocado prices and the number"
                " of avocados sold in the US between 2015 and 2018"
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data_group.index,
                        "y": data_group["Total Volume"],
                        "type": "bar",
                        
                    },
                ],
                "layout": {"title": "Total Volume Each year"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8099",debug=True)