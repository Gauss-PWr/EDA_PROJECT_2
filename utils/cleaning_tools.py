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

def occupation_count(df) -> dict:
    """
    Creates dictionary with occupations as keys and number of unique representatives as values

    Args:
        df: original dataframe
    
    Returns:
        dict: occupation : number of representatives
    """
    working_dict = {}
    for x in df.index: #creates dictionary with occupations as keys and empty sets as values
        if(df.loc[x, 'Occupation'] not in working_dict.keys()):
            working_dict[df.loc[x, 'Occupation']] = set()
    for x in df.index: #adds every customer id to value set
        working_dict[df.loc[x, 'Occupation']].add(df.loc[x, 'Customer_ID'])
    final_dict = {}
    for x in working_dict: #creates dictionary with occupations as keys and number of unique representatives as values
        final_dict[x] = len(working_dict[x])
    return final_dict