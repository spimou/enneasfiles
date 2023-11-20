import os
from posixpath import splitext
import shutil
from reportlab.pdfgen.canvas import Canvas

 
subfolderNames = ['00', '01', '02']
imageExtentions  = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
files = []
folder_path = "./files"
 

def get_files_and_create_folders():
    try:
        global files
        # put all files in global lsit
        files = os.listdir(folder_path)   
        print(f"folder contains {len(files)} files")

        # create subfloders based on subfolderNames list - if they dont exist already
        for i in subfolderNames: 
            new_folder_path = os.path.join(folder_path, i)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path) 

        print(f"subfolders {subfolderNames} created")
        distribute_files_in_subfolders()

    except OSError as e:
        print(f"error creating  folders: {e}")
        
        
def distribute_files_in_subfolders():
    try:

        # for every subfolder and every file in global files list
        for subfolderName in subfolderNames: 
            for file in files: 
                # form path for file being in parent folder
                filepath = os.path.join(folder_path, file)
                # form path for subfolder 
                folderpath = os.path.join(folder_path, subfolderName) 
                # if it is a file and starts with the same chars as subfolder, move it there
                if os.path.isfile(filepath):
                     if file.startswith(subfolderName): 
                         shutil.move(filepath, folderpath )

        print(f"files successfully distributed to subfolders")
        put_images_in_pdf()


    except OSError as e:
        print(f"error distributing files to folders: {e}")


def put_images_in_pdf():
    try:

        global imageExtentions
        global folder_path 
 
        # set current folder as paernt
        os.chdir(folder_path)

        for subfolderName in subfolderNames:  
            #go to every subfolder
            os.chdir(subfolderName)

            #create an empty pdf
            canvasName = subfolderName+".pdf"
            canvas = Canvas(canvasName)
            canvas.drawString(0, 0, " ") 

            #for the files inside the subfolder
            files = os.listdir('.')   
            for file in files:
                #check if they are files and if they are images
                if os.path.isfile(file):
                    file_name, file_extension = splitext(file)
                    if file_extension in imageExtentions: 
                        #set image path to be used by canvas drawInlineImage, set place in page, width height of image
                        img_path = os.path.join(os.getcwd(), file)   
                        canvas.drawInlineImage(img_path, 0, 0, width=200, height=200)
                        #after drawing the image, create a new page in pdf
                        canvas.showPage()
                        print(f"image {file} copied in pdf {subfolderName}")
            #save pdf and go to parent folder, so it can go to subfolder again
                        
            canvas.save()
            os.chdir('..') 

            

    except OSError as e:
        print(f"error getting images in subfolders : {e}")

get_files_and_create_folders()

 