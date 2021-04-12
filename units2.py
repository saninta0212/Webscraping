import pandas as pd
import re

dataset = pd.read_csv("hemo_5.csv")
# https://www.thermofisher.com/ca/en/home/references/ambion-tech-support/rna-tools-and-calculators/proteins-
# and-amino-acids.html

a = 0
unit_list = []
while a < 81:
    if "μg/ml" in dataset.iloc[a]["ACTIVITY"] or "µg/mL" in dataset.iloc[a]["ACTIVITY"]:
        unit_list.insert(a, "μg/ml")

    else:
        unit_list.insert(a, "μM")

    a = a + 1
dataset["Unit"] = unit_list

aa_weight = {"A": 89.1, "R": 174.2, "N": 132.1, "D": 133.1, "C": 121.2, "E": 147.1, "Q": 146.2,
             "G": 75.1, "H": 155.2, "I": 131.2, "L": 131.2, "K": 146.2, "M": 149.2, "F": 165.2,
             "P": 115.1, "S": 105.1, "T": 119.1, "W": 204.2, "Y": 181.2, "V": 117.1
             }

b = 0
entry = []
while b < 81:
    if dataset.iloc[b, 12] == "μg/ml" or dataset.iloc[b, 12] == "μg/mL":

        seq = dataset.iloc[b]["Sequence"].upper()
        len_seq = len(seq)

        i = 0
        weight = 0.00

        while len_seq > 0:
            weight = aa_weight.get(seq[i]) + weight
            i = i + 1
            len_seq = len_seq - 1

        mol_weight = weight - (18.015 * len(seq)-1)
        pp = dataset.iloc[b]["ACTIVITY"]
        pattern = re.findall(r"(\d+)(\.\d+)?", pp)[-1][0]+re.findall(r"(\d+)(\.\d+)?", pp)[-1][1]
        concentration = float(pattern)
        new_conc = (1000 * concentration) / mol_weight
        entry.append(f'{new_conc:.4}')

    else:
        entry.append(int(re.findall(r"\d+", dataset.iloc[b]["ACTIVITY"])[-1]))
    b = b + 1

dataset["Processed Concentration"] = entry
duplicates = dataset[dataset.duplicated(['Sequence'])]
print(duplicates)
dataset.to_csv("hemolytik_processed3.csv", index=False, header=True)

# this part is to get the range of values with > in concentration
range_conc = []
c = 0
while c < 81:
    if ">" in dataset.iloc[c]["ACTIVITY"]:
        range_conc.append(dataset.iloc[c]["Processed Concentration"])
    c = c + 1
print(range_conc)