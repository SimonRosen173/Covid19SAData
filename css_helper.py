
def insert_css(file_name_in, file_name_out):
    with open(file_name_in, 'r') as file:
        file_data = file.read()

    # Replace the target string
    css_class = "<style>\n .nsewdrag {-webkit-tap-highlight-color: transparent !important;}\n</style>\n</head>"
    file_data = file_data.replace('</head>', css_class)
    # css_tag_old = "cursor-pointer"
    # css_tag_new = "cursor-pointer remove_blue_highlight"
    # file_data = file_data.replace(css_tag_old, css_tag_new)

    # Write the file out again
    with open(file_name_out, 'w') as file:
        file.write(file_data)


file_names = ["cumulative_deaths.html", "cumulative_deaths_recovered.html", "cumulative_recovered.html",
              "date_vs_cases.html", "date_vs_cases_per_province.html", "date_vs_cases_tests.html",
              "date_vs_daily_cases.html", "date_vs_daily_cases_per_province.html", "date_vs_daily_tests.html",
              "date_vs_daily_tests_cases.html"]

for file_name in file_names:
    insert_css(file_name,file_name)

# insert_css("date_vs_daily_tests_cases.html", "date_vs_daily_tests_cases_new.html")