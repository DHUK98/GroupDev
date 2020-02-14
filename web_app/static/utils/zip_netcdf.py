from zipfile import ZipFile

def zip_folder(filepath):


    with ZipFile('export.zip', 'w') as zipObj:
        # Add multiple files to the zip
        zipObj.write('test.nc')
        zipObj.write('test2.nc')


if __name__ == "__main__":
    zip_folder("")