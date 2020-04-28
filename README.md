# Covid19 SA Data
Website to show data visualisations pertaining to current coronavirus outbreak in South Africa.
___

**Note: I manually recreate the graphs and ensure the data is correct, thus the website may take a bit of time to update after data is officially released.**

# Parts of Repo
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
    - Note that this folder does not contain all the updates.
  - data_from_img.py
    - Python code to use computer vision along with the associated preprocessing ([pytesseract](https://github.com/madmaze/pytesseract) & OpenCV) to automatically get data from the NICD twitter update infographics.
    - This is an overengineered solution to a simple problem (getting latest data) that is not 100% accurate in its output. None the less it is a fun and informative intro to computer vision for a real world scenario.
    
# Upcomming Features
## Backend
  - Consolidate Jupyter notebooks code from preprocessing data and visualisations into single callable Pythpn file.
    - Will make updating data on site much easier and could potentially be triggered by updates to the [DSFSI research group repo](https://github.com/dsfsi/covid19za).

## Misc
  - Jupyter notebook to show process of preprocessing image and extracting text data from NICD infographics.
    
## Front End 
### Site Layout
- Split site into multiple pages for better usability and smaller download sizes. I.e. page for provinces and then a page for each province.
- Data per district for each province. This will first be Gauteng, then Western Cape, then Kwa-Zulu Natal and from there it is undecided.
### Graphs/Charts
- Make better use of hide trace functionality of Plotly.
  - I.e. instead of seperate graphs for tests and confirmed over time use a single graph containing both and stress the use of clicking on the legend to hide the ones you don't wish to see. 
- Add active cases to confirmed cases and tests graphs.
- Deaths per province over time graph.
- Recoveries per province pie chart.
- Replace totals per province charts with choropleth maps. (Potentially)

# Acknowledgements
## Libraries Used
 - [lazyload by Verlok](https://github.com/verlok/lazyload)
    - Lazy loading of images
 - [spam-referrals-blocker by MohamedBassem](https://github.com/MohamedBassem/spam-referrals-blocker)
    - Exclude known bots from Google Analytics
 - [plotly.py by plotly](https://github.com/plotly/plotly.py)
    - Graphing library used
 - [pytesseract](https://github.com/madmaze/pytesseract)
    - Python wrapper for Tesseract. Uses deep learning to extract text from an image.
## Data
Original data taken from the following sources:
 - DSFSI research group at the University of Pretoria's repository at [Coronavirus COVID-19 (2019-nCoV) Data Repository for South Africa](https://github.com/dsfsi/covid19za).
 - [NICD Twitter](https://twitter.com/nicd_sa)
 - [COVID-19 Corona Virus South African Resource Portal](https://sacoronavirus.co.za/)


## License
Data [![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
