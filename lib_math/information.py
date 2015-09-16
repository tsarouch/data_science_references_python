import math
import pandas as pd


def entropy(df, attribute):
    """
    Calculates the entropy of a dataframe for the passed attribute.
    :param df: DataFrame
    :attribute: the attribute we want to calculate the entropy on
    returns the entropy of the attribute
    """

    _entropy = 0.0
    freq = {}

    N = len(df)
    for ii in range(N):
        row = df.iloc[[ii]]
        attribute_val = row[attribute].values[0]
        if (attribute_val in freq):
            freq[attribute_val] += 1.0
        else:
            freq[attribute_val]  = 1.0
    for freqi in freq.values():
        _entropy += (-freqi / N) * math.log(freqi / N, 2)

    return _entropy


def information_gain(df, attribute, target_attribute):
    """
    Calculates the information gain which measures how much an attribute
    improves (decreases) entropy over the whole segmentation it creates.
    Strictly speaking, information gain measures the change in entropy due to
    any amount of new information being added
    :param df: DataFrame which holds our data
    :param attribute: any attribute that we want to study the IG
    :param target_attribute: the target attribute, used for the global entropy
    returns information gain
    """
    subset_entropy = 0.0
    freq = {}

    for ii in range(len(df)):
        row = df.iloc[[ii]]
        attribute_val = row[attribute].values[0]
        if (attribute_val in freq):
            freq[attribute_val] += 1.0
        else:
            freq[attribute_val]  = 1.0

    for val in freq.keys():
        val_prob = freq[val] / sum(freq.values())
        df_subset = df[df[attribute] == val]
        subset_entropy += val_prob * entropy(df_subset, target_attribute)

    return (entropy(df, target_attribute) - subset_entropy)
