class TrainingCorpus:
    def get_class(self, filename):
        self.filename = filename
        self.file = open(self.filename, mode='r', encoding='UTF-8')
        self.body = self.file.read()
        
        self.is_spam()
        self.is_ham()
        
        self.file.close()
        return 'OK'
    
    def is_spam(self):
        spam_points = 0
        
        spam_points += self.char_analyzation()
        
        print(spam_points)
        return spam_points
    
    def is_ham(self):
        ham_points = 0

        print(ham_points)
        return ham_points
    
    def char_analyzation(self):
        points = 0
        if '!' in self.body:
            points += self.body.count('!')
            
        if '?' in self.body:
            points += self.body.count('?')
            
        if '%' in self.body:
            points += self.body.count('%')
            
        if '*' in self.body:
            points += self.body.count('*')
            
        return points
        
if __name__ == "__main__":
    i = TrainingCorpus()
    i.get_class('/Users/42073/Documents/Škola/Semestr-1/Reseni-Problemu-a-Hry/Home-Works/spam_filter/test_files/email_MFuFZAQg.txt')