import pandas as pd
import requests
import io
import plotly.express as px
import datetime
import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline
import os
import subprocess

def pre_process_data():
    # get dataframe from specified url using kwargs specified for read_csv
    def df_from_url(df_url, pd_kwargs={}):
        df_req = requests.get(df_url).content
        df = pd.read_csv(io.StringIO(df_req.decode('utf-8')), **pd_kwargs)
        return df

    def get_cum_daily(data_url, cum_col='total', index_col='date'):  # kwargs={}):
        cols = ['date', 'total']
        pd_kwargs = {"usecols": [cum_col, index_col], "index_col": [index_col]}

        data = df_from_url(data_url, pd_kwargs)
        data.reset_index(inplace=True)
        data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')
        data.set_index('date', inplace=True)
        data.rename({cum_col: "cum_no"}, axis=1, inplace=True)
        data.ffill(inplace=True)

        data['daily_no'] = data['cum_no']
        data['daily_no'][1:] = data['cum_no'].diff()[1:]
        # Cast columns to integer
        data = data.astype('int32')
        return data

    confirmed_cases_url = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv"
    confirmed_data = get_cum_daily(confirmed_cases_url)

    deaths_url = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv"
    deaths_data = get_cum_daily(deaths_url)

    tests_url = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_timeline_testing.csv"
    tests_data = get_cum_daily(tests_url, 'cumulative_tests', 'date')

    tests_url = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_timeline_testing.csv"
    recovered_data = get_cum_daily(tests_url, 'recovered', 'date')

    def get_active_cases():
        _active_data = confirmed_data[['cum_no']].copy().rename({"cum_no": "confirmed"}, axis=1)
        _active_data = pd.concat([_active_data,
                                 recovered_data[['cum_no']].copy().rename({"cum_no": "recovered"}, axis=1),
                                 deaths_data[['cum_no']].copy().rename({"cum_no": "deaths"}, axis=1)
                                 ], axis=1)
        _active_data = _active_data.iloc[9:]
        _active_data = _active_data.ffill().fillna(0)

        _active_data['cum_no'] = _active_data['confirmed'] - _active_data['recovered'] - _active_data['deaths']
        _active_data.drop(['confirmed', 'recovered', 'deaths'], axis=1, inplace=True)
        _active_data['daily_no'] = _active_data['cum_no'].copy()
        _active_data['daily_no'].iloc[1:] = _active_data['cum_no'].diff().iloc[1:]
        _active_data = _active_data.astype('int32')

        return _active_data

    active_data = get_active_cases()

    def get_all_cum_data():
        _all_cum_data = confirmed_data[['cum_no']].rename({"cum_no": "confirmed"}, axis=1)
        _all_cum_data = pd.concat([
            _all_cum_data,
            tests_data[['cum_no']].rename({"cum_no": "tests"}, axis=1),
            deaths_data[['cum_no']].rename({"cum_no": "deaths"}, axis=1),
            recovered_data[['cum_no']].rename({"cum_no": "recovered"}, axis=1),
            active_data[['cum_no']].rename({"cum_no": "active"}, axis=1),

        ], axis=1)
        # _all_cum_data['recovered'] = recovered_data['cum_no']
        # _all_cum_data['active'] = active_data['cum_no']
        _all_cum_data.ffill(inplace=True)
        _all_cum_data.fillna(0, inplace=True)
        _all_cum_data = _all_cum_data.astype('int32')

        # DERIVED STATS

        # confirmed_div_by_tests
        _all_cum_data['confirmed_div_by_tests'] = _all_cum_data['confirmed'] / _all_cum_data['tests']
        _all_cum_data['confirmed_div_by_tests'] = _all_cum_data['confirmed_div_by_tests'].round(3)

        # deaths_div_by_confirmed
        _all_cum_data['deaths_div_by_confirmed'] = _all_cum_data['deaths'] / _all_cum_data['confirmed']
        _all_cum_data['deaths_div_by_confirmed'] = _all_cum_data['deaths_div_by_confirmed'].round(3)
        _all_cum_data.fillna(0.000, inplace=True)

        # recovered_div_by_confirmed
        _all_cum_data['recovered_div_by_confirmed'] = _all_cum_data['recovered'] / _all_cum_data['confirmed']
        _all_cum_data['recovered_div_by_confirmed'] = _all_cum_data['recovered_div_by_confirmed'].round(3)
        _all_cum_data.fillna(0.000, inplace=True)

        # STATS PER MILLION POP

        sa_tot_population = 59195720
        # total population rounded in millions
        sa_tot_pop_mil = sa_tot_population / 1000000

        _all_cum_data['confirmed_per_mil'] = _all_cum_data['confirmed'] / sa_tot_pop_mil
        _all_cum_data['tests_per_mil'] = _all_cum_data['tests'] / sa_tot_pop_mil
        _all_cum_data['deaths_per_mil'] = _all_cum_data['deaths'] / sa_tot_pop_mil
        _all_cum_data['recovered_per_mil'] = _all_cum_data['recovered'] / sa_tot_pop_mil
        _all_cum_data['active_per_mil'] = _all_cum_data['active'] / sa_tot_pop_mil
        tmp_cols = ['confirmed_per_mil', 'tests_per_mil', 'deaths_per_mil', 'recovered_per_mil', 'active_per_mil']
        _all_cum_data[tmp_cols] = _all_cum_data[tmp_cols].round(2)
        _all_cum_data.fillna(0.00, inplace=True)

        return _all_cum_data

    # All cumulative data
    all_cum_data = get_all_cum_data()
    all_cum_data.to_csv('data/all_cum_data.csv')

    def get_all_daily_data():
        _all_daily_data = confirmed_data[['daily_no']].rename({"daily_no": "confirmed"}, axis=1)
        _all_daily_data = pd.concat([
            _all_daily_data,
            tests_data[['daily_no']].rename({"daily_no": "tests"}, axis=1),
            deaths_data[['daily_no']].rename({"daily_no": "deaths"}, axis=1),
            recovered_data[['daily_no']].rename({"daily_no": "recovered"}, axis=1),
            active_data[['daily_no']].rename({"daily_no": "active"}, axis=1),

        ], axis=1)
        _all_daily_data.ffill(inplace=True)
        _all_daily_data.fillna(0, inplace=True)
        _all_daily_data = _all_daily_data.astype('int32')
        return _all_daily_data

    # All daily data
    all_daily_data = get_all_daily_data()
    all_daily_data.to_csv("data/all_daily_data.csv")

    # -----------
    # BY PROVINCE
    # -----------

    # Generator method to get all dates in specified interval
    from datetime import timedelta, datetime

    def datetime_range(start_datetime, end_datetime):
        curr_date = start_datetime
        yield curr_date
        while curr_date < end_datetime:
            curr_date += timedelta(days=1)
            yield curr_date

    # round_no - decimals to round to
    def get_cum_daily_by_prov(data_url, fill_date_gaps=False, dropna=True, round_no=3):
        cols = ['date', 'EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']
        pd_kwargs = {"usecols": cols}
        cum_data = df_from_url(data_url, pd_kwargs)

        if dropna:
            cum_data.dropna(inplace=True)

        cum_data['date'] = pd.to_datetime(cum_data['date'], format='%d-%m-%Y')

        if fill_date_gaps:
            start_date = cum_data.iloc[0]['date']
            end_date = cum_data.iloc[-1]['date']
            date_range = list(datetime_range(start_date, end_date))
            cum_data.set_index('date', inplace=True)
            cum_data = cum_data.reindex(date_range)
            cum_data.ffill(inplace=True)
            cum_data.reset_index(inplace=True)

        daily_data = cum_data.copy()
        daily_data.iloc[1:, 1:] = daily_data.iloc[:, 1:].diff().iloc[1:]
        daily_data_melt = daily_data.melt(id_vars=['date'], var_name='province', value_name='daily_no')
        daily_data_melt.set_index(['date'], inplace=True)

        cum_data_melt = cum_data.melt(id_vars=['date'], var_name='province', value_name='cum_no')
        cum_data_melt.set_index(['date'], inplace=True)

        data = pd.concat([cum_data_melt, daily_data_melt[['daily_no']]], axis=1)
        data[['cum_no', 'daily_no']] = data[['cum_no', 'daily_no']].astype('int32')

        prov_pops = {  # https://github.com/dsfsi/covid19za/blob/master/data/district_data/za_province_pop.csv
            "EC": 6712276.0,
            "FS": 2887465.0,
            "GP": 15176115.0,
            "KZN": 11289086.0,
            "LP": 5982584.0,
            "MP": 4592187.0,
            "NW": 4072160.0,
            "NC": 1263875.0,
            "WC": 6844272.0,
            "UNKNOWN": None
        }

        data['cum_no_perc_pop'] = data['province'].map(prov_pops)
        data['cum_no_perc_pop'] = data['cum_no'] / data['cum_no_perc_pop'] * 100
        data['cum_no_perc_pop'] = data['cum_no_perc_pop'].round(round_no)

        data['daily_no_perc_pop'] = data['province'].map(prov_pops)
        data['daily_no_perc_pop'] = data['daily_no'] / data['daily_no_perc_pop'] * 100
        data['daily_no_perc_pop'] = data['daily_no_perc_pop'].round(round_no)

        return data

    # Confirmed
    confirmed_by_prov_timeline = get_cum_daily_by_prov("https://raw.githubusercontent.com/dsfsi/covid19za/master/" +
                                                       "data/covid19za_provincial_cumulative_timeline_confirmed.csv")
    confirmed_by_prov_timeline.to_csv("data/confirmed_by_prov_timeline.csv")

    # Deaths
    deaths_by_prov_timeline = get_cum_daily_by_prov("https://raw.githubusercontent.com/dsfsi/covid19za/master/" +
                                                    "data/covid19za_provincial_cumulative_timeline_deaths.csv",
                                                    round_no=4)
    deaths_by_prov_timeline.to_csv("data/deaths_by_prov_timeline.csv")

    # Recoveries
    recoveries_by_prov_timeline = get_cum_daily_by_prov("https://raw.githubusercontent.com/dsfsi/covid19za/master/" +
                                                        "data/covid19za_provincial_cumulative_timeline_recoveries.csv",
                                                        fill_date_gaps=True)
    recoveries_by_prov_timeline.to_csv("data/recoveries_by_prov_timeline.csv")

    # Total & Latest Change
    def get_tot_latest_change(data_url, fill_date_gaps=False):
        cols = ['date', 'EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW', 'WC', 'UNKNOWN']
        pd_kwargs = {"usecols": cols}
        cum_data = df_from_url(data_url, pd_kwargs)
        cum_data.dropna(inplace=True)  # Rather fillna or ffill - look into
        cum_data['date'] = pd.to_datetime(cum_data['date'], format='%d-%m-%Y')

        if fill_date_gaps:
            start_date = cum_data.iloc[0]['date']
            end_date = cum_data.iloc[-1]['date']
            date_range = list(datetime_range(start_date, end_date))
            cum_data.set_index('date', inplace=True)
            cum_data = cum_data.reindex(date_range)
            cum_data.ffill(inplace=True)
            cum_data.reset_index(inplace=True)

        province_names = {
            "EC": "Eastern Cape",
            "FS": "Free State",
            "GP": "Gauteng",
            "KZN": "KwaZulu-Natal",
            "LP": "Limpopo",
            "MP": "Mpumalanga",
            "NW": "North West",
            "NC": "Northern Cape",
            "WC": "Western Cape",
            "UNKNOWN": "Unknown"
        }

        daily_data = cum_data.copy()
        daily_data.iloc[1:, 1:] = daily_data.iloc[:, 1:].diff().iloc[1:]
        daily_data = daily_data.tail(1)  # get last entry
        daily_data_melt = daily_data.melt(id_vars=['date'], var_name='province', value_name='latest_change')
        daily_data_melt['province'] = daily_data_melt['province'].map(province_names)
        daily_data_melt.set_index(['province'], inplace=True)

        cum_data = cum_data.tail(1)  # get last entry
        cum_data_melt = cum_data.melt(id_vars=['date'], var_name='province', value_name='total')
        cum_data_melt['province'] = cum_data_melt['province'].map(province_names)
        cum_data_melt.set_index(['province'], inplace=True)

        data = pd.concat([cum_data_melt, daily_data_melt[['latest_change']]], axis=1)
        data.drop(['date'], axis=1, inplace=True)
        data = data.astype('int32')

        return data

    # Total & latest change in deaths by prov
    deaths_by_prov_total = get_tot_latest_change("https://raw.githubusercontent.com/dsfsi/covid19za/master/" +
                                                 "data/covid19za_provincial_cumulative_timeline_deaths.csv")
    deaths_by_prov_total.to_csv('data/tot_deaths_provinces.csv')

    # Total & latest change in confirmed by prov
    confirmed_by_prov_total = get_tot_latest_change("https://raw.githubusercontent.com/dsfsi/covid19za/master/" +
                                                    "data/covid19za_provincial_cumulative_timeline_confirmed.csv")
    confirmed_by_prov_total.to_csv('data/tot_provinces.csv')

    # Total & latest change in recoveries by prov
    recoveries_by_prov_total = get_tot_latest_change("https://raw.githubusercontent.com/dsfsi/covid19za/master/" +
                                                     "data/covid19za_provincial_cumulative_timeline_recoveries.csv")
    recoveries_by_prov_total.to_csv('data/tot_recovered_provinces.csv')

    print("Pre-Processing Done")

    def get_index_page_data():
        def zero_space(num):
            return format(num, ',d').replace(",", " ")

        # Tests
        tot_tested = zero_space(tests_data.tail(1).iloc[0]['cum_no'].astype(int))
        change_tested = zero_space(tests_data.tail(1).iloc[0]['daily_no'].astype(int))

        # Confirmed
        tot_infected = zero_space(confirmed_data.tail(1).iloc[0]['cum_no'].astype(int))
        change_infected = zero_space(confirmed_data.tail(1).iloc[0]['daily_no'].astype(int))

        # Deaths
        tot_deaths = zero_space(deaths_data.tail(1).iloc[0]['cum_no'].astype(int))
        change_deaths = zero_space(deaths_data['daily_no'].tail(1).iloc[0].astype(int))

        # Recoveries
        tot_recoveries = zero_space(recovered_data.tail(1).iloc[0]['cum_no'].astype(int))
        change_recoveries = zero_space(recovered_data.tail(1).iloc[0]['daily_no'].astype(int))

        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M %d %B %Y")

        _gen_data = pd.DataFrame(dict(tot_infected=[tot_infected], change_infected=[change_infected],
                                     tot_deaths=[tot_deaths], change_deaths=[change_deaths],
                                     tot_tested=[tot_tested], change_tested=[change_tested],
                                     tot_recoveries=[tot_recoveries], change_recoveries=[change_recoveries],
                                     datetime_updated=[current_time]))

        return _gen_data

    index_page_data = get_index_page_data()
    index_page_data.to_csv("data/gen_data.csv", index=False)

    # Render templates
    import template_renderer as tr
    tr.render_all()


