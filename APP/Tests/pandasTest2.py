import pandas as pd

# Sample DataFrame with x and y columns
def test():
    data = {'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'y': [5, 8, 12, 15, 18, 22, 25, 28, 32, 35]}
    df = pd.DataFrame(data)

    # Select every other row to reduce the values by half
    reduced_df = df.iloc[::2]

    print(reduced_df)

test()