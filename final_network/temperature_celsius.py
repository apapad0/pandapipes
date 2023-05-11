import pandas


def temp_to_celsius(path):
    df = pandas.read_excel(f"{path}.xlsx", usecols=lambda x: 'Unnamed' not in str(x))
    for i in range(len(df)):
        for j in range(len(df.columns)):
            df.iat[i, j] -= 273.15

    df.to_excel(f"{path}_celsius.xlsx")
