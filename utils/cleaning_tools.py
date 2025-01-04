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

def remove_leading_character(value, char_to_remove) -> str:
    """
    Deletes a character of choice from the beginning of a record, if it is present

    Args:
        value (str): a value to be checked
        char_to_remove (str): a character to be removed 

    Returns:
        str: a record without chosen char at the beginning.
    """
    if isinstance(value, str) and value.startswith(char_to_remove):
        return value[len(char_to_remove) -1:]
    return value

def voter(dataframe, strata_column, column_to_check) -> dict:
    """
    Checks if there are multiple records in table corresponding to one unique value,
    then selects the most popular one among the records and with that,
    creates a dictionary for each pair.

    Args:
        dataframe(df): original dataframe
        value_column(str): original column of strata
        column_to_check(str): column we want to have unified for strata

    Returns:
        dict: stratum : the most popular value among the records for unique stratum
    """
    encoding = {}
    strata = dataframe[f'{strata_column}'].unique()

    for value in strata:
        table = dataframe[dataframe[f'{strata_column}'] == f"{value}"].copy()
        if table.empty:
            continue
        counts = table[f'{column_to_check}'].value_counts()
        if counts.empty:
            continue
        winner = counts.idxmax()
        encoding[value] = winner
    return encoding

def stratified_median_calculator(dataframe, strata_column, column_to_check) -> dict:
    """
    Computes the median for each individual stratum. Then creates a dictionary with
    strata and values of each.

    Args:
        dataframe(df): original dataframe
        value_column(str): original column of stratum
        column_to_check(str): column we want to have median calculated for strata

    Returns:
        dict: stratum : median
    """
    encoding = {}
    strata_list = dataframe[f'{strata_column}'].unique()
    for strata in strata_list:
        table = dataframe[dataframe[f'{strata_column}'] == f'{strata}'].copy()
        median = table[f'{column_to_check}'].median()
        encoding[strata] = median
    return encoding

def stratified_NaN_filler(dataframe, strata_column, value_column, dictionary) -> pd.DataFrame:
    for stratum, median in dictionary.items():
        mask = (dataframe[f'{strata_column}'] == stratum) & (dataframe[f'{value_column}'].isna())
        dataframe.loc[mask, f'{value_column}'] = median
    return dataframe

def count(column, df) -> dict:
    """
    Creates dictionary with desired column values as keys and number of unique 
    representatives as values.

    Args:
        column(str): column with desired values
        df: original dataframe
    
    Returns:
        dict: column values : number of representatives
    """
    working_dict = {}
    for x in df.index: #creates dictionary with column values as keys and empty sets as values
        if(df.loc[x, column] not in working_dict.keys() and not pd.isna(df.loc[x, column])):
            working_dict[df.loc[x, column]] = set()
    for x in df.index: #adds every customer id to value set
        if(not pd.isna(df.loc[x, 'Credit_Score'])):
            working_dict[df.loc[x, column]].add(df.loc[x, 'Customer_ID'])
    final_dict = {}
    for x in working_dict: #creates dictionary with column values as keys and number of unique representatives as values
        final_dict[x] = len(working_dict[x])
    final_dict = {key : final_dict[key] for key in sorted(final_dict)} #alphabetical order
    return final_dict

def percentage(dictionary) -> dict:
    """
    Creates the same dictionary, but with percentage of the total as values 
    (instead of number of representatives). 

    Args:
        dictionary(dict)
    
    Returns:
        dict: column values : percentage of the total
    """
    sum_values = sum(dictionary.values())
    final_dict = {}
    for x in dictionary:
        final_dict[x] = round(dictionary[x]/sum_values*100, 2)
    return final_dict