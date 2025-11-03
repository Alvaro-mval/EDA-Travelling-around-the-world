# %%
import hashlib
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import re
import time
from bs4 import BeautifulSoup as bs

#Se cambia Sellenium (imposible de ejecutar en Streamlit web) por el csv creado.


# %%
df_taste_atlas1 = pd.read_csv("data/taste_atlas1.csv")

# %%



