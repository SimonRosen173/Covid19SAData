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

varDict = dict(tot_infected="709", change_infected="155",
               tot_tested="15 529", change_tested="0",
               datetime_updated="20:00 25 March 2020")

render_template(template_name, output_name, varDict)
