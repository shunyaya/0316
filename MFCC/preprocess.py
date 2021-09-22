import os

def save_mfcc(dataset_path, json_path, n_mfcc=13, n_fft=2048, hop_length=512, num_segments=5):

    # Dictionary to store data
    data = {
        "mapping" : [],
        "mfcc" : [],
        "lable" :[]
    }

    # loop through all the genres
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
        
        # ensure that we're not at the root level
       