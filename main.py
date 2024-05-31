import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from ExtractionPipeline import ExtractionPipeline
from Transformers import FileNameDropper, MetaDataEncoder
from TransformerPipeline import TransformerPipeline
from StorageExtractionTransformer import StorageExtractionTransformer

def main():
    root = 'D:/8-31-2023 Leica Scan/Unmerged-data/DMN'
    file_type = '.tif'
    slidenumber = 11
    zstack = 10
    channel_number = 3
    species = ['Msmeg']
    labeling = ['DMN']
    objective = ['60X', '160X']
    pipe = TransformerPipeline(root, file_type, slidenumber, zstack, channel_number, species, labeling, objective).MakeDataFrame()
    print(pipe)

if __name__ == '__main__':
    main()
