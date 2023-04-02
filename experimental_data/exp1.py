import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("Data Exp 1/sca1_data.txt", sep="\t")
    df.drop(["sex", "age", "title"], axis=1, inplace=True)
    print(df.head(15))
