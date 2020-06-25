# This file is used to convert markdown 'template' file to markdown file that will be rendered into html by Jekyll
# Replaces variables in template that are in the syntax {#...#} with their corresponding variable as specified by
# dictionary.
# E.g. using dict = {"var1":"hello", "var2":"world"}. Then "This is {#var1#} {#var2#}" becomes "This is hello world"

import re
import pandas as pd


def render_template(in_file_name, out_file_name, var_dict):
    var_dict = dict(("{{#{}#}}".format(k),str(v)) for k,v in var_dict.items())

    regex_pattern = re.compile(r'(' + '|'.join(re.escape(key) for key in var_dict.keys()) + r')')

    result = ""
    f_out = open(out_file_name, "w", encoding='utf8')
    with open(in_file_name, encoding='utf8') as f_in:
        for line in f_in:
            f_out.write(regex_pattern.sub(lambda x: (var_dict[x.group()]), line))
            # result += regex_pattern.sub(lambda x: (form_dict[x.group()]), line)
    f_out.close()


def df_to_html(df):
    url_map = {}
    html_text = "<table>\n"
    #  Headings
    # ----------
    html_text += "<thead>\n\t<tr class=\"header\">\n"
    # Each Column
    html_text += "\t\t<th>" + df.index.name + "</th>\n"  # index name
    for col in df.columns:
        html_text += "\t\t<th>"+col+"</th>\n"
        # print(col)

    html_text += "\n\t</tr>\n</thead>\n"

    #  Body
    # ------
    html_text += "<tbody>\n"
    no_rows = df.shape[0]
    no_cols = df.shape[1]
    for j in range(no_rows):
        html_text += "\t<tr>\n"

        index_str = ""
        if df.index[j] in url_map:
            url_str = url_map[df.index[j]]
            index_str = "[" + str(df.index[j]) + "](" + url_str + ")"
        else:
            index_str = str(df.index[j])

        class_text = "index"
        is_total_row = False
        if str(df.index[j]).lower() == "total":
            class_text += " total"
            is_total_row = True

        html_text += "\t\t<td class=\""+class_text+"\" markdown=\"span\">" + index_str + "</td>\n"
        # html_text += "\t\t<td class=\"index\"><p>" + index_str + "</p></td>\n"

        class_text = ""
        if is_total_row:
            class_text = "class=\"total\""
        for i in range(no_cols):
            html_text += "\t\t<td " + class_text + " markdown=\"span\">"+str(df.iloc[j,i])+"</td>\n"

        html_text += "\t</tr>\n"

    # print(no_rows, no_cols)
    html_text += "</tbody>\n"

    html_text += "</table>"
    return html_text


def render_index():
    template_name = "index_template.md"
    output_name = "index.md"  # Outputted file

    gen_data = pd.read_csv('data/gen_data.csv')
    tot_infected = gen_data.iloc[0]['tot_infected']
    change_infected = gen_data.iloc[0]['change_infected']

    tot_tested = gen_data.iloc[0]['tot_tested']
    change_tested = gen_data.iloc[0]['change_tested']

    tot_deaths = gen_data.iloc[0]['tot_deaths']
    change_deaths = gen_data.iloc[0]['change_deaths']

    tot_recoveries = gen_data.iloc[0]['tot_recoveries']
    change_recoveries = gen_data.iloc[0]['change_recoveries']

    datetime_updated = gen_data.tail(1).iloc[0]['datetime_updated']

    varDict = dict(tot_infected=tot_infected, change_infected=change_infected, tot_deaths=tot_deaths,
                   tot_tested=tot_tested, change_tested=change_tested, change_deaths=change_deaths,
                   tot_recoveries=tot_recoveries, change_recoveries=change_recoveries,
                   datetime_updated=datetime_updated)

    # print(varDict)
    render_template(template_name, output_name, varDict)
    print("Index Template Rendered - " + datetime_updated + "\n")


def render_provinces():
    template_name = "provinces_template.md"
    output_name = "provinces.md"  # Outputted file

    def zero_space(num):
        return format(num, ',d').replace(",", " ")

    def num_to_plus_minus_str(num):
        if num >= 0:
            num = zero_space(num)
            num = "+" + num
        else:
            num = zero_space(num)
        return num

    prov_summary_df = pd.read_csv("data/prov_summary.csv", index_col='Province',)

    prov_summary_df['New Cases'] = prov_summary_df['New Cases'].apply(num_to_plus_minus_str)
    prov_summary_df['New Recoveries'] = prov_summary_df['New Recoveries'].apply(num_to_plus_minus_str)
    prov_summary_df['New Deaths'] = prov_summary_df['New Deaths'].apply(num_to_plus_minus_str)

    prov_summary_df['Cases'] = prov_summary_df['Cases'].apply(zero_space)
    prov_summary_df['Recoveries'] = prov_summary_df['Recoveries'].apply(zero_space)
    prov_summary_df['Deaths'] = prov_summary_df['Deaths'].apply(zero_space)

    # print(prov_summary_df)
    prov_summary_tbl = df_to_html(prov_summary_df)

    gen_data = pd.read_csv('data/gen_data.csv')
    datetime_updated = gen_data.tail(1).iloc[0]['datetime_updated']

    var_dict = {"datetime_updated":datetime_updated, "prov_summary_tbl":prov_summary_tbl}

    render_template(template_name, output_name, var_dict)

    print("Provinces Template Rendered\n")


def render_all():
    render_index()
    render_provinces()


# render_provinces()
render_all()
