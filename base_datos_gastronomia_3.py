# %%
import hashlib
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import re
from bs4 import BeautifulSoup as bs
import time

#Se cambia Sellenium (imposible de ejecutar en Streamlit web) por el csv creado.

# %%
df_dish1=pd.read_csv("data/taste_atlas2.csv")

# %%



