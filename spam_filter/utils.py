def read_classification_from_file(filename):
    filename = filename
    email_OK_SPAM = {}
    
    main_file = open(filename, mode='r', encoding='UTF-8')
    whole_text = main_file.read()
    
    strings = whole_text.split()
    
    for i in range(0, len(strings), 2):
        email_OK_SPAM[strings[i]] =  strings[i + 1]
        
    return email_OK_SPAM
    
if __name__ == "__main__":
    print(read_classification_from_file('hello.txt'))