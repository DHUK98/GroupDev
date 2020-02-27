import os
from os import listdir
from zipfile import ZipFile


def zip_netcdf_exports():
    print("zip_netcdf.py function")

    # create a ZipFile object
    with ZipFile('static/netcdf_export/download.zip', 'w') as zipObj:

        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk("static\\netcdf_export\\"):

            for filename in filenames:

                if filename != "download.zip":
                    # concatenate complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)

                    # Add file to zip
                    print("Zipping: " + str(filePath))
                    zipObj.write(filePath)


def delete_nc_exports():
    folder_path = "static/netcdf_export/"

    for file_name in listdir(folder_path):
        if file_name.endswith('.nc'):
            print("About to delete: " + folder_path + file_name)
            os.remove(folder_path + file_name)
            print("Deleted: " + str(file_name))


if __name__ == "__main__":
    zip_netcdf_exports()
    delete_nc_exports()