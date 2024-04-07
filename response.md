**Pseudocode:**

```plaintext
File Structure:
- .gitignore
- GUI.py
- README.md
- csv_code.py
- download_XLS.py
- mysql_code.py
- plots.py
- requirements.txt

Variables:
- pressed5: boolean
- pressed6: boolean
- year: integer
- months: array of strings
- header: array of strings
- current_directory: string
- csv_directory: string
- links: array of strings
- filname: string
- conn: database connection
- c: cursor object
- tables_atrr: string
- sql: string
- val: tuple
- record: array
- table: array
- current_book: string
- workbook: Excel workbook object
- current_worksheet: Excel worksheet object
- total_rows: integer
- total_cols: integer
- match: regex match object
- match_stop: regex match object
- country: string
- temp: integer
- i, x, y: integers
- dict_all_years: dictionary
- dict_each_year: array of dictionaries
- sorted_all_years: array of tuples
- sorted_for_each_year: array of arrays of tuples
- countries_names_each: array of arrays of strings
- countries_total_each: array of arrays of integers
- countries_names_all: array of strings
- countries_total_all: array of integers
- quarter_sum: integer
- current_quarter: integer
- all_years_quarters: array of arrays of integers
- xpos: array of integers

Dependencies:
- tkinter
- messagebox
- ttk
- csv
- xlrd
- os
- urllib
- pandas
- matplotlib
- numpy
- operator
- sqlite3
- re

---

# GUI.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv_code as csv
import download_XLS as xls
import plots as pl

pressed5 = False
pressed6 = False

def buttonClick1():
    try:
        pl.plot_1()
    except:
        messagebox.showerror("Error", "Download XLS and create CSVs first!")

def buttonClick2(cmb):
    try:
        if cmb.get() == "2011":
            pl.plot_2(2011)
        elif cmb.get() == "2012":
            pl.plot_2(2012)
        elif cmb.get() == "2013":
            pl.plot_2(2013)
        elif cmb.get() == "2014":
            pl.plot_2(2014)
        elif cmb.get() == "2015":
            pl.plot_2(2015)
        else:
            pl.plot_2(-1)
    except:
        messagebox.showerror("Error", "Download XLS and create CSVs first!")

def buttonClick3():
    try:
        pl.plot_3()
    except:
        messagebox.showerror("Error", "Download XLS and create CSVs first!")

def buttonClick4():
    try:
        pl.plot_4()
    except:
        messagebox.showerror("Error", "Download XLS and create CSVs first!")

def buttonClick5():
    global pressed5
    if not pressed5:
        xls.download_xls()
        messagebox.showinfo("Info", "Download successful")
        pressed5 = True
    else:
        messagebox.showerror("Error", "Already downloaded XLS")

def buttonClick6():
    global pressed6
    if not pressed6:
        csv.create_csv()
        messagebox.showinfo("Info", "Creation successful")
        pressed6 = True
    else:
        messagebox.showerror("Error", "Already created CSVs")

if __name__ == '__main__':
    # GUI setup code

---

# csv_code.py
import csv
import xlrd
import re
import os

def create_csv():
    # CSV creation code

---

# download_XLS.py
import urllib.request
import os

def download_xls():
    # XLS download code

---

# mysql_code.py
import sqlite3
import re
import xlrd
import os

def db_create_tables():
    # Database table creation code

def db_insert():
    # Database data insertion code

---

# plots.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import operator
import os

def plot_1():
    # Plotting code for total arrivals

def plot_2(grafhma_no):
    # Plotting code for 10 first countries with the biggest number of arrivals

def plot_3():
    # Plotting code for arrivals by means of transport

def plot_4():
    # Plotting code for arrivals per quarter

---

# requirements.txt
contourpy==1.0.7
cycler==0.11.0
fonttools==4.38.0
kiwisolver==1.4.4
matplotlib==3.6.3
numpy==1.24.1
packaging==23.0
pandas==1.5.3
Pillow==9.4.0
pyparsing==3.0.9
python-dateutil==2.8.2
pytz==2022.7.1
six==1.16.0
tk==0.1.0
xlrd==2.0.1
```

This pseudocode provides a structured overview of the code files, variables, dependencies, and functions involved in the project. It can be used as a blueprint to implement the same logic in various programming languages.
