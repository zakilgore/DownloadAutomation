# Zachary Kilgore
# Copyright 2019
# Credit to https://www.youtube.com/watch?v=qbW6FRbaSl0 for this idea
# Contact email: kilgorez@email.sc.edu

# import statements
from watchdog.events import FileSystemEventHandler
import os
import json
import datetime
from zipfile import ZipFile
import sys

# FILE INTEGER NUMS
# 1 - jpg or jpeg
# 2 - txt
# 3 - csv OR xsl
# 4 - psd OR ai
# 5 - abr
# 6 - zip
# 7 - otherwise

#class to handle
# @param: FileSystemEventHandler



# Function that makes folders and returns the path based on file types
# @param: fileType      -> integer that specifies what kind of file is being used
#                          the integers are specified in the comments above
# @param: day_folder    -> the folder for the current day
# Returns the path for the files new folder
def makeFolder(fileType, day_folder):
    folder_destination = day_folder
    if fileType == 1:
        folder_destination += "/" + "Images"
        try:
            os.mkdir(folder_destination)
        except FileExistsError:
            pass
    elif fileType == 2:
        folder_destination += "/" + "Documents"
        try:
            os.mkdir(folder_destination)
        except FileExistsError:
            pass
    elif fileType == 3:
        folder_destination += "/" + "Excel_Files"
        try:
            os.mkdir(folder_destination)
        except FileExistsError:
            pass
    elif fileType == 4:
        folder_destination += "/" + "Adobe_Files"
        try:
            os.mkdir(folder_destination)
        except FileExistsError:
            pass
    elif fileType == 5:
        folder_destination += "/" + "Photoshop_Brushes"
        try:
            os.mkdir(folder_destination)
        except FileExistsError:
            pass
    elif fileType == 6:
        folder_destination += "/" + "ZIP_Compressed"
        try:
            os.mkdir(folder_destination)
        except FileExistsError:
            pass
    elif fileType == 7:
        folder_destination = desktop + "/_" + "Random"
        try:
            os.mkdir(folder_destination)
        except FileExistsError:
            pass
    return folder_destination



# Arrays for comparison
fileNames = ["csv", "xsl", "abr", "zip"]
images_ext = ["jpeg", "jpg", "png", "gif", "bmp", "png", "cr2", "nef", "xmp", "img", "heif"]
adobe_ext = ["psd", "eps", "ai", "svg", "tiff"]
document_ext = ["pdf", "doc", "docx", "pages", "txt"]

# Function that makes folders and returns the path based on file types
# @param: filename      -> list formed from the filename that is dropped into Downloads
#                          list is split at . giving you the form ["filename", "EXTENSION"]
# Returns an integer that relates to the type of file
def get_file_type(filename):
    ext = filename.pop()
    if ext.lower() in images_ext:     # Checking to see if it is an image
        return 1
    elif ext.lower() in document_ext: # Checking to see if it is a document
        return 2
    elif ext.lower() == fileNames[0].lower() or ext.lower() == fileNames[1].lower(): # Checking if excel
        return 3
    elif ext.lower() in adobe_ext:    # Checking to see if it is an adobe file
        return 4
    elif ext.lower() == fileNames[2].lower(): # Checking if ABR
        return 5
    elif ext.lower() == fileNames[3].lower(): # Checking if ZIP
        return 6
    else:
        return 7

# The folder that you want to watch
folder_to_track = '/Users/kilgorez/Downloads'
# The main folder that you want to sort into
desktop = '/Users/kilgorez/SortedDownloads'
# If the file doesn't exist, create it. Otherwise, do nothing
try:
    os.mkdir(desktop)
    print("Making desktop folder")
except FileExistsError:
    pass

list = os.listdir(folder_to_track)
num_files = len(list)

for filename in list:
    # src = file to move
    src = folder_to_track + "/" + filename
    # spliting src into list, split at every .
    fileType = src.split('.')
    file_integer = get_file_type(fileType)
    print("Currently moving the file: ", filename)

    # Getting the date from datatime
    date = datetime.datetime.now()
    day = date.strftime("%d")
    month = date.strftime("%B")
    year = date.strftime("%Y")
    # Creating path for the day
    day_folder = desktop + "/" + month + "_" + day + "_" + year
    try:
        os.mkdir(day_folder)
    except FileExistsError:
        pass

    # Calling makeFolder, which will make the folder depending
    # on the file type
    folder_destination = makeFolder(file_integer, day_folder)

    # Specifying where the files new destination is going to be
    new_destination = folder_destination + "/" + filename

    # Trying to make the folder if not there
    # Making folder if not there
    # Moving to that folder no matter what
    try:
        os.mkdir(folder_destination)
        os.rename(src, new_destination)
    except FileExistsError:
        os.rename(src, new_destination)

    # If the file is a ZIP file, uncompress the file, and move folder
    # of uncompressed files to the ZIP_Compressed folder
    if(file_integer == 6):
        zipName = filename.split('.')
        with ZipFile(new_destination, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(folder_destination + "/" + zipName[0])

print("Thank you! Your downloads have been sorted")
