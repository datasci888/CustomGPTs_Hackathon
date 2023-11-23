

def read_file(file_path : str) -> str :
    with open(file_path,'r') as file :
        file_content = file.read()
        return file_content