import os

# Crea (en caso de no existir) el directorio de descargas de archivos CSV,JSON,PDF,XLSX y HTML
def create_download_folder(self,extension):
    local_path = os.path.dirname(__file__)
    sub_directories = ["downloads", extension]  # Lista de subdirectorios
    folder_path = os.path.join(local_path, *sub_directories)

    # Verificar si el directorio no existe antes de crearlo
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully")
        except OSError as e:
            raise OSError(f"Unable to create the directory '{folder_path}': {e}")
    return folder_path