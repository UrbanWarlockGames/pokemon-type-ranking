import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from sklearn.preprocessing import MinMaxScaler

def load_generation_data(gen):
    base_path = os.path.dirname(os.path.abspath(__file__))

    if gen == "GEN9":
        mono_file = "monotype_combinations.csv"
        dual_file = "dualtype_combinations.csv"
        triple_file = "tripletype_combinations.csv"
    else:
        mono_file = f"monotype_combinations{gen}.csv"
        dual_file = f"dualtype_combinations{gen}.csv"
        triple_file = f"tripletype_combinations{gen}.csv"

    mono = pd.read_csv(os.path.join(base_path, mono_file))
    dual = pd.read_csv(os.path.join(base_path, dual_file))
    triple = pd.read_csv(os.path.join(base_path, triple_file))

    # Add Combined Type columns
    dual["Combined Type"] = dual.apply(lambda row: '/'.join(filter(None, [str(row["First Type"]), str(row["Second Type"])])), axis=1)
    triple["Combined Type"] = triple.apply(lambda row: '/'.join(filter(None, [str(row["First Type"]), str(row["Second Type"]), str(row["Third Type"])])), axis=1)

    # Add Rank column based on Total Score
    for df in [mono, dual, triple]:
        df["Rank"] = df["Total Score"].rank(ascending=False, method="min").astype(int)
        df.sort_values("Rank", inplace=True)

    # Reorder Rank to be first column
    def move_rank_first(df):
        cols = list(df.columns)
        if "Rank" in cols:
            cols.insert(0, cols.pop(cols.index("Rank")))
            return df[cols]
        return df

    mono = move_rank_first(mono)
    dual = move_rank_first(dual)
    triple = move_rank_first(triple)

    # Normalise key scores
    scaler = MinMaxScaler()
    for col in ["Total Score", "Defensive Score", "Offensive Score"]:
        mono[f"Normalised {col}"] = scaler.fit_transform(mono[[col]]).round(4)
        dual[f"Normalised {col}"] = scaler.fit_transform(dual[[col]]).round(4)
        triple[f"Normalised {col}"] = scaler.fit_transform(triple[[col]]).round(4)

    return mono, dual, triple

# Initialise the Dash app
app = dash.Dash(__name__)

@app.server.route('/healthz')
def health_check():
    return "OK", 200

app.layout = html.Div([
    html.H1("Pokémon Type Rankings Viewer"),

dcc.Dropdown(
    id='generation-dropdown',
    options=[
        {'label': 'VI-IX', 'value': 'GEN9'},
        {'label': 'I', 'value': 'GEN1'},
        {'label': 'II-V', 'value': 'GEN5'},
    ],
    value='GEN9',  # Default selected generation
    clearable=False,
    style={'width': '300px'}
),

    html.H2("Monotype Rankings"),
    dash_table.DataTable(
        id='single-type-table',
        columns=[],
        data=[],
        sort_action="native",
        page_size=20,
        style_table={'overflowX': 'auto'},
    ),

    html.H2("Dual-Type Rankings"),
    dcc.Input(
        id='dual-type-search',
        type='text',
        placeholder='Search by Type',
    ),
    dash_table.DataTable(
        id='dual-type-table',
        columns=[],
        data=[],
        sort_action="native",
        page_size=20,
        style_table={'overflowX': 'auto'},
    ),

    html.H2("Tri-Type Rankings"),
    dcc.Input(
        id='triple-type-search',
        type='text',
        placeholder='Search by Type',
    ),
    dash_table.DataTable(
        id='triple-type-table',
        columns=[],
        data=[],
        sort_action="native",
        page_size=20,
        style_table={'overflowX': 'auto'},
    ),

    html.H2("Single-Type Rankings Visualisation"),
    dcc.RadioItems(
        id='score-type-radio',
        options=[
            {'label': 'Total', 'value': 'Normalised Total Score'},
            {'label': 'Defense', 'value': 'Normalised Defensive Score'},
            {'label': 'Offense', 'value': 'Normalised Offensive Score'}
        ],
        value='Normalised Total Score',
        inline=True
    ),
    dcc.Graph(id='single-type-visualisation'),

    html.H2("Dual-Type Rankings Visualisation"),
    dcc.RadioItems(
        id='dual-score-type-radio',
        options=[
            {'label': 'Total', 'value': 'Normalised Total Score'},
            {'label': 'Defense', 'value': 'Normalised Defensive Score'},
            {'label': 'Offense', 'value': 'Normalised Offensive Score'}
        ],
        value='Normalised Total Score',
        inline=True
    ),
    dcc.Graph(id='dual-type-visualisation'),

    html.H2("Triple-Type Rankings Visualisation"),
    dcc.RadioItems(
        id='triple-score-type-radio',
        options=[
            {'label': 'Total', 'value': 'Normalised Total Score'},
            {'label': 'Defense', 'value': 'Normalised Defensive Score'},
            {'label': 'Offense', 'value': 'Normalised Offensive Score'}
        ],
        value='Normalised Total Score',
        inline=True
    ),
    dcc.Graph(id='triple-type-visualisation')
])

