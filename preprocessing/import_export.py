import pandas as pd

def import_csv2pd(file_name):
    """Import csv to pandas dataframe. Based on the stm data. The first row of the data need to be the column name."""
    data = pd.read_csv(file_name, sep=';', encoding='latin-1' )
    return data

def clean(df):
    #df = df.replace('NaN', None)
    df = set_data_type(df, 'Date')

    #df.dropna()

    return df


def set_data_type(df, datetime_column):
    #df.loc[:, df.columns != datetime_column] = df.loc[:, df.columns != datetime_column].apply(pd.to_numeric, errors='coerce')
    pd.to_datetime(df[datetime_column], errors='coerce')
    column_list = (list(df.columns))
    column_list.remove(datetime_column)
    for c in column_list:
        pd.to_numeric(df[c], errors='coerce')
    df = df.dropna()

    #df = df.astype(float)
    #df['Price'] = df['Price'].astype(float)
    #df = df.apply(pd.to_numeric(df, errors='coerce'))
    print(df.head())
    print(df.dtypes)
    print(df)
   # print(df.dtypes)
   # print(df)
    #print(df.dtypes)
   # print(df.head())
    #df[datetime_column].to_datetime(errors='coerce')
    #df.dropna()

    return df

