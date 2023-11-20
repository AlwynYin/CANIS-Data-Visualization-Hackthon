import os

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from plot import horizontal_bar

dirname = os.path.dirname(__file__)
path = os.path.join(dirname, "data/")

data_df = pd.read_csv(path + "results.csv")

languages = data_df["Language"].unique()
options_lan = [
    dict(label=key, value=key)
    for key in languages
]
# print(options_lan)
regions = data_df["Region"].unique()
regions.sort()
options_reg = [
    dict(label=key, value=key)
    for key in regions
]

medias = ["Twitter", "Facebook", "Instagram", "Threads", "Youtube", "Tiktok", "Max_media", "All_media"]
options_med = [
    dict(label=med, value=med)
    for med in medias
]
# print(options_reg)

# --------------------------------- Pie Chart -----------------------

count_sunburst = px.sunburst(
    data_df,
    path=["States", "Specific", "Region"],
    color_discrete_sequence=px.colors.cyclical.Twilight,
).update_traces(hovertemplate="%{label}<br>" + "Media Count: %{value}")

count_sunburst = count_sunburst.update_layout(
    {
        "margin": dict(t=0, l=0, r=0, b=10),
        "paper_bgcolor": "#F9F9F8",
        "font_color": "#363535",
    }
)

sum_sunburst = px.sunburst(
    data_df,
    path=["States", "Specific", "Region"],
    values="All_media_fol",
    # color="Group",
    color_discrete_sequence=px.colors.cyclical.HSV,
).update_traces(
    hovertemplate="%{label}<br>" + "Followers: %{value}",
    textinfo="label + percent entry",
)

sum_sunburst = sum_sunburst.update_layout(
    {
        "margin": dict(t=0, l=0, r=0, b=10),
        "paper_bgcolor": "#F9F9F8",
        "font_color": "#363535",
    }
)

drop_reg = dcc.Dropdown(
    id="drop_reg",
    clearable=False,
    searchable=True,
    options=options_reg,
    value='China',
    style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
)

drop_lan = dcc.Dropdown(
    id="drop_lan",
    # clearable=False,
    searchable=True,
    multi=True,
    options=options_lan,
    value='Chinese',
    style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
)

drop_med = dcc.Dropdown(
    id="drop_med",
    searchable=True,
    multi=True,
    options=options_med,
    value="All_media",
    style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
)

options_des = {"Top": 'Top', "Bottom": "Bottom"}

drop_des = dcc.Dropdown(
    id="drop_des",
    searchable=False,
    multi=False,
    options=options_des,
    value="Top",
    style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
)

input_rows = dcc.Input(id='num_rows', type='number', value=10, min=1, max=100, step=1,
                       style={"margin": "4px", 'height': "30px"})