@app.callback(
    [Output('single-type-table', 'data'),
     Output('single-type-table', 'columns')],
    Input('generation-dropdown', 'value')
)
def update_single_type_table(gen):
    mono, _, _ = load_generation_data(gen)
    columns = [{"name": col, "id": col, "deletable": False, "selectable": True} for col in mono.columns]
    return mono.to_dict('records'), columns

@app.callback(
    [Output('dual-type-table', 'data'),
     Output('dual-type-table', 'columns')],
    [Input('generation-dropdown', 'value'),
     Input('dual-type-search', 'value')]
)
def update_dual_type_table(gen, search_query):
    _, dual, _ = load_generation_data(gen)
    if search_query:
        dual = dual[
            dual['First Type'].str.contains(search_query, case=False, na=False) |
            dual['Second Type'].str.contains(search_query, case=False, na=False)
        ]
    columns = [{"name": col, "id": col, "deletable": False, "selectable": True} for col in dual.columns]
    return dual.to_dict('records'), columns

@app.callback(
    [Output('triple-type-table', 'data'),
     Output('triple-type-table', 'columns')],
    [Input('generation-dropdown', 'value'),
     Input('triple-type-search', 'value')]
)
def update_triple_type_table(gen, search_query):
    _, _, triple = load_generation_data(gen)
    if search_query:
        triple = triple[
            triple['First Type'].str.contains(search_query, case=False, na=False) |
            triple['Second Type'].str.contains(search_query, case=False, na=False) |
            triple['Third Type'].str.contains(search_query, case=False, na=False)
        ]
    columns = [{"name": col, "id": col, "deletable": False, "selectable": True} for col in triple.columns]
    return triple.to_dict('records'), columns

@app.callback(
    Output('single-type-visualisation', 'figure'),
    [Input('generation-dropdown', 'value'),
     Input('score-type-radio', 'value')]
)
def update_single_type_graph(gen, selected_score):
    mono, _, _ = load_generation_data(gen)
    if selected_score not in mono.columns:
        return px.bar(title="Invalid Selection", labels={"First Type": "Type"})
    mono['Score Type'] = mono[selected_score].apply(lambda x: 'Positive' if x >= 0.5 else 'Negative')
    return px.bar(
        mono,
        x="First Type",
        y=selected_score,
        color="Score Type",
        title=f"Single-Type Rankings – {gen}",
        labels={"First Type": "Type", selected_score: selected_score}
    ).update_layout(
        xaxis={'categoryorder': 'total ascending'},
        yaxis=dict(range=[0, 1.2]),
        bargap=0.2
    )

@app.callback(
    Output('dual-type-visualisation', 'figure'),
    [Input('generation-dropdown', 'value'),
     Input('dual-score-type-radio', 'value')]
)
def update_dual_type_graph(gen, selected_score):
    _, dual, _ = load_generation_data(gen)
    if selected_score not in dual.columns:
        return px.bar(title="Invalid Selection", labels={"Combined Type": "Type Combination"})
    dual = dual.dropna(subset=[selected_score, "Combined Type"])
    if dual.empty:
        return px.bar(title="No Data Available", labels={"Combined Type": "Type Combination"})
    dual['Score Type'] = dual[selected_score].apply(lambda x: 'Positive' if x >= 0.5 else 'Negative')
    return px.bar(
        dual,
        x="Combined Type",
        y=selected_score,
        color="Score Type",
        title=f"Dual-Type Rankings – {gen}",
        labels={"Combined Type": "Type Combination", selected_score: selected_score}
    ).update_layout(
        xaxis={'categoryorder': 'total ascending'},
        yaxis=dict(range=[0, 1.2]),
        bargap=0.2
    )

@app.callback(
    Output('triple-type-visualisation', 'figure'),
    [Input('generation-dropdown', 'value'),
     Input('triple-score-type-radio', 'value')]
)
def update_triple_type_graph(gen, selected_score):
    _, _, triple = load_generation_data(gen)
    if selected_score not in triple.columns:
        return px.bar(title="Invalid Selection", labels={"Combined Type": "Type Combination"})
    triple = triple.dropna(subset=[selected_score, "Combined Type"])
    if triple.empty:
        return px.bar(title="No Data Available", labels={"Combined Type": "Type Combination"})
    triple['Score Type'] = triple[selected_score].apply(lambda x: 'Positive' if x >= 0.5 else 'Negative')
    return px.bar(
        triple,
        x="Combined Type",
        y=selected_score,
        color="Score Type",
        title=f"Triple-Type Rankings – {gen}",
        labels={"Combined Type": "Type Combination", selected_score: selected_score}
    ).update_layout(
        xaxis={'categoryorder': 'total ascending'},
        yaxis=dict(range=[0, 1.2]),
        bargap=0.2
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    print(f"Running on port {port}")
    app.run_server(host="0.0.0.0", port=port, debug=True)
