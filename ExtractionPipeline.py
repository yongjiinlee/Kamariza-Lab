from StorageExtraction import StorageExtraction
import pandas as pd

class ExtractionPipeline(StorageExtraction):
    '''
    ExtractionPipeline is a class that inherits from the StorageExtraction class (for reference, look at the StorageExtraction.py file in the Preprocessor folder). 
    The class is an entry-first pipeline that combines all the functions of the StorageExtraction class and creates a dataframe from it.
    Functions:
    __init__: Initializes the class with the root path and file type
    ExtractPipeline: Extracts the files, slides, Z-stacks, channels, species, labeling, and objective from the root path
    MakeDataFrame: Creates a dataframe from the extracted data

    Parameters:
    root_path: The root path of the files
    file_type: The file type of the files to be extracted
    datadict: A dictionary containing the filenames, path, and images as numpy arrays
    slide_number: The number of slides in the filenames
    zstack: The number of Z-stacks in the filenames
    channel_number: The number of channels in the filenames
    species: The species in the filenames
    labeling: The labeling in the filenames
    objective: The objective in the filenames
    '''
    def __init__(self, root_path, file_type = '.tif', slidenumber = 11, zstack = 10, channelnumber = 3, species = ['Msmeg'], labeling = ['DMN'], objective = ['60X','160X']):
        super().__init__(root_path, file_type, slidenumber, zstack, channelnumber, species, labeling, objective)
    
    def ExtractPipeline(self):
        self.ExtractSlides()
        self.ExtractZStack()
        self.ExtractChannel()
        self.ExtractSpecies()
        self.ExtractLabeling()
        self.ExtractObjective()
        return self.datadict
    
    def MakeDataFrame(self):
        data = self.ExtractPipeline()
        df = pd.DataFrame(data)
        return df