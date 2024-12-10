import pandas as pd

def remove_trailing_character(value, char_to_remove) -> str:
    """
    Deletes a character of choice from the end of a record, if it is present

    Args:
        value (str): a value to be checked
        char_to_remove (str): a character to be removed 

    Returns:
        str: a record without chosen char at the end.
    """
    if isinstance(value, str) and value.endswith(char_to_remove):
        return value[:-len(char_to_remove)]
    return value

def voter(dataframe, value_column, column_to_check):
    """
    Checks if there are multiple records in table corresponding to one unique value,
    then proceeds to swap values of chosen column into the most popular one among the records

    Args:
        value(str): a value to be checked
        dataframe(df): original dataframe
        value_column(str): original column of 'value' 
        column_to_check(str): column we want to have unified for one unique value

    Returns:
        str: the most popular value among the records
    """
    df = pd.DataFrame()

    values = dataframe[f'{value_column}'].unique()
    #print(f"Unique values in '{value_column}': {values}")

    for value in values:
        table = dataframe[dataframe[f'{value_column}'] == f"{value}"].copy()
        #print(f"Table for value '{value}':")
        #print(table)

        counts = table[f'{column_to_check}'].value_counts()
        #print(f"Value counts for '{column_to_check}':")
        #print(counts)

        winner = counts.idxmax()

        table.loc[:, f'{column_to_check} unified'] = winner
        #print(f"Updated table for value '{value}':")
        #print(table)

        df = pd.concat([df,table], axis=0, ignore_index=True)
    return df