# ------------------------------------------------------ APP ------------------------------------------------------

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    [
        html.Div(
            # sidebar
            [
                html.H1(children="Media Navigator"),
                html.Label(
                    "the interactive gateway to visualizing China's media influence worldwide. Explore our charts to "
                    "see where and how China's voice resonates globally. Discover, engage, and gain insights into a "
                    "world of media shaped by one of the largest players in the digital age. Start your journey into "
                    "the landscape of global media with us today.",
                    style={"color": "rgb(33 36 35)"},
                ),
            ],
            className="side_bar",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                # pie chart left
                                html.Div(
                                    [
                                        html.Label(
                                            "1. Sphere of Influence: Followers’ Distribution",
                                            style={"font-size": "medium"},
                                        ),
                                        html.Br(),
                                        html.Label(
                                            "This sunburst chart is based on the number of media entities "
                                            "in the region",
                                            style={"font-size": "9px"},
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        dcc.Graph(id="count", figure=sum_sunburst),
                                    ],
                                    id="followers_div",
                                    className="box",
                                    style={"width": "50%"},
                                ),
                                # pie chart 2
                                html.Div(
                                    [
                                        html.Label(
                                            "2. Digital Diversity: China's Media Spectrum",
                                            style={"font-size": "medium"},
                                        ),
                                        html.Br(),
                                        html.Label(
                                            "This sunburst chart is  based on the number of me"
                                            "dia entities in the region",
                                            style={"font-size": "9px"},
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        dcc.Graph(figure=count_sunburst, id="followers"),
                                    ],
                                    className="box",
                                    style={"width": "50%"},
                                ),
                            ],
                            className="row",
                        ),
                        # top box
                        html.Div(
                            [
                                html.Label("Choose the region, language, number of rows, and social media types"),
                                html.Br(),
                                html.Br(),
                                drop_reg,
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                drop_lan,
                                            ],
                                            style={
                                                "width": "60%"
                                            },
                                        ),
                                        html.Div(
                                            ["Number of media entites:"],
                                            style={
                                                "width": "15%"
                                            },
                                        ),
                                        html.Div(
                                            [
                                                input_rows,
                                                html.Br(),
                                                html.Br(),
                                            ],
                                            style={
                                                "width": "25%"
                                            },
                                        ),
                                    ],
                                    className="row",
                                ),
                                drop_med,
                                drop_des,
                            ],
                            className="box",
                            style={
                                "margin": "10px",
                                "padding-top": "15px",
                                "padding-bottom": "15px",
                            },
                        ),
                        html.Div(
                            [
                                # bar chart
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Label(id="title_bar"),
                                                dcc.Graph(id="bar_fig"),
                                            ],
                                            className="box",
                                            style={"padding-bottom": "15px"},
                                        ),
                                    ],
                                    style={"width": "100%"},
                                ),
                            ],
                            className="row",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            [
                                                "Authors",
                                                html.Br(),
                                                "Xinyue (Hecate) Li, Aiwei (Alwyn) Yin, Siyi (Sophia) Zhu,"
                                                " Yuchen (Clint) Hua",
                                                html.Br(),
                                                html.A("@hecatelixyue", href="https://github.com/hecateli"), " ",
                                                html.A("@AlwynYin", href="https://devpost.com/AlwynYin"), " ",
                                                html.A("@Sophiaaa12", href="https://devpost.com/Sophiaaa12"), " ",
                                                html.A("@Yuchen Hua", href="https://ca.linkedin.com/in/yuchen-hu"
                                                                           "a-89bb22250")
                                            ],
                                            style={"font-size": "12px"},
                                        ),
                                    ],
                                    style={"width": "60%"},
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            [
                                                "Sources",
                                                html.Br(),
                                                html.A(
                                                    "CANIS Data Visualization and Foreign Interference",
                                                    href="https://canis-hackathon-2.devpost.com/?ref_feature="
                                                         "challenge&ref_medium=your-open-hackathons&ref_content="
                                                         "Submissions+open",
                                                    target="_blank",
                                                ),
                                                html.Br(),
                                                "View the project on ", 
                                                html.A("Github", href="https://github.com/AlwynYin/CANIS-Data-Visualization-Hackthon")
                                            ],
                                            style={"font-size": "12px"},
                                        )
                                    ],
                                    style={"width": "37%"},
                                ),
                            ],
                            className="footer",
                            style={"display": "flex"},
                        ),
                    ],
                    className="main",
                ),
            ]
        ),
    ]
)


# ------------------------------------------------------ Callbacks -----------------------------------------------------


@app.callback(
    [
        Output("title_bar", "children"),
        Output("bar_fig", "figure"),
    ],
    [Input("drop_reg", "value"),
     Input("drop_lan", "value"),
     Input("num_rows", "value"),
     Input("drop_med", "value"),
     Input("drop_des", "value")
     ],
)
def bar_chart(region, languages, num_rows, medias, top):
    adj = "highest" if top == "Top" else "lowest"
    title = f"Bar chart with {num_rows} {adj} media in {region}"

    if isinstance(languages, list):
        lang = languages
    else:
        lang = [languages]
    # print(lang)

    if isinstance(medias, list):
        meds = medias
    else:
        meds = [medias]

    return (
        title,
        horizontal_bar(data_df, [region], languages=lang, medias=meds, num_entities=num_rows, top=(top == "Top"))
    )


@app.callback(Output('drop_reg', 'value'), [Input('followers', 'clickData'), Input('count', 'clickData')])
def display_selected(data1, data2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    region = None
    if 'followers' in changed_id:
        region = data1['points'][-1]['label']
    if 'count' in changed_id:
        region = data2['points'][-1]['label']
    if region is None:
        return dash.no_update
    if region not in regions:
        return dash.no_update
    return region


if __name__ == "__main__":
    app.run_server(debug=True)
