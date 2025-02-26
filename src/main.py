import re
import os
import shutil
from textnode import *
from htmlnode import *
from splitnodes import *


def copy_contents(source_directory, target_directory): 
    
    source_path = os.path.abspath(source_directory)
    target_path = os.path.abspath(target_directory) 
    
    if os.path.exists(target_path) == True:
        shutil.rmtree(target_directory) 
        
    os.mkdir(target_path)
    
    for file in os.listdir(source_path):
        source_file = os.path.join(source_path, file)
        target_file = os.path.join(target_path, file)
        
        if os.path.isfile(source_file) == True:
            shutil.copy(source_file, target_file)
        elif os.path.isdir(source_file) == True:
            os.mkdir(target_file)
            copy_contents(source_file, target_file)


def copy_contents_prime(source_directory, target_directory): 
    
    source_path = os.path.abspath(source_directory)
    target_path = os.path.abspath(target_directory) 
    
    if os.path.exists(target_path) == True:
        shutil.rmtree(target_directory) 
    
    shutil.copytree(source_path, target_path) 


def main():
    copy_contents("./static/", "./public/")
    
if __name__ == "__main__":
    main()