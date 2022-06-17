import pandas as pd

dict1 = {8: {1: 0, 2: 0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 0, 7: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 17: 0.4, 18: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0}, 
14: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 9: 1.0, 10: 0, 11: 0, 12: 1.0, 13: 1.0, 17: 0, 18: 0, 23: 0.46, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0}, 
15: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 17: 0, 18: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0}, 
19: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 17: 0.32, 18: 1.0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 1.0, 30: 0}, 
20: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 17: 0.29, 18: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0}, 
21: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 17: 0, 18: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0}, 
22: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 17: 0, 18: 0, 23: 0.54, 24: 0, 25: 0, 26: 1.0, 27: 0, 28: 1.0, 29: 0, 30: 0}}

# print(type(dict1))
# print(dict1)
head = dict1.keys()
cols = dict1[8].keys()

lst = []
for h in head:
    l = []
    for k, v in dict1[h].items():
        l.append(v)
    lst.append(l)
lst = list(map(list, zip(*lst)))
print(lst)
df = pd.DataFrame(lst, index=cols, columns=head)
df.to_excel("membership_value_30.xlsx")
# print(head)
# print()
# print(cols)