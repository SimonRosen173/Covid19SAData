---
layout: default
title: Covid-19 SA Provincial Data
description: South African Provincial Covid-19 data & visualisations. <br>Contains data for confirmed cases, tests, recoveries and deaths by province.
author: Simon Rosen
last_updated: {#datetime_updated#}
---

<center><a href="/" class="btn alt_btn_col">Home</a></center>

# Summary
___

**Note: Click on an underlined province name to be taken to a page specific to that province.**

{#prov_summary_tbl#}
Negative values in the "New" columns indicate that the total of that value for the specified province went down from the previous
day. This is due to the numbers being adjusted by government and moved to the totals of other provinces or mistakes in the reporting by government.

# Total & Latest Change in Cases

___

### Total Cases Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_cases_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Latest Change in Cases Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="latest_change_cases_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

# Total Tests
___

### Total Tests Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_tests_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>
Tests per province data is for **28 May 2020**. This is when the data was last released.

# Total & Latest Change in Recoveries

___

### Total Recoveries Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_recovered_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>
<!--
### Latest Change in Recoveries Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_recovered_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>
-->

# Total & Latest Change in Deaths & Recoveries
___

### Total Deaths Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="tot_deaths_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Latest Change in Deaths Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy pieChart" data-src="latest_change_deaths_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

# Cases Over Time
___
Note: You can click on provinces in the legend to hide or show them on the graph.
### Date vs No of Positive Cases Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_cases_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs Daily Change of Positive Cases Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_daily_cases_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs No of Positive Cases Per Province As Percent of Province's Population
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_cases_perc_pop_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>
**Populations per province are shown the bottom of this page**

# Recoveries Over Time
___
### Date vs No of Recoveries Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_recoveries_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs Daily Change of Recoveries Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_daily_recoveries_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs No of Recoveries Per Province As Percent of Province's Population
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_recoveries_perc_pop_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>
**Populations per province are shown at the bottom of this page**

# Deaths Over Time
___
### Date vs No of Deaths Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_deaths_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs Daily Change of Deaths Per Province
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_daily_deaths_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

### Date vs No of Deaths Per Province As Percent of Province's Population
<div class="iframeDiv" align="center">
    <iframe class="lazy" data-src="date_vs_deaths_perc_pop_per_province.html" scrolling="no" frameborder="0"></iframe>
</div>

## Population Per Province

___

{#prov_pop_tbl#}

{% include_relative _includes/footer.md %}

