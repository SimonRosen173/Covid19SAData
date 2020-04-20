# Covid19 SA Data
Website to show data visualisations pertaining to current coronavirus outbreak in South Africa.

**Note: I manually recreate the graphs and ensure the data is correct, thus the website may take a bit of time to update after data is officially released.**

## Parts of Repo
The repo currently consists of the following parts:
  - Jekyll related files to control styling of site.
    - These folders are the ones preceded by '_'
  - Jupyter notebooks to preprocess data, calculate predictions and generate curves
    - Data_Preprocessing.ipynb
    - Predictions.ipynb
    - Visualisations.ipynb
    - Other notebooks are currently not used.
  - Graphs in HTML file form.
  - template_renderer.py
    - Custom template renderer that allows for use of variables in markdown files.
    - Markdwon files followed by '_template' are used by the template_renderer.
  - Markdown files
    - Used as a template by Jekyll to render markdown to html. These are the files that compile to the website page/s.
  - Data folder
    - csv files that are used to generate graphs and data for site.
  - NICD updates
    - NICD daily updates in image form taken from their twitter.
    - Note that this folder is severely outdated.
    
Folders not currently in use:
  - Docs
  - notebooks

## Acknowledgements
### Libraries Used
 - [lazyload by Verlok](https://github.com/verlok/lazyload)
    - Lazy loading of images
 - [spam-referrals-blocker by MohamedBassem](https://github.com/MohamedBassem/spam-referrals-blocker)
    - Exclude known bots from Google Analytics
 - [plotly.py by plotly](https://github.com/plotly/plotly.py)
    - Graphing library used
### Data
Original data taken from the following sources:
 - DSFSI research group at the University of Pretoria's repository at [Coronavirus COVID-19 (2019-nCoV) Data Repository for South Africa](https://github.com/dsfsi/covid19za).
 - [NICD Twitter](https://twitter.com/nicd_sa)
 - [COVID-19 Corona Virus South African Resource Portal](https://sacoronavirus.co.za/)


### License
Data [![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
