import numpy as np
import pandas as pd
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder

'''
FileNameDropper and MetaDataEncoder are classes that serve as transformers in the preprocessing pipeline. FileNameDropper drops the 'Filename' column from the DataFrame. 
MetaDataEncoder uses the OneHotEncoder, which is a transformer that streamlines and encodes the metadata columns as one-hot vectors. MetaDataEncoder converts all of the metadata values to strings to columns
and associates them to the corresponding metadata columns. The class then drops the original metadata columns from the DataFrame.

Functions:
fit: Fits the transformer
transform: Transforms the data
'''
class FileNameDropper(BaseEstimator, TransformerMixin):
    #Fit the transformer
    def fit(self, X, y=None):
        return self
    
    #Transform the data by dropping the 'Filename' column
    def transform(self, X):
        return X.drop(['Filename'], axis=1)

class MetaDataEncoder(BaseEstimator, TransformerMixin):
    #Initialize the class with the OneHotEncoder
    def __init__(self):
        self.encoder = OneHotEncoder(sparse=False)
    
    #Fit the transformer by fitting the OneHotEncoder to the metadata columns
    def fit(self, X, y=None):
        self.encoder.fit(X[['Slide', 'ZStack','Channel', 'Species', 'Labeling', 'Objective']])
        return self
    
    #Transform the data by encoding the metadata columns
    def transform(self, X):
        #Start the encoding process using a matrix
        encoded_matrix = self.encoder.transform(X[['Slide', 'ZStack', 'Channel', 'Species', 'Labeling', 'Objective']])
        
        #Create a DataFrame with the encoded matrix
        encoded_df = pd.DataFrame(
            encoded_matrix,
            columns=self.encoder.get_feature_names_out(['Slide', 'ZStack','Channel', 'Species', 'Labeling', 'Objective'])
        )
        
        #Reset the index to prevent errors during concatenation
        X = X.reset_index(drop=True)
        X = pd.concat([X, encoded_df], axis=1)
        
        # Drop original columns
        return X.drop(['Slide', 'ZStack','Channel', 'Species', 'Labeling', 'Objective'], axis=1)