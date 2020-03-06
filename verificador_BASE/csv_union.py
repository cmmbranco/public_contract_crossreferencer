import pandas as pd

DATA_FILE = 'data.csv'
NIFS_FILE = 'racius.csv'


data = pd.read_csv(DATA_FILE)
nifs = pd.read_csv(NIFS_FILE)


combined_csv = data.merge(nifs, left_on='winner_nif', right_on='nif')

combined_csv.drop(combined_csv.columns[len(combined_csv.columns)-1], axis=1, inplace=True)

#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

print(combined_csv)
