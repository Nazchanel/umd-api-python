from src.professors import Professors

class test:
    def __init__(self):
        self.professors = Professors()
    
if __name__ == '__main__':
    api = test()
    try:
        listO = api.professors.list_professors(name = "Raluca Rosca")
        for prof in listO:
            print(prof) 
    except Exception as e:
        print(f"An error occurred: {e}")
