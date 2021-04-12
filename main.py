import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re

# First get all the protein IDs
# (Monomers, No N and C modifications)
entry = []

with open("peptides.csv", newline='') as f:
    dbaasp = csv.reader(f)
    row1 = next(dbaasp)  # gets the first line
    for row in dbaasp:

        url = "https://dbaasp.org/peptide-card?id=" + str(row[0])
        options = Options()
        options.headless = True
        driver = webdriver.Chrome("/Users/sambinaislam/chromedriver", options=options)
        driver.get(url)


        def convert(lst):
            return [a for item in lst for a in item.split()]


        table = driver.find_element_by_class_name(
            "container-fluid.table.hemolytic-and-cytotoxic-activity-container.m-t-50").text

        other_info = re.findall(r'(.*50% Hemolysis.*)', table)
        Name = row[2]
        Sequence = row[4]

        # Converts the line into a comma separated list of items
        info_list = convert(other_info)

        if len(info_list) > 0:
            Target = info_list[0] + " " + info_list[1]
            Activity = info_list[2] + " " + info_list[3]
            Unit = info_list[5]
            Peptide_Conc = info_list[4]
            protein = {
                'ID': str(row[0]),
                'Name': Name,
                'Sequence': Sequence,
                'Target': Target,
                'Activity Measure': Activity,
                'Peptide Concentration': Peptide_Conc,
                'Unit': Unit
            }
            entry.append(protein)
        driver.close()
        df = pd.DataFrame(entry)
        df.to_csv(r'dbaasp2.csv', index=False, header=True)



