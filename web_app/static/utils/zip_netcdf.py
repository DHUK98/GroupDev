import os
from os import listdir

from zipfile import ZipFile

def zip_netcdf_exports():

    # create a ZipFile object
    with ZipFile('../netcdf_export/download.zip', 'w') as zipObj:
        # Iterate over all the files in directory

        for folderName, subfolders, filenames in os.walk("..\\netcdf_export\\"):

            for filename in filenames:

                if filename != "download.zip":
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)

                    # Add file to zip
                    print("Zipping: " + str(filePath))
                    zipObj.write(filePath)


def delete_nc_exports():
    folder_path = "../netcdf_export/"

    for file_name in listdir(folder_path):
        if file_name.endswith('.nc'):
            os.remove(folder_path + file_name)


if __name__ == "__main__":
    zip_netcdf_exports()
    delete_nc_exports()