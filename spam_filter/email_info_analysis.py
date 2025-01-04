import os
import corpus
from utils import read_classification_from_file

class EmailInfoAnalysis:
    def main(self, path_to_folder: str) -> None:

        days_of_week = ['; Mon, ', '; Tue, ', '; Wed, ',
                        '; Thu, ', '; Fri, ', '; Sat, ', '; Sun, ']

        self.path_to_folder = path_to_folder

        truth_file = os.path.join(self.path_to_folder, "!truth.txt")
        classifications = read_classification_from_file(truth_file)

        for filename in self.load_emails():
            path_to_file = os.path.join(self.path_to_folder, filename)
            file = open(path_to_file, mode='r', encoding='UTF-8')
            
            email_body = file.read()
            for day in days_of_week:
                if day in email_body:
                    day_idx = email_body.find(day)
                    newline_idx = email_body.find('\n', day_idx)
                    
                    the_info = email_body[day_idx:newline_idx]
                    
                    classification = classifications.get(filename, "UNKNOWN")
                    if classification == 'SPAM':
                        print(f'SPAM: {the_info}')

    def load_emails(self):
        test_file = corpus.Corpus(self.path_to_folder)
        count = 0
        for filename, body in test_file.emails():
            yield filename
            count += 1
        print(f"Finished: {count} files processed")

if __name__ == "__main__":
    idk = EmailInfoAnalysis()
    idk.main('C:/Users/42073/Documents/Škola/Semestr-1/Reseni-Problemu-a-Hry/Home-Works/Spam_Filter_Project/spam_filter/test_files/1')