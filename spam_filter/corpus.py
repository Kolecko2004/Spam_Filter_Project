import os

class Corpus:
    def __init__(self, path_to_folder: str) -> None:
        self.path_to_folder = path_to_folder
    
    def get_files(self):
        self.files_list = os.listdir(self.path_to_folder)
        self.filter_files()
        
    def emails(self): 
        self.get_files()
        for filename in self.files_list:
            filepath = os.path.join(self.path_to_folder, filename)
            file = open(filepath, mode='r', encoding='UTF-8')
            body = file.read()
            yield filename, body
            file.close()
        
    def filter_files(self):
        delete_list = []
        for file in self.files_list:
            if file[0] == '!':
                delete_list.append(file)
                
        for bad_file in delete_list:
            self.files_list.remove(bad_file)
        
if __name__ == "__main__":
    i = Corpus('C:/Users/42073/Documents/Škola/Semestr-1/Reseni-Problemu-a-Hry/Home-Works/Spam_Filter_Project/spam_filter/test_files/1')
    count = 0
    for filename, body in i.emails():
        print(f'FILENAME: {filename}')
        # print(f'MESSAGE: {body.encode()}')
        print('--------------------------------------')
        count += 1
    print(f"Finished: {count} files processed")