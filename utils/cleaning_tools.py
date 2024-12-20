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

    encoding = (
            dataframe
            .groupby(strata_column)[column_to_check]
            .apply(lambda x: x.mode()[0])
            .dropna()  # Remove groups with only NaN
            .to_dict()
        )
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
    encoding = (
        dataframe
        .groupby(strata_column)[column_to_check]
        .median()
        .dropna()  # Remove groups with only NaN
        .to_dict()
    )
    return encoding

def stratified_NaN_filler(dataframe, strata_column, value_column, dictionary) -> pd.DataFrame:
    for stratum, median in dictionary.items():
        mask = (dataframe[f'{strata_column}'] == stratum) & (dataframe[f'{value_column}'].isna())
        dataframe.loc[mask, f'{value_column}'] = median
    return dataframe