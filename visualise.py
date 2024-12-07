import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from sklearn.preprocessing import MinMaxScaler

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the data using paths relative to the script's directory
type_values_path = os.path.join(script_dir, "monotype_combinations.csv")
dual_type_values_path = os.path.join(script_dir, "dualtype_combinations.csv")
triple_type_values_path = os.path.join(script_dir, "tripletype_combinations.csv")

# Verify file existence (optional but recommended for debugging)
assert os.path.exists(type_values_path), f"File not found: {type_values_path}"
assert os.path.exists(dual_type_values_path), f"File not found: {dual_type_values_path}"
assert os.path.exists(triple_type_values_path), f"File not found: {triple_type_values_path}"

# Read CSV files
type_values_df = pd.read_csv(type_values_path)
dual_type_values_df = pd.read_csv(dual_type_values_path)
triple_type_values_df = pd.read_csv(triple_type_values_path)

# Combine types for display purposes only
def combine_types(row, type_columns):
    return '/'.join(str(row[col]) for col in type_columns if pd.notna(row[col]))

dual_type_values_df_display = dual_type_values_df.copy()
dual_type_values_df_display['Combined Type'] = dual_type_values_df.apply(combine_types, axis=1, type_columns=["First Type", "Second Type"])

triple_type_values_df_display = triple_type_values_df.copy()
triple_type_values_df_display['Combined Type'] = triple_type_values_df.apply(combine_types, axis=1, type_columns=["First Type", "Second Type", "Third Type"])

# Sort dataframes by Total Score
type_values_df = type_values_df.sort_values(by="Total Score", ascending=True)
dual_type_values_df_display = dual_type_values_df_display.sort_values(by="Total Score", ascending=True)
triple_type_values_df_display = triple_type_values_df_display.sort_values(by="Total Score", ascending=True)

# Normalise the Total Score, Defensive Score, and Offensive Score columns for visualisation
scaler = MinMaxScaler()
for column in ["Total Score", "Defensive Score", "Offensive Score"]:
    type_values_df[f"Normalised {column}"] = scaler.fit_transform(type_values_df[[column]])
    dual_type_values_df_display[f"Normalised {column}"] = scaler.fit_transform(dual_type_values_df_display[[column]])
    triple_type_values_df_display[f"Normalised {column}"] = scaler.fit_transform(triple_type_values_df_display[[column]])

# Initialise the Dash app
app = dash.Dash(__name__)

@app.server.route('/healthz')
def health_check():
    return "OK", 200

app.layout = html.Div([
    html.H1("Pokémon Type Rankings Viewer"),

    html.H2("Monotype Rankings"),
    dash_table.DataTable(
        id='single-type-table',
        columns=[
            {"name": col, "id": col, "deletable": False, "selectable": True} for col in type_values_df.columns
        ],
        data=type_values_df.to_dict('records'),
        sort_action="native",
        page_size=20,
        style_table={'overflowX': 'auto'},
    ),

    html.H2("Dual-Type Rankings"),
    dash_table.DataTable(
        id='dual-type-table',
        columns=[
            {"name": col, "id": col, "deletable": False, "selectable": True} for col in dual_type_values_df_display.columns
        ],
        data=dual_type_values_df_display.to_dict('records'),
        sort_action="native",
        page_size=20,
        style_table={'overflowX': 'auto'},
    ),

    html.H2("Tri-Type Rankings"),
    dash_table.DataTable(
        id='triple-type-table',
        columns=[
            {"name": col, "id": col, "deletable": False, "selectable": True} for col in triple_type_values_df_display.columns
        ],
        data=triple_type_values_df_display.to_dict('records'),
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
    dash.dependencies.Output('single-type-visualisation', 'figure'),
    [dash.dependencies.Input('score-type-radio', 'value')]
)
def update_single_type_graph(selected_score):
    type_values_df['Score Type'] = type_values_df[selected_score].apply(lambda x: 'Positive' if x >= 0.5 else 'Negative')
    return px.bar(
        type_values_df,
        x="First Type",
        y=selected_score,
        color="Score Type",
        title="Single-Type Rankings",
        labels={selected_score: selected_score, "First Type": "Type", "Score Type": "Score Type"}
    ).update_layout(
        xaxis={'categoryorder': 'total ascending'},
        yaxis=dict(range=[0, 1.2]),
        bargap=0.2
    )

@app.callback(
    dash.dependencies.Output('dual-type-visualisation', 'figure'),
    [dash.dependencies.Input('dual-score-type-radio', 'value')]
)
def update_dual_type_graph(selected_score):
    dual_type_values_df_display['Score Type'] = dual_type_values_df_display[selected_score].apply(lambda x: 'Positive' if x >= 0.5 else 'Negative')
    return px.bar(
        dual_type_values_df_display,
        x="Combined Type",
        y=selected_score,
        color="Score Type",
        title="Dual-Type Rankings",
        labels={selected_score: selected_score, "Combined Type": "Type Combination", "Score Type": "Score Type"}
    ).update_layout(
        xaxis={'categoryorder': 'total ascending'},
        yaxis=dict(range=[0, 1.2]),
        bargap=0.2
    )

@app.callback(
    dash.dependencies.Output('triple-type-visualisation', 'figure'),
    [dash.dependencies.Input('triple-score-type-radio', 'value')]
)
def update_triple_type_graph(selected_score):
    triple_type_values_df_display['Score Type'] = triple_type_values_df_display[selected_score].apply(lambda x: 'Positive' if x >= 0.5 else 'Negative')
    return px.bar(
        triple_type_values_df_display,
        x="Combined Type",
        y=selected_score,
        color="Score Type",
        title="Triple-Type Rankings",
        labels={selected_score: selected_score, "Combined Type": "Type Combination", "Score Type": "Score Type"}
    ).update_layout(
        xaxis={'categoryorder': 'total ascending'},
        yaxis=dict(range=[0, 1.2]),
        bargap=0.2
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    print(f"Running on port {port}")
    app.run_server(host="0.0.0.0", port=port, debug=True)
