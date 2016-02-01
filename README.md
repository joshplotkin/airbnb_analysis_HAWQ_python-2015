## An analysis of 35k airbnb NYC listings using python connecting to HAWQ+MADlib.

### To simply view, go to the notebook_md file and open the md file.

### This is a demo using python with HAWQ to easily generate and execute queries in parallel.
* python for fast generation of SQL queries
* jupyter notebook and pandas for a better interface for returning results
* HAWQ for a fast MPP engine on top of HDFS
* PL/Python for creating custom functions that the HAWQ engine executes in parallel
* MADlib for in-database machine learning and statistics, in parallel

### The easiest way to use this is by installing anaconda. Anaconda is a package manager for python, found here: https://www.continuum.io/downloads
* if a package isn't found, you can run `conda install <package name>` to install it
* to run the jupyter notebook, first open the terminal (or cmd in windows). navigate to the directory where your ipynb file is located and then type `jupyter notebook`.
* you will need to modify the connection string to connect to your airbnb database

#### TODO:
* several TODOs at bottom of the notebook
* add code for scraping airbnb
