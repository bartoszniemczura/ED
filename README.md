Scripts for Data Mining course at AGH-UST Kraków

##Requirements

Python 2.6+, preferably 3+
 
For database:

 * [pymysql library](https://github.com/PyMySQL/PyMySQL/)

  `pip install PyMySQL`
 
 * [MySQL](http://www.mysql.com/) driver needed to be installed 

##Usage
 
###Crawler

Crawler consists of two files: 
 
* `ted_api.py` - file where you need to provide you API key for TED developer website and which is used to call the ordinary TED service,
* `get_comments.py` - used for crawling user comments throughout TED subpages (it uses `ted_api.py` as dependency).

All crawled data is saved in JSON format for later analysis or loading to database.

###Loader

Again two files:

* `load_comments.py` - user for loading comments into database,
* `load_talks.py` - user for loading everything else (specified by giving proper argument: talks, ratings, themes, tags or speakers).

And a utility file containing multiple SQL commands `sql_commands.py`. You need to provide the database user, password and name inside the scripts. By default the scripts will try to contact the database at localhost on port 10888. The JSON file related to the data being loaded has to exist prior to using the script.

###Analysis
Some utility scripts are provided for extracting data from database and preparing it for further analysis (mainly graph analysis).

* The `select_gephi.py` script has lots of methods (names of them are quite descriptive), which uses provided SQL commands to fetch data and then gives a nicely formatted __.csv__ files, which can be loaded to Gephi (or easily changed in order to fit other programs).
* The `research_user_modularity.py` - script takes a __.csv__ file containing ThemeID,ThemeName and files containing users modules (exported from Gephi) based on themes of talks commented by users. It counts the existence of each theme inside the module and outputs `user_modularity_<YEAR>.csv` file containing histogram of talk themes for each module (per year).