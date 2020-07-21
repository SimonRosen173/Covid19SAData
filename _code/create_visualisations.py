import pandas as pd
import requests
import io
import plotly.express as px
import plotly.offline


def create_pie_chart(df, values, names, save_file_name="", color_discrete_sequence=[]):
    if color_discrete_sequence == []:
        fig = px.pie(df, values=values, names=names)
    else:
        fig = px.pie(df, values=values, names=names, color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(
        legend=dict(x=0, y=1),
        showlegend=False,
        margin=dict(
            t=0,  # 50
            b=20,
            l=0,
            r=0,
        ),
    )
    fig.update_traces(hoverinfo='label+percent',
                      hovertemplate='%{label}<br>%{value}',
                      textinfo='value+label',
                      textposition='inside')

    if save_file_name != "":
        plotly.offline.plot(fig, filename=save_file_name, auto_open=False,
                            config=dict(displayModeBar=False))

    return fig


def create_line_graph(data,  # Dataframe
                      xaxis_title, yaxis_title,  # Strings
                      x_col,  # string denoting column in dataframe for x axis
                      y_cols,  # list of strings denoting column in dataframe for y values for each curve
                      names,  # list of strings - names of each curve
                      colors,  # list of strings - color of each curve
                      annotations=[],
                      start_x="",
                      date_format='%Y-%m-%d',
                      html_file_name="",
                      ):

    data = data.copy()

    if start_x != "":
        start_index = data.loc[data[x_col] == start_x, x_col].index[0]
        data.drop(data.index[:start_index], inplace=True)
    #         data = data.iloc[start_index:]

    if x_col == "date":
        data['date'] = pd.to_datetime(data['date'], format=date_format)

    data_long = pd.melt(data, id_vars=[x_col], value_vars=y_cols)
    fig = px.line(data_long, x='date', y='value', color='variable', color_discrete_sequence=colors)

    fig.update_layout(
        annotations=annotations,
        title="",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        hovermode='x',
        legend=dict(x=0.01, y=.98, title=dict(text="")),
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        margin=dict(
            t=0,
            b=0,
            l=0,
            r=0,
        ),
    )

    fig.update_traces(mode='lines')

    for i in range(0, len(y_cols)):
        fig.data[i].name = names[i]

        fig.data[i].hovertemplate = '%{y}'
        fig.data[i].hoverlabel.namelength = 0

    if html_file_name != "":
        plotly.offline.plot(fig, filename=html_file_name, auto_open=False,
                            config=dict(displayModeBar=False))

    return fig


def create_line_graph_group(data,  # Dataframe
                            xaxis_title, yaxis_title,  # Strings
                            x_col,  # string denoting column in dataframe for x axis
                            y_col,  # strings denoting column in dataframe for y value of each group
                            group_col,
                            is_y_percentage=False,
                            date_format='%Y-%m-%d',
                            html_file_name=""
                            ):
    if x_col == "date":
        data['date'] = pd.to_datetime(data['date'], format=date_format)

    fig = px.line(data, x=x_col, y=y_col, color=group_col,
                  hover_data=[group_col])
    fig.update_layout(
        title="",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        hovermode='x',
        legend=dict(x=0.01, y=.98, title=dict(text="")),
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        margin=dict(
            t=0,
            b=0,
            l=0,
            r=0,
        ),
    )

    for d in fig.data:
        d.hoverinfo = 'all'
        template_str = '%{customdata[0]}<br>%{y}'
        if is_y_percentage:
            template_str += "%"
        d.hovertemplate = template_str
        d.hoverlabel.namelength = 0

    if html_file_name != "":
        plotly.offline.plot(fig, filename=html_file_name, auto_open=False,
                            config=dict(displayModeBar=False))

    return fig


# -------------------------
# - CREATE VISUALISATIONS -
# -------------------------

# SOUTH AFRICA
def create_sa_vis():
    print("Create SA visualisations started")
    # --------------
    #   SUMMARIES
    # --------------
    #  * Pie Charts

    #  Deaths Vs Recoveries
    # ----------------------
    def get_recovered_deaths_totals():
        recovered_deaths_totals = pd.read_csv('data/gen_data.csv',
                                              usecols=['tot_recoveries', 'tot_deaths']).reset_index()
        recovered_deaths_totals.rename({"tot_recoveries": "Recoveries", "tot_deaths": "Deaths"}, axis=1, inplace=True)
        recovered_deaths_totals = recovered_deaths_totals.melt(id_vars=['index'], var_name='variable',
                                                               value_name='total')

        # Below is needed due to integers losing accuracy in division
        recovered_deaths_totals.drop('index', axis=1, inplace=True)
        recovered_deaths_totals['total'] = recovered_deaths_totals['total'].apply(lambda x: str(x).replace(" ", ""))
        recovered_deaths_totals['total'] = pd.to_numeric(recovered_deaths_totals['total'], downcast='float')
        return recovered_deaths_totals

    recovered_deaths_totals = get_recovered_deaths_totals()
    create_pie_chart(recovered_deaths_totals, 'total', 'variable', 'tot_recovered_deaths.html', ['green', 'black'])

    # --------------
    #    OVER TIME
    # ---------------
    #  - Line Graphs

    #    CUMULATIVE DATA
    # -----------------------
    all_cum_data = pd.read_csv('data/all_cum_data.csv')

    # Tests & Confirmed
    # -----------------
    create_line_graph(all_cum_data, "Date", "Cumulative No",
                      x_col='date', y_cols=['tests', 'confirmed'],
                      names=['Tests', 'Positive Cases'], colors=['blue', 'firebrick'],
                      html_file_name="date_vs_cases_tests.html"
                      )
    # Confirmed
    # ---------
    first_day_lockdown_annotations = [dict(
        x=pd.to_datetime('2020-03-27', format='%Y/%m/%d'),
        y=1170,
        xref="x",
        yref="y",
        text="First Day of Lockdown",
        showarrow=True,
        arrowsize=1.5,
        arrowhead=1,
        yshift=4,
        ax=0,
        ay=-40
    )]

    create_line_graph(all_cum_data, "Date", "Cumulative No of Confirmed Cases",
                      x_col='date', y_cols=['confirmed'],
                      names=['Confirmed Cases'], colors=['firebrick'],
                      # annotations=first_day_lockdown_annotations, # Removing temporarily
                      start_x="2020-03-03",
                      html_file_name='date_vs_cases.html'
                      )

    # Recovered & Deaths
    # ------------------
    create_line_graph(all_cum_data, "Date", "Cumulative No",
                      x_col='date', y_cols=['recovered', 'deaths'],
                      names=['Recoveries', 'Deaths'], colors=['green', 'black'],
                      start_x="2020-03-21",
                      html_file_name='cumulative_deaths_recovered.html'
                      )

    # Deaths
    # ------
    create_line_graph(all_cum_data, "Date", "Cumulative No of Deaths",
                      x_col='date', y_cols=['deaths'],
                      names=['Deaths'], colors=['black'],
                      start_x="2020-03-26",
                      html_file_name='cumulative_deaths.html'
                      )

    # Active Cases
    # ------------
    create_line_graph(all_cum_data, "Date", "Active Cases",
                      x_col='date', y_cols=['active'],
                      names=['Active Cases'], colors=['red'],
                      start_x="2020-03-03",
                      html_file_name='date_vs_active.html'
                      )

    # Confirmed Divided By Tests
    # --------------------------
    create_line_graph(all_cum_data, "Date", "Ratio of Confirmed Cases to Tests Conducted",
                      x_col='date', y_cols=['confirmed_div_by_tests'],
                      names=['Confirmed Cases : Tests'], colors=['firebrick'],
                      start_x="2020-03-03",
                      html_file_name="date_vs_confirmed_div_by_tests.html"
                      )

    # Deaths Divided by Confirmed & Recovered Div by Confirmed
    # --------------------------------------------------------
    create_line_graph(all_cum_data, "Date", "Total No",
                      x_col='date', y_cols=['recovered_div_by_confirmed', 'deaths_div_by_confirmed'],
                      names=['Recovered Divided by Confirmed', 'Deaths Divided by Confirmed'],
                      colors=['green', 'black'],
                      start_x="2020-03-21"
                      )

    #     DAILY DATA
    # -----------------------
    all_daily_data = pd.read_csv('data/all_daily_data.csv')

    # Tests & Positive Cases
    # ---------------------
    create_line_graph(all_daily_data, "Date", "Daily Change",
                      x_col='date', y_cols=['tests', 'confirmed'],
                      names=['Tests', 'Confirmed Cases'], colors=['blue', 'firebrick'],
                      html_file_name="date_vs_daily_tests_cases.html"
                      )

    # Positive Cases
    # --------------
    create_line_graph(all_daily_data, "Date", "Daily Change in Confirmed Cases",
                      x_col='date', y_cols=['confirmed'],
                      names=['Confirmed Cases'], colors=['firebrick'],
                      start_x="2020-03-03",
                      html_file_name='date_vs_daily_cases.html'
                      )

    # Deaths & Recoveries
    # -------------------
    create_line_graph(all_daily_data, "Date", "Daily Change",
                      x_col='date', y_cols=['recovered', 'deaths'],
                      names=['Recoveries', 'Deaths'], colors=['green', 'black'],
                      start_x="2020-03-21",
                      html_file_name='daily_deaths_recovered.html'
                      )

    # Deaths
    # ------
    create_line_graph(all_daily_data, "Date", "Daily Change in Deaths",
                      x_col='date', y_cols=['deaths'],
                      names=['Deaths'], colors=['black'],
                      start_x="2020-03-26",
                      html_file_name='daily_deaths.html'
                      )

    print("Create SA visualisations finished")


# -------------
#  BY PROVINCE
# -------------
def create_prov_vis():
    print("Create provincial visualisations started")
    # --------------
    #   SUMMARIES
    # --------------
    #  * Pie Charts

    # Recoveries per province
    # -----------------------
    prov_recov_totals = pd.read_csv('data/tot_recovered_provinces.csv')
    # Totals
    create_pie_chart(prov_recov_totals, 'total', 'province', 'provinces/tot_recovered_per_province.html')
    # Latest Change

    # Confirmed Per Province
    # ----------------------
    prov_totals_data = pd.read_csv('data/tot_provinces.csv')
    # Totals
    create_pie_chart(prov_totals_data, 'total', 'province', 'provinces/tot_cases_per_province.html')
    # Latest Change
    create_pie_chart(prov_totals_data, 'latest_change', 'province', 'provinces/latest_change_cases_per_province.html')

    # Deaths Per Province
    # -------------------
    prov_deaths_totals_data = pd.read_csv('data/tot_deaths_provinces.csv')
    # Totals
    create_pie_chart(prov_deaths_totals_data, 'total', 'province', 'provinces/tot_deaths_per_province.html')
    # Latest Change
    create_pie_chart(prov_deaths_totals_data, 'latest_change', 'province',
                     'provinces/latest_change_deaths_per_province.html')

    # Tests Per Province
    # ------------------
    prov_tests_totals_data = pd.read_csv('data/tot_tests_provinces.csv')
    # Totals
    create_pie_chart(prov_tests_totals_data, 'total', 'province', 'provinces/tot_tests_per_province.html')

    # -------------------------
    #  LINE GRAPHS BY PROVINCE
    # -------------------------

    # Confirmed
    # ---------
    confirmed_by_prov_timeline = pd.read_csv("data/confirmed_by_prov_timeline.csv")
    # Total
    create_line_graph_group(confirmed_by_prov_timeline, "Date", "Total Confirmed Cases",
                            x_col='date', y_col='cum_no', group_col='province',
                            html_file_name="provinces/date_vs_cases_per_province.html")
    # Total As Percentage Of Population
    create_line_graph_group(confirmed_by_prov_timeline, "Date", "Total as Percentage of Population",
                            x_col='date', y_col='cum_no_perc_pop', group_col='province', is_y_percentage=True,
                            html_file_name="provinces/date_vs_cases_perc_pop_per_province.html")
    # Daily Change
    create_line_graph_group(confirmed_by_prov_timeline, "Date", "Daily Change in Confirmed Cases",
                            x_col='date', y_col='daily_no', group_col='province',
                            html_file_name="provinces/date_vs_daily_cases_per_province.html")

    # Deaths
    # ------
    deaths_by_prov_timeline = pd.read_csv("data/deaths_by_prov_timeline.csv")
    # Total
    create_line_graph_group(deaths_by_prov_timeline, "Date", "Total Deaths",
                            x_col='date', y_col='cum_no', group_col='province',
                            html_file_name='provinces/date_vs_deaths_per_province.html')
    # Total As Percentage Of Population
    create_line_graph_group(deaths_by_prov_timeline, "Date", "Total as Percentage of Population",
                            x_col='date', y_col='cum_no_perc_pop', group_col='province', is_y_percentage=True,
                            html_file_name='provinces/date_vs_deaths_perc_pop_per_province.html')
    # Daily Change
    create_line_graph_group(deaths_by_prov_timeline, "Date", "Daily Change in Deaths",
                            x_col='date', y_col='daily_no', group_col='province',
                            html_file_name="provinces/date_vs_daily_deaths_per_province.html")

    # Recoveries
    # ----------
    recoveries_by_prov_timeline = pd.read_csv("data/recoveries_by_prov_timeline.csv")
    # Total
    create_line_graph_group(recoveries_by_prov_timeline, "Date", "Total Recoveries",
                            x_col='date', y_col='cum_no', group_col='province',
                            html_file_name='provinces/date_vs_recoveries_per_province.html')
    # Total As Percentage Of Population
    create_line_graph_group(recoveries_by_prov_timeline, "Date", "Total as Percentage of Population",
                            x_col='date', y_col='cum_no_perc_pop', group_col='province', is_y_percentage=True,
                            html_file_name="provinces/date_vs_recoveries_perc_pop_per_province.html")
    # Daily Change
    create_line_graph_group(recoveries_by_prov_timeline, "Date", "Daily Change in Recoveries",
                            x_col='date', y_col='daily_no', group_col='province',
                            html_file_name="provinces/date_vs_daily_recoveries_per_province.html")

    print("Create provincial visualisations finished")


# -------------
#    GAUTENG
#  BY DISTRICT
# -------------
def create_gp_vis():
    print("Create Gauteng visualisations started")
    # --------------
    #   SUMMARIES
    # --------------
    #  * Pie Charts

    # Confirmed Per District
    # ----------------------
    gp_tot_latest_data = pd.read_csv('data/gp_tot_latest.csv')
    # Totals
    create_pie_chart(gp_tot_latest_data, 'total', 'district', 'provinces/gauteng/tot_cases_per_district_gp.html')
    # Latest Change
    create_pie_chart(gp_tot_latest_data, 'latest_change', 'district', 'provinces/gauteng/latest_change_cases_per_district_gp.html')

    # -------------------------
    #  LINE GRAPHS BY DISTRICT
    # -------------------------

    # Confirmed
    # ---------
    confirmed_by_dist_gp_timeline = pd.read_csv("data/confirmed_by_dist_gp_timeline.csv")
    # Total
    create_line_graph_group(confirmed_by_dist_gp_timeline, "Date", "Total Confirmed Cases",
                            x_col='date', y_col='cum_no', group_col='district',
                            html_file_name="provinces/gauteng/date_vs_cases_per_district_gp.html")
    # Daily Change
    create_line_graph_group(confirmed_by_dist_gp_timeline, "Date", "Total Confirmed Cases",
                            x_col='date', y_col='daily_no', group_col='district',
                            html_file_name="provinces/gauteng/date_vs_daily_cases_per_district_gp.html")

    print("Create Gauteng visualisations finished")


def create_all():
    print("-----------------------------")
    print("Create Visualisations started")
    create_sa_vis()
    create_prov_vis()
    create_gp_vis()
    # GP by District

    print("Create Visualisations finished")