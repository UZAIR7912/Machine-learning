import pandas as pd
import statistics
wb = pd.read_excel("shedule.xlsx", sheet_name="book1")
wb = wb.drop(['Unnamed: 33', 'Unnamed: 34', 'Rs'], axis=1)
wb = wb.drop([12, 13, 14])
for index, row in wb.iterrows():
    for i, col in enumerate(wb.columns):
        if row[col] == 'R':
            if i >= 1 and i + 1 < len(wb.columns):
                prev_col = wb.columns[i - 1]
                next_col = wb.columns[i + 1]
                d_row_count = sum(1 for val in row if val in ['D', 'R/D'])
                n_row_count = sum(1 for val in row if val in ['N', 'R/N'])
                d_col_count = wb[col].isin(['D', 'R/D']).sum()
                n_col_count = wb[col].isin(['N', 'R/N']).sum()
                if (wb.at[index, prev_col] not in ["N", "R/N"]) and (wb.at[index, next_col] not in ["D", "R/D"]):
                    if d_row_count != 3 and d_col_count < 3:
                        wb.at[index, col] = "R/D"
                    elif n_row_count != 3 and n_col_count < 3:
                        wb.at[index, col] = "R/N"
                else:
                    if wb.at[index, prev_col] not in ['N', 'R/N'] and d_row_count != 3 and d_col_count < 3:
                        wb.at[index, col] = "R/D"
                    elif wb.at[index, next_col] not in ['D', 'R/D'] and n_row_count != 3 and n_col_count < 3:
                        wb.at[index, col] = "R/N"
wb['Total_Workdays'] = wb.apply(lambda row: sum(1 for val in row if val in ['R/D', 'R/N']), axis=1)
array = list(wb["Total_Workdays"])
average = round(statistics.mean(array))
for index, row in wb.iterrows():
    if row["Total_Workdays"] == average:
        continue
    elif row["Total_Workdays"] > average:
        i = 0
        while wb.at[index, "Total_Workdays"] > average and i < len(wb.columns):
            col = wb.columns[i]
            if col == "Total_Workdays":
                i += 1
                continue
            if wb.at[index, col] in ["R/D", "R/N"]:
                wb.at[index, col] = "R"
                wb.at[index, "Total_Workdays"] -= 1
            i += 1
    elif row["Total_Workdays"] < average:
        for indx, clmn in enumerate(wb.columns):
            if clmn == "Total_Workdays":
                break
            if wb.at[index, "Total_Workdays"] == average:
                break
            if wb.at[index, clmn] != "R":
                continue
            if indx >= 1 and indx + 1 < len(wb.columns):
                prev_col = wb.columns[indx - 1]
                next_col = wb.columns[indx + 1]
                d_row_count = sum(1 for val in row if val in ['D', 'R/D'])
                n_row_count = sum(1 for val in row if val in ['N', 'R/N'])
                d_col_count = wb[clmn].isin(['D', 'R/D']).sum()
                n_col_count = wb[clmn].isin(['N', 'R/N']).sum()
                if (wb.at[index, prev_col] not in ["N", "R/N"]) and (wb.at[index, next_col] not in ["D", "R/D"]):
                    if d_row_count != 3 and d_col_count < 3:
                        wb.at[index, clmn] = "R/D"
                elif (wb.at[index, prev_col] not in ["D", "R/D"]) and (wb.at[index, next_col] not in ["D", "R/D"]):
                    if n_row_count != 3 and n_col_count < 3:
                        wb.at[index, clmn] = "R/N"
                else:
                    if wb.at[index, prev_col] not in ["N", "R/N"] and d_row_count != 3 and d_col_count < 3:
                        wb.at[index, clmn] = "R/D"
                    elif wb.at[index, next_col] not in ["D", "R/D"] and n_row_count != 3 and n_col_count < 3:
                        wb.at[index, clmn] = "R/N"
            wb.at[index, "Total_Workdays"] = sum(1 for val in wb.loc[index] if val in ["R/D", "R/N"])
print(wb.iloc[:12, :33])