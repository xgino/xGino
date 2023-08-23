from floorbal_stick_scraper import data_manipulation
import pandas as pd
from tqdm import tqdm

#data_manipulation()

def clean():
    df = pd.read_csv('stick.csv')
    df = df.replace('\n','', regex=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    #df = df[df['feature_dict'].str.contains("Weight", na=False)]

    print(df["price"].head(10))

    feature_dict = df["feature_dict"].str.split(",", expand=True).replace('\W', '', regex=True)
    df["weight"] = feature_dict[19]
    df["weight1"] = feature_dict[20]

    

    # df.sort_values('weight', ascending=False)

    #print(df["weight"])


    df.to_excel("stick_weight.xlsx")

clean()

