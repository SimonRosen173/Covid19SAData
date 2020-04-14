# This file is used to convert markdown 'template' file to markdown file that will be rendered into html by Jekyll
# Replaces variables in template that are in the syntax {#...#} with their corresponding variable as specified by
# dictionary.
# E.g. using dict = {"var1":"hello", "var2":"world"}. Then "This is {#var1#} {#var2#}" becomes "This is hello world"

import re


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


template_name = "index_template.md"
output_name = "index.md"  # Outputted file

import pandas as pd
import numpy as np

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
