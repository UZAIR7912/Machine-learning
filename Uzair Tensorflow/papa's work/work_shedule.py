import pandas as pd
import statistics
wb = pd.read_excel("shedule.xlsx", sheet_name="book1")
wb = wb.drop(['Unnamed: 33',"Unnamed: 34","Rs"], axis=1)
wb = wb.drop([12,13,14])
wb['count_Rs'] = wb.apply(lambda row: sum(1 for val in row if val in ['R']), axis=1)
for index,row in wb.iterrows():
    change_ratio = wb.at[index,'count_Rs']
    change_ratio = round(change_ratio/3)
    for i ,col in enumerate(wb.columns):
        if row[col] == 'R' and change_ratio > 0:
            if i >= 1 and i + 1 < len(wb.columns):
                prev_col = wb.columns[i - 1]
                next_col = wb.columns[i + 1]
                if (wb.at[index,prev_col] != "N" and wb.at[index,prev_col] != "R/N") and (wb.at[index,next_col] != "D" and wb.at[index,next_col] != "R/D"):
                    d_type_count = wb[col].isin(['D', 'R/D']).sum()
                    n_type_count = wb[col].isin(['N', 'R/N']).sum()
                    if d_type_count != 3:
                        wb.at[index,col] = "R/D"
                        change_ratio -= 1
                    elif n_type_count != 3:
                        wb.at[index,col] = "R/N"
                        change_ratio -= 1
                else:
                    d_type_count = wb[col].isin(['D', 'R/D']).sum()
                    n_type_count = wb[col].isin(['N', 'R/N']).sum()                  
                    if wb.at[index,prev_col] != 'N' and wb.at[index,prev_col] != 'R/N':
                        if d_type_count != 3:
                            wb.at[index,col] = "R/D"
                            change_ratio -= 1
                    elif wb.at[index,next_col] != 'D' and wb.at[index,next_col] != 'R/D':
                        if n_type_count != 3:
                            wb.at[index,col] = "R/N"
                            change_ratio -= 1
    print(change_ratio)
wb['OT'] = wb.apply(lambda row: sum(1 for val in row if val in ['R/D', 'R/N']), axis=1)
array = list(wb["OT"])
average = round(statistics.mean(array)) + 2
for index,row in wb.iterrows():
    if row["OT"] == average:
        pass
    elif row["OT"] > average:
        i = 0
        if col == "OT":
            i += 1
            continue
        while wb.at[index, "OT"] > average and i < len(wb.columns):
            col = wb.columns[i]
            if wb.at[index, col] == "R/D" or wb.at[index, col] == "R/N":
                wb.at[index, col] = "R"
                wb.at[index, "OT"] -= 1
            i += 1
    elif row["OT"] < average:
        for indx, clmn in enumerate(wb.columns):
            if clmn == "OT":
                break
            if wb.at[index, "OT"] == average:
                break
            if wb.at[index, clmn] != "R":
                continue

            if indx >= 1 and indx + 1 < len(wb.columns):
                prev_col = wb.columns[indx - 1]
                next_col = wb.columns[indx + 1]

                d_type_count = wb[clmn].isin(['D', 'R/D']).sum()
                n_type_count = wb[clmn].isin(['N', 'R/N']).sum()

                if (wb.at[index, prev_col] not in ["N", "R/N"]) and (wb.at[index, next_col] not in ["D", "R/D"]):
                    if d_type_count != 3:
                        wb.at[index, clmn] = "R/D"
                elif (wb.at[index, prev_col] not in ["D", "R/D"]) and (wb.at[index, next_col] not in ["D", "R/D"]):
                    if n_type_count != 3:
                        wb.at[index, clmn] = "R/N"
                else:
                    if wb.at[index, prev_col] not in ["N", "R/N"] and d_type_count != 3:
                        wb.at[index, clmn] = "R/D"
                    elif wb.at[index, next_col] not in ["D", "R/D"] and n_type_count != 3:
                        wb.at[index, clmn] = "R/N"
            wb.at[index, "OT"] = sum(1 for val in wb.loc[index] if val in ["R/D", "R/N"])
print(wb.iloc[:12, :34])
#wb.to_excel("shedule(distrubuted).xlsx",index=False)