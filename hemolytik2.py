import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

entry = []
with open("hemolytik2.csv", newline='') as f:
    hemo = csv.reader(f)
    row1 = next(hemo)  # gets the first line
    for row in hemo:
        url = "http://crdd.osdd.net/raghava/hemolytik/display_sub.php?details=" + str(row[0])
        options = Options()
        options.headless = True
        driver = webdriver.Chrome("/Users/sambinaislam/chromedriver", options=options)
        driver.get(url)

        ID = row[0]
        SEQUENCE = row[1]
        NAME = driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[7]/td[2]').text
        CMOD = driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[8]/td[2]').text
        NMOD = driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[9]/td[2]').text
        LINEAR_CYCLIC = \
            driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[10]/td[2]').text
        STEREO = driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[11]/td[2]').text
        MODRESIDUE = driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[12]/td[2]').text
        FUNCTION = \
            driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[13]/td[2]/font').text
        ACTIVITY = driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[14]/td[2]').text
        RBC_SOURCE = driver.find_element_by_xpath\
            ('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[15]/td[2]/font').text
        LENGTH = driver.find_element_by_xpath('//*[@id="templatemo_right_column"]/table[4]/tbody/tr[6]/td[2]/font').text

        protein = {
            'ID': ID,
            'Name': NAME,
            'Sequence': SEQUENCE,
            'C-MODIFICATION': CMOD,
            'N-MODIFICATION': NMOD,
            'LINEAR/CYCLIC': LINEAR_CYCLIC,
            'STEREOCHEMISTRY': STEREO,
            'MODIFIED-RESIDUE': MODRESIDUE,
            'FUNCTION': FUNCTION,
            'ACTIVITY': ACTIVITY,
            'RBC_SOURCE': RBC_SOURCE,
            'LENGTH': LENGTH

        }
        entry.append(protein)
        driver.close()
        df = pd.DataFrame(entry)
        df.to_csv(r'hemolytik_output2.csv', index=False, header=True)

