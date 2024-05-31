import numpy as np
import pandas as pd
import os
from sklearn.base import BaseEstimator, TransformerMixin
from StorageExtraction import StorageExtraction

class StorageExtractionTransformer(BaseEstimator, TransformerMixin):
    '''
    StorageExtractionTransformer is a class that inherits from the BaseEstimator and TransformerMixin classes from the sklearn library and uses the StorageExtraction 
    class to extract files from a root path and generates a dictionary with the filenames, path, and images as numpy arrays. The class then transforms the dictionary
    into a pandas DataFrame and encodes the metadata columns using the OneHotEncoder class from the sklearn library.

    Functions:
    __init__: Initializes the class with the root path and file type
    fit: Fits the transformer
    transform: Transforms the data

    Parameters:
    root_path: The root path of the files
    file_type: The file type of the files to be extracted
    slidenumber: The number of slides in the filenames
    zstack: The number of Z-stacks in the filenames
    channel_number: The number of channels in the filenames
    species: The species in the filenames
    labeling: The labeling in the filenames
    objective: The objective in the filenames
    storage_extraction: An instance of the StorageExtraction class
    '''

    #Initialize the class with the root path and file type
    def __init__(self, root_path, file_type='.tif', slidenumber=11, zstack=10, channel_number=3, species=['Msmeg'], labeling=['DMN'], objective=['60X', '160X']):
        self.root_path = root_path
        self.file_type = file_type
        self.slidenumber = slidenumber
        self.zstack = zstack
        self.channel_number = channel_number
        self.species = species
        self.labeling = labeling
        self.objective = objective
        self.storage_extraction = StorageExtraction(root_path, file_type, slidenumber, zstack, channel_number, species, labeling, objective)
    
    #Fit the transformer
    def fit(self, X=None, y=None):
        return self
    
    def transform(self, X=None):
        #Extract the data (see documentation for StorageExtraction class)
        self.storage_extraction.ExtractChannel()
        self.storage_extraction.ExtractObjective()
        self.storage_extraction.ExtractSpecies()
        self.storage_extraction.ExtractLabeling()
        self.storage_extraction.ExtractSlides()
        self.storage_extraction.ExtractZStack()
        
        #Dictionary containing the extracted data
        datadict = self.storage_extraction.datadict
        
        # Ensure required columns are present
        for col in ['Slide', 'ZStack', 'Species', 'Labeling']:
            if col not in datadict:
                datadict[col] = [None] * len(datadict['Filename'])
        
        # Convert all values to strings
        for col in ['Slide', 'ZStack', 'Channel', 'Species', 'Labeling', 'Objective']:
            datadict[col] = [str(x) for x in datadict.get(col, [])]
        
        return pd.DataFrame(datadict)