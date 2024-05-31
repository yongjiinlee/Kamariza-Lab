import numpy as np
import pandas as pd
import cv2
import os
from concurrent.futures import ThreadPoolExecutor

class StorageExtraction():
    '''
    StorageExtraction is an entry-level class that extracts files from a root path and generates a dictionary with the filenames, path, and images as numpy arrays.
    Functions:
    __init__: Initializes the class with the root path and file type
    ExtractFiles: Extracts the files from the root path
    ExtractSlides: Extracts the slide number from the filenames
    ExtractZStack: Extracts the Z-stack number from the filenames
    ExtractChannel: Extracts the channel number from the filenames
    ExtractSpecies: Extracts the species from the filenames
    ExtractLabeling: Extracts the labeling from the filenames
    ExtractObjective: Extracts the objective from the filenames
    ReadConvert: Converts the images to numpy arrays
    StoreImgs: Stores the images in the dictionary as numpy arrays

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
    #Initialize the class with the file path
    def __init__(self, root_path, file_type = '.tif', slidenumber = 11, zstack = 10, channelnumber = 3, species = ['Msmeg'], labeling = ['DMN'], objective = None):
        if objective is None:
            objective = ['10X', '20X', '40X', '60X', '100X', '120X', '140X', '160X']
        self.root_path = root_path
        self.file_type = file_type
        self.slide_number = slidenumber
        self.zstack = zstack
        self.channel_number = channelnumber
        self.species = species
        self.labeling = labeling
        self.objective = objective
        self.datadict = self.ExtractFiles()
    
    #Extract the files from the root path
    def ExtractFiles(self):
        #Create an empty dictionary to store filenames and paths
        datadict = {'Filename':[], 'Path': []}
        
        #Walk through the root path and extract the files
        for root, dirs, file in os.walk(self.root_path):
            for f in file:
                if f.endswith(self.file_type):
                    datadict['Filename'].append(f)
                    datadict['Path'].append(os.path.join(root + '/'+ f))
        return datadict
    
    #Extract the slide number from the filenames
    def ExtractSlides(self):
        filenames = self.datadict['Filename']
        #Empty slide list to store the slide numbers
        slides = []
        #Iterate through the filenames and extract the slide number
        for f in filenames:
            slidebase = 's'
            for i in range(0, self.slide_number + 1):
                if i < 10:
                    slide = slidebase + str(0) + str(i)
                else:
                    slide = slidebase + str(i)
                if slide in f:
                    print(f'Slide {slide} found in {f}')
                    slides.append(i)
                    break
        self.datadict['Slide'] = slides
        return self.datadict

    #Extract the Z-stack number from the filenames
    def ExtractZStack(self):
        filenames = self.datadict['Filename']
        zstack = []
        for f in filenames:
            zbase = 'z'
            for i in range(0, self.zstack + 1):
                if i < 10:
                    z = zbase + str(0) + str(i)
                else:
                    z = zbase + str(i)
                if z in f:
                    print(f'Z-stack {z} found in {f}')
                    zstack.append(i)
                    break
        self.datadict['ZStack'] = zstack
        return self.datadict
    
    #Extract the channel number from the filenames
    def ExtractChannel(self):
        filenames = self.datadict['Filename']
        channels = []
        for f in filenames:
            zbase = 'ch'
            channel_found = False
            for i in range(0, self.channel_number + 1):
                if i < 10:
                    channel = zbase + '0' + str(i)
                else:
                    channel = zbase + str(i)
                if channel in f:
                    print(f'Channel {channel} found in {f}')
                    channels.append(i)
                    channel_found = True
                    break
            
            if not channel_found:
                if 'overlay' in f:
                    print(f'Overlay found in {f}')
                    channels.append('overlay')
                else:
                    print(f'No channel or overlay found in {f}')
                    channels.append(None)
        
        self.datadict['Channel'] = channels
        return self.datadict
    
    #Extract the species from the filenames
    def ExtractSpecies(self):
        filenames = self.datadict['Filename']
        species = []
        for f in filenames:
            for s in self.species:
                if s in f:
                    print(f'Species {s} found in {f}')
                    species.append(s)
                    break
        self.datadict['Species'] = species
        return self.datadict
    
    #Extract the labeling from the filenames
    def ExtractLabeling(self):
        filenames = self.datadict['Filename']
        labeling = []
        for f in filenames:
            for l in self.labeling:
                if l in f:
                    print(f'Labeling {l} found in {f}')
                    labeling.append(l)
                    break
        self.datadict['Labeling'] = labeling
        return self.datadict
    
    #Extract the objective from the filenames
    def ExtractObjective(self):
            filenames = self.datadict['Filename']
            objective = []
            for f in filenames:
                f_lower = f.lower()
                objective_found = False
                for o in self.objective:
                    if o.lower() in f_lower:
                        print(f'Objective {o} found in {f}')
                        objective.append(o)
                        objective_found = True
                        break
                if not objective_found:
                    print(f'No objective found in {f}')
                    objective.append(None)
            self.datadict['Objective'] = objective
            return self.datadict
    
    #Use ReadConvert with imread to convert the images to numpy arrays
    def ReadConvert(self, path):
        print(f"Converting {path} to Numpy Array...")
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        return img
    
    #Store the images in the dictionary as numpy arrays
    def StoreImgs(self):
        path = self.datadict['Path']
        #Use multithreading to parallelize the conversion process
        with ThreadPoolExecutor() as executor:
            imgs = list(executor.map(self.ReadConvert, path))
        self.datadict['Image'] = imgs
        return self.datadict