def create_visualisations():
    print("Create Visualisations started")
    # --------------
    #   SUMMARIES
    # --------------
    #  * Pie Charts

    print("Create pie charts started")

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

    # Recoveries per province
    # -----------------------
    prov_recov_totals = pd.read_csv('data/tot_recovered_provinces.csv')
    # Totals
    create_pie_chart(prov_recov_totals, 'total', 'province', 'tot_recovered_per_province.html')
    # Latest Change

    # Confirmed Per Province
    # ----------------------
    prov_totals_data = pd.read_csv('data/tot_provinces.csv')
    # Totals
    create_pie_chart(prov_totals_data, 'total', 'province', 'tot_cases_per_province.html')
    # Latest Change
    create_pie_chart(prov_totals_data, 'latest_change', 'province', 'latest_change_cases_per_province.html')

    # Deaths Per Province
    # -------------------
    prov_deaths_totals_data = pd.read_csv('data/tot_deaths_provinces.csv')
    # Totals
    create_pie_chart(prov_deaths_totals_data, 'total', 'province', 'tot_deaths_per_province.html')
    # Latest Change
    create_pie_chart(prov_deaths_totals_data, 'latest_change', 'province', 'latest_change_deaths_per_province.html')

    # Tests Per Province
    # ------------------
    prov_tests_totals_data = pd.read_csv('data/tot_tests_provinces.csv')
    # Totals
    create_pie_chart(prov_tests_totals_data, 'total', 'province', 'tot_tests_per_province.html')
    # Latest - TODO

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

    print("Create pie charts finished")
    # --------------
    #    OVER TIME
    # ---------------
    #  - Line Graphs
    print("Create line graphs started")

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
                      annotations=first_day_lockdown_annotations,
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

    print("Create line graphs finished")

    # -------------------------
    #  LINE GRAPHS BY PROVINCE
    # -------------------------
    print("Create line graphs by province started")

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

    # Confirmed
    # ---------
    confirmed_by_prov_timeline = pd.read_csv("data/confirmed_by_prov_timeline.csv")
    # Total
    create_line_graph_group(confirmed_by_prov_timeline, "Date", "Total Confirmed Cases",
                            x_col='date', y_col='cum_no', group_col='province',
                            html_file_name="date_vs_cases_per_province.html")
    # Total As Percentage Of Population
    create_line_graph_group(confirmed_by_prov_timeline, "Date", "Total as Percentage of Population",
                            x_col='date', y_col='cum_no_perc_pop', group_col='province', is_y_percentage=True,
                            html_file_name="date_vs_cases_perc_pop_per_province.html")
    # Daily Change
    create_line_graph_group(confirmed_by_prov_timeline, "Date", "Daily Change in Confirmed Cases",
                            x_col='date', y_col='daily_no', group_col='province',
                            html_file_name="date_vs_daily_cases_per_province.html")

    # Deaths
    # ------
    deaths_by_prov_timeline = pd.read_csv("data/deaths_by_prov_timeline.csv")
    # Total
    create_line_graph_group(deaths_by_prov_timeline, "Date", "Total Deaths",
                            x_col='date', y_col='cum_no', group_col='province',
                            html_file_name='date_vs_deaths_per_province.html')
    # Total As Percentage Of Population
    create_line_graph_group(deaths_by_prov_timeline, "Date", "Total as Percentage of Population",
                            x_col='date', y_col='cum_no_perc_pop', group_col='province', is_y_percentage=True,
                            html_file_name = 'date_vs_deaths_perc_pop_per_province.html')
    # Daily Change
    create_line_graph_group(deaths_by_prov_timeline, "Date", "Daily Change in Deaths",
                            x_col='date', y_col='daily_no', group_col='province',
                            html_file_name="date_vs_daily_deaths_per_province.html")

    # Recoveries
    # ----------
    recoveries_by_prov_timeline = pd.read_csv("data/recoveries_by_prov_timeline.csv")
    # Total
    create_line_graph_group(recoveries_by_prov_timeline, "Date", "Total Recoveries",
                            x_col='date', y_col='cum_no', group_col='province',
                            html_file_name='date_vs_recoveries_per_province.html')
    # Total As Percentage Of Population
    create_line_graph_group(recoveries_by_prov_timeline, "Date", "Total as Percentage of Population",
                            x_col='date', y_col='cum_no_perc_pop', group_col='province', is_y_percentage=True,
                            html_file_name="date_vs_recoveries_perc_pop_per_province.html")
    # Daily Change
    create_line_graph_group(recoveries_by_prov_timeline, "Date", "Daily Change in Recoveries",
                            x_col='date', y_col='daily_no', group_col='province',
                            html_file_name="date_vs_daily_recoveries_per_province.html")

    print("Create line graphs by province finished")
    print("Create Visualisations finished")


input("Press Enter to Quit")