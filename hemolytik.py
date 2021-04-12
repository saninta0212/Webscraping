import pandas as pd
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# First get all the protein IDs

url1 = "http://crdd.osdd.net/raghava/hemolytik/naturalseqL.txt"

html1 = uReq(url1)
page_html1 = html1.read()
html1.close()
soup1 = soup(page_html1, "html.parser")
df1 = pd.DataFrame(soup1)
df1.to_csv("hemolytik.txt", index=False, header=True)
