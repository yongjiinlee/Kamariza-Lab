import numpy as np
import pandas as pd
import os
from sklearn.pipeline import Pipeline
from StorageExtractionTransformer import StorageExtractionTransformer
from Transformers import FileNameDropper, MetaDataEncoder

class TransformerPipeline:
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
        self.pipe = self.MakePipeline()
    
    def MakePipeline(self):
        #Create a pipeline with the StorageExtractionTransformer, FileNameDropper, and MetaDataEncoder
        pipe = Pipeline([
            ('StorageExtractionTransformer', StorageExtractionTransformer(self.root_path, self.file_type, self.slidenumber, self.zstack, self.channel_number, self.species, self.labeling, self.objective)),
            ('FileNameDropper', FileNameDropper()),
            ('MetaDataEncoder', MetaDataEncoder())
        ])
        return pipe
    
    #Transform the data
    def TransformData(self):
        data = self.pipe.fit_transform(None)
        return data
    
    #Create a DataFrame from the transformed data
    def MakeDataFrame(self):
        data = self.TransformData()
        df = pd.DataFrame(data)
        return df