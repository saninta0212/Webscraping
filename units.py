import pandas as pd
import re

# https://www.thermofisher.com/ca/en/home/references/ambion-tech-support/rna-tools-and-calculators/proteins-
# and-amino-acids.html

aa_weight = {"A": 89.1, "R": 174.2, "N": 132.1, "D": 133.1, "C": 121.2, "E": 147.1, "Q": 146.2,
             "G": 75.1, "H": 155.2, "I": 131.2, "L": 131.2, "K": 146.2, "M": 149.2, "F": 165.2,
             "P": 115.1, "S": 105.1, "T": 119.1, "W": 204.2, "Y": 181.2, "V": 117.1
             }

dataset = pd.read_csv("dbaasp_processed1.csv")

a = 0
entry_1 = []
while a < 497:
    if re.search("±", dataset.iloc[a]["Peptide Concentration"]):
        my_match = re.search(r"((\d+)(\.\d+)?)?±((\d+)(\.\d+)?)?", dataset.iloc[a]["Peptide Concentration"])
        lower_con = round(float(my_match.group(1)) - float(my_match.group(4)), 2)
        entry_1.append(lower_con)
    else:
        entry_1.append(float(re.findall(r"\d+", dataset.iloc[a]["Peptide Concentration"])[0]))
    a = a + 1
dataset["Lower Concentration"] = entry_1

a = 0
entry_2 = []
while a < 497:
    if dataset.iloc[a]["Unit"] == "µg/ml":
        seq = dataset.iloc[a]["Sequence"].upper()
        len_seq = len(seq)

        i = 0
        weight = 0.00

        while len_seq > 0:
            weight = aa_weight.get(seq[i]) + weight
            i = i + 1
            len_seq = len_seq - 1

        mol_weight = weight - 18 * (len(seq) - 1)
        pp = dataset.iloc[a]["Lower Concentration"]
        # concentration = re.findall(r"\d+", pp)
        # concentration = int(concentration[0])
        new_conc = 1000 * pp / mol_weight
        entry_2.append(f'{new_conc:.4}')
    else:

        entry_2.append(dataset.iloc[a]["Lower Concentration"])
    a = a + 1

entry_3 = []
for item in entry_2:
    entry_3.append(float(item))
dataset["Processed Concentration"] = entry_3

# To find duplicate Sequences
duplicates = dataset[dataset.duplicated(['Sequence'])]
print(duplicates)
# print(dataset.iloc[20,5]) same as doing dataset.iloc[20]["Peptide Concentration"]

# To get the range of values :
range_conc = []
c = 0
while c < 497:
    if ">" in dataset.iloc[c]["Peptide Concentration"] or re.findall(r"\d+<", dataset.iloc[c]["Peptide Concentration"]) \
            or ">>" in dataset.iloc[c]["Peptide Concentration"]:
        range_conc.append(dataset.iloc[c]["Processed Concentration"])
    c = c + 1
# print(range_conc)
# print(sum(range_conc)/len(range_conc))
#
# print(len(range_conc))

# ID 11385 and 4675, ID 13517 and 2025, ID 16253 and 4806 have duplicates
# if dataset.loc[dataset['ID'] == 11385]["Processed Concentration"].values < dataset.loc[dataset['ID'] ==
#                                                                                        4675][
#     "Processed Concentration"].values:
#     dataset.loc[dataset['ID'] == 4675]["Processed Concentration"] = dataset.loc[dataset['ID'] ==
#                                                                                 11385]["Processed Concentration"].values
# else:
#     dataset.loc[dataset['ID'] == 11385]["Processed Concentration"] = dataset.loc[dataset['ID'] ==
#                                                                                  4675]["Processed Concentration"].values
# dataset.to_csv("dbaasp_processed2.csv", index=False, header=True)
