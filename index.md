
<!-- Hopefully should remove issue where on mobile div flashes blue. Maybe? -->
<script type="text/css">
    .iframeDiv {
        user-select: none; /* supported by Chrome and Opera */
       -webkit-user-select: none; /* Safari */
       -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
       -ms-user-select: none; /* Internet Explorer/Edge */
    }
</script>

**Note for mobile users: This site is not supported for mobile mode, please switch to desktop mode.**
For info on how to do this, click [here](https://support.gpsgate.com/hc/en-us/articles/360021934034-Change-to-Desktop-mode-on-your-mobile-browser).

Please note that some interactive graphs take a bit of time to load, thank you for your patience. <br>

# Updates
* South Africa is currently in lockdown. Under the lockdown, South Africans will be required to stay at home from midnight on Thursday 26 March 2020, until midnight on Thursday 16 April 2020. [[Source]](https://www.sanews.gov.za/south-africa/coronavirus-sa-go-lockdown)
<br><br>

These charts are all interactive. Mouse over an aspect of the chart to see more info, or if you are on mobile tap.
# Total Cases 
**1353 Infected (+27 today) | 41072 Tested (+2663 today) | 5 Deaths (+2 today)** 
<br><br>

<!--
"We must outrightly state that these numbers do not indicate a reduction in the number of infections. 
It is merely a reflection of positive results that were received, verified and ready for today’s reporting."  - 28 March 2020 [SA Department of Health Twitter Statement](https://twitter.com/HealthZA/status/1243968569597181957)
-->
___
### Total Cases Per Province
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/tot_cases_per_province.html" frameborder="0" width="100%" height ="400px"></iframe>
</div>

**Charts for total cases per gender, age and transmission type were removed as these numbers are no longer released by government.**

<!--
### Total Cases Per Gender
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/tot_cases_per_gender.html" frameborder="0" width="100%" height ="400px"></iframe>
</div>
Last updated - 19:00 23 March 2020 (New data not released yet by gov.)

### Total Cases Per Transmission Type
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/tot_cases_per_travel.html" frameborder="0" width="100%" height ="400px"></iframe>
</div>
Last updated - 19:00 23 March 2020 (New data not released yet by gov.)

### Total Cases Per Age Group
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/tot_cases_per_age.html" frameborder="0" width="100%" height ="400px"></iframe>
</div>
Last updated - 19:00 23 March 2020 (New data not released yet by gov.)
-->

# Testing & Cases Over Time
___
## Cumulative
### Date vs Cumulative No of Tests & Positive Cases 
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/date_vs_cases_tests.html" frameborder="0" width="100%" height ="450px"></iframe>
</div>

### Date vs Cumulative No of Positive Cases
Note: You can hide/show the predicted curve by clicking on it in the legend. 
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/date_vs_cases.html" frameborder="0" width="100%" height ="450px"></iframe>
</div>
[What “flattening the curve” means and why it’s so important.](https://sacoronavirus.co.za/2020/03/22/what-flattening-the-curve-means-and-why-its-so-important/) - COVID-19 Corona Virus South African Resource Portal

### Date vs Cumulative No of Positive Cases Per Province
Note: You can click on provinces in the legend to hide or show them on the graph.
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/date_vs_cases_per_province.html" frameborder="0" width="100%" height ="450px"></iframe>
</div>

## Daily
### Date vs No of Positive Cases Per Day
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/date_vs_daily_cases.html" frameborder="0" width="100%" height ="450px"></iframe>
</div>

### Date vs No of Tests Per Day
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/date_vs_daily_tests.html" frameborder="0" width="100%" height ="450px"></iframe>
</div>
Note, the data contained in this figure was obtained by calculating the difference between the daily 'total tested' statistics released by governement. As such this data may not directly correspond to the amount of tests actually conducted each day. 

### Date vs No of Positive Cases & Tests Per Day
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/date_vs_daily_tests_cases.html" frameborder="0" width="100%" height ="450px"></iframe>
</div>

### Date vs No of Positive Cases Per Day Per Province
<div class="iframeDiv" align="center">
    <iframe src="https://simonrosen173.github.io/Covid19SAData/date_vs_daily_cases_per_province.html" frameborder="0" width="100%" height ="450px"></iframe>
</div>
<br><br>

**Data last updated: 14:52 31 March 2020**

# Upcoming Features
* Graphs for recovered, in hospital, critical and deaths.

# Further Info
### N.B. Contact Info
* SA DoH's Covid-19 Emergency Hotline: [0800 029 999](tel:0800 029 999)
* SA DoH's Covid-19 WhatsApp Support Line: [0600-123456](tel:0600-123456)

### Resources
Make sure to keep up to date using the following sources:
* [COVID-19 Corona Virus South African Resource Portal](https://sacoronavirus.co.za/)
* [National Institute for Communicable Diseases Website](http://www.nicd.ac.za/)
* [South African Government News Agency Website](https://www.sanews.gov.za/)

# References
### Data
* [Coronavirus COVID-19 (2019-nCoV) Data Repository for South Africa](https://github.com/dsfsi/covid19za) - 
Data Science for Social Impact Research Group at the University of Pretoria
* [COVID-19 Corona Virus South African Resource Portal](https://sacoronavirus.co.za/)
* [NICD Twitter](https://twitter.com/nicd_sa?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor)
* [South African Government News Agency Website](https://www.sanews.gov.za/)

<br>
Note: Data will only be updated after being officially released by government. This is to avoid using incorrect data.
<br>

If you encounter incorrect data on this site please report it via this email: [simonrosen173@gmail.com](mailto:simonrosen173@gmail.com)