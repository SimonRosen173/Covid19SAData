---
layout: default
title: Covid-19 SA Data
description: South African Covid-19 data & visualisations. <br>Contains data for confirmed cases, tests, recoveries, deaths & active cases.
author: Simon Rosen
last_updated: {#datetime_updated#}
---
<center><a href="/provinces" class="btn alt_btn_col">Data Per Province Page</a></center> 
Click the above button to be taken to a page showing Covid19 data per province. 

___

<br>
**Please note that some interactive graphs take a bit of time to load, thank you for your patience.** 

These charts are all interactive. Mouse over an aspect of the chart to see more info, or if you are on mobile tap.
# Total Cases & Tests
**{#tot_infected#} Cases (+{#change_infected#} change) | {#tot_tested#} Tested (+{#change_tested#} change)**
<br><br>

___

<br>

<!--### Total Cases Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_cases_per_province.html" frameborder="0"></iframe>
</div>-->

# Total Deaths & Recoveries
**{#tot_deaths#} Deaths (+{#change_deaths#} change) | {#tot_recoveries#} Recoveries (+{#change_recoveries#} change)** 
<br><br>

___

### Total Deaths & Recoveries
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_recovered_deaths.html" scrolling="no" frameborder="0"></iframe>
</div>

<!--### Total Deaths Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_deaths_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Total Recoveries Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_recovered_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>-->

# Testing & Cases Over Time
___
## Cumulative
### Date vs Cumulative No of Tests & Positive Cases 
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_cases_tests.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs Cumulative No of Positive Cases
<!--Note: You can hide/show the predicted curve by clicking on it in the legend. The graph will be rescaled accordingly. -->
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_cases.html" scrolling="no" frameborder="0"></iframe>
</div>
[What “flattening the curve” means and why it’s so important.](https://sacoronavirus.co.za/2020/03/22/what-flattening-the-curve-means-and-why-its-so-important/) - COVID-19 Corona Virus South African Resource Portal

### Date vs Cumulative No of Active Cases
Active cases are cases where there has not yet been an outcome. I.e. confirmed cases - recoveries - deaths.
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_active.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs Ratio of Positive Cases To Test Conducted
i.e. positive cases divided by tests conducted. 
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_confirmed_div_by_tests.html" scrolling="no" frameborder="0"></iframe>
</div>

<!--### Date vs Cumulative No of Positive Cases Per Province
Note: You can click on provinces in the legend to hide or show them on the graph.
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_cases_per_province.html" frameborder="0"></iframe>
</div>
UNK - Unkown-->

## Daily Change
### Date vs Daily Change in Positive Cases & Tests
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_daily_tests_cases.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs Daily Change in Positive Cases
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_daily_cases.html" scrolling="no" frameborder="0"></iframe>
</div>
<!--
### Date vs No of Tests Per Day
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_daily_tests.html" scrolling="no" frameborder="0"></iframe>
</div>
Note, the data contained in this figure was obtained by calculating the difference between the daily 'total tested' statistics released by governement. As such this data may not directly correspond to the amount of tests actually conducted each day.
### Date vs No of Positive Cases Per Day Per Province
Note: You can click on provinces in the legend to hide or show them on the graph.
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_daily_cases_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>
UNK - Unkown -->
<br>

# Recoveries And Deaths Over Time
___
## Cumulative
### Date vs Cumulative No of Recoveries & Deaths
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="cumulative_deaths_recovered.html" scrolling="no" frameborder="0"></iframe>
</div>

<!--
### Date vs Cumulative No of Recoveries
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="cumulative_recovered.html" scrolling="no" frameborder="0"></iframe>
</div>
-->
### Date vs Cumulative No of Deaths
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="cumulative_deaths.html" scrolling="no" frameborder="0"></iframe>
</div>

## Daily Change
### Date vs Daily Change in Recoveries & Deaths
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="daily_deaths_recovered.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs Daily Change in Deaths
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="daily_deaths.html" scrolling="no" frameborder="0"></iframe>
</div>

<!--
<br>
**Data last updated: {#datetime_updated#}**
-->

{% include_relative _includes/footer.md %}