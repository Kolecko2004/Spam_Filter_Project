import os

#-10 spam
#10 ham

class Analyser():
    def __init__(self):
        self.spam_tag = "SPAM"

        #These are base values
        self.upp_spam_avrg = 630   
        self.upp_ham_avrg = 300

        self.html_bias = 1
        self.cap_html_bias = 1

        #Phrase lists
        self.html_phrases = ["<img",  "</a>",  "color=", "bgcolor=", "<br>", "</font>", "</td>", "</tr>"]
        self.cap_html_phrases = ["<IMG", "</A>", "COLOR=", "BGCOLOR=", "<BR>", "</FONT>", "</TD>", "</TR>"]
    
    def results(self, filename):
        """
        Expects absolute adress
        """
        self.filename = filename
        self.file = open(self.filename, mode='r', encoding='UTF-8')
        content = self.file.read()
        self.file.close()
        points = []
        points.append(self.uppercase_result(content))   
        points.append(self.html_result(content))

        return points
    
    #This part should be called in train
    def setup_properties(self, train_dir, truth_dict):
        """
        Truth dict should have absolute adresses
        """

        spam_BIG = 0
        spam_small = 0
        spam_i = 0
        ham_BIG = 0
        ham_small = 0
        ham_i = 0

        #For html bias
        already_touched = False
        cap_already_touched = False
        spam_touched = 0
        cap_spam_touched = 0
        ham_touched = 0
        cap_ham_touched = 0

        for filename in truth_dict:
            already_touched = False
            cap_already_touched = False
            final_filename = os.path.join(train_dir, filename)
            with open(final_filename, "r", encoding='utf-8') as file:
                content = file.read()
                uppercase_count = sum(1 for char in content if char.isupper())
                lowercase_count = sum(1 for char in content if char.islower())
                
            if truth_dict[filename] == self.spam_tag:
                spam_i += 1
                #We will divide once we have gathered all
                spam_BIG += uppercase_count
                spam_small += lowercase_count 

                for phrase in self.html_phrases:
                    if phrase in content and not already_touched:
                        spam_touched += 1
                        already_touched = True
                for phrase in self.cap_html_phrases:
                    if phrase in content and not cap_already_touched:
                        cap_spam_touched += 1
                        cap_already_touched = True
            else:
                ham_i += 1
                ham_BIG += uppercase_count
                ham_small += lowercase_count

                for phrase in self.html_phrases:
                    if phrase in content and not already_touched:
                        ham_touched += 1
                        already_touched = True
                for phrase in self.cap_html_phrases:
                    if phrase in content and not cap_already_touched:
                        cap_ham_touched += 1
                        cap_already_touched = True
        
        if spam_i != 0:
            spam_BIG = round(spam_BIG/spam_i, 2)
            spam_small = round(spam_small/spam_i, 2)
        if ham_i != 0:
            ham_BIG = round(ham_BIG/ham_i, 2)
            ham_small = round(ham_small/ham_i, 2)

        self.upp_ham_avrg = ham_BIG
        self.upp_spam_avrg = spam_BIG

        self.html_bias = 1 - (ham_touched/spam_touched)
        self.cap_html_bias = 1 - (cap_ham_touched/cap_spam_touched)

        #For unexpected behaviour
        if(ham_touched > spam_touched):
            self.html_bias = 0
            
        if(cap_ham_touched > cap_spam_touched):
            self.cap_html_bias = 0


    def uppercase_result(self, content):
        if(self.upp_ham_avrg >= self.upp_spam_avrg):
            #This seems like the safest option when the real data is not what we expected
            return 0

        upper = 0
        upper += sum(1 for char in content if char.isupper())

        
        #print(str(self.upp_ham_avrg) + " ham and spam avrg " + str(self.upp_spam_avrg))
        #print(str(upper))
        if(upper < self.upp_ham_avrg):
            #print("returned 5")
            #I never return ten because this isn't a sure way to know if it is ham
            return 5
        if(upper < self.upp_ham_avrg + (self.upp_spam_avrg - self.upp_ham_avrg)/2):
            #print(str(self.upp_ham_avrg + (self.upp_spam_avrg - self.upp_ham_avrg)/2))
            #print(str((upper - self.upp_ham_avrg)/(self.upp_ham_avrg + (self.upp_spam_avrg - self.upp_ham_avrg)/2 - self.upp_ham_avrg)))
            #Returns a number between 5 and -5 depending on where between ham_avrg and halfway to spam_avrg does upper stand
            return (5 - 15*(upper - self.upp_ham_avrg)/(self.upp_ham_avrg + (self.upp_spam_avrg - self.upp_ham_avrg)/2 - self.upp_ham_avrg))
        
        """
        Didn't use these because I didn't find a setting where they would be better than the current one
        if(upper < self.upp_spam_avrg):
            #Similarly
            #print(str((upper - (self.upp_ham_avrg + (self.upp_spam_avrg - self.upp_ham_avrg)/2))/(self.upp_spam_avrg-self.upp_ham_avrg)))
            return (-10 - 0*(upper - (self.upp_ham_avrg + (self.upp_spam_avrg - self.upp_ham_avrg)/2))/(self.upp_spam_avrg-self.upp_ham_avrg))
        if(self.upp_spam_avrg <= upper):
            #print("returned -10")
            ret = (-10 - 1*(upper - self.upp_spam_avrg))
            if (ret < -10):
                ret = -10
            return ret
        """

        return -10
    
    def html_result(self, content):
        #Unexpected situation
        if self.cap_html_bias == 0 or self.html_bias == 0:
            return 0
        
        ret = 5

        #The html bias is equal to 1 - (number of ham emails with html) divided by (number of spam emails with html)
        for phrase in self.html_phrases:
            if phrase in content:
                ret = -10 * self.html_bias
        for phrase in self.cap_html_phrases:
            if phrase in content:
                ret = -10 * self.cap_html_bias
              
        """
        Played with the idea of some complexity, but we just got lower accuracy on spams while always seeing hams as spams
        for phrase in self.html_phrases:
            count = content.count(phrase)
            if count > 0:
                ret -= 0.5
            if count > 10:
                ret -= 1.5
            if count > 20:
                ret -= 3
        for phrase in self.cap_html_phrases:
            count = content.count(phrase)
            if count > 0:
                ret -= 1
            if count > 10:
                ret -= 2
            if count > 20:
                ret -= 3
        """
        
        if ret < -10:
            ret = -10

        return ret
    
    #To test whether the analyzer gives credible results
    def test_this_analyzer(self, train_dir, truth_dict):
        #self.setup_properties(truth_dict)


        case_spam_avrg = 0
        case_spam_i = 0
        case_ham_avrg = 0
        case_ham_i = 0

        html_spam_avrg = 0
        html_spam_i = 0
        html_ham_avrg = 0
        html_ham_i = 0

        results = []

        #This is an inneficent method for a bulk of phrases
        for filename in truth_dict:
            results = self.results(train_dir + filename)
            if truth_dict[filename] == self.spam_tag:
                case_spam_i += 1
                case_spam_avrg += results[0]
                html_ret = results[1]
                #Option to filter out non html email
                #if(html_ret != 5):
                html_spam_avrg += html_ret
                html_spam_i += 1
            else:
                case_ham_i += 1
                case_ham_avrg += results[0]
                html_ret = results[1]
                #Option to filter out non html email
                #if(html_ret != 5):
                html_ham_avrg += html_ret
                html_ham_i += 1
            
        
        if case_spam_i != 0:
            case_spam_avrg = round(case_spam_avrg/case_spam_i, 2)
        if case_ham_i != 0:
            case_ham_avrg = round(case_ham_avrg/case_ham_i, 2)

        if html_spam_i != 0:
            html_spam_avrg = round(html_spam_avrg/html_spam_i, 2)
        if html_ham_i != 0:
            html_ham_avrg = round(html_ham_avrg/html_ham_i, 2)

        print("Average case results among spams is " + str(case_spam_avrg) + " and hams is " + str(case_ham_avrg))
        print("Average html results among spams is " + str(html_spam_avrg) + " and hams is " + str(html_ham_avrg) + " of " + str(html_ham_i))



if __name__ == "__main__":
    import utils
    #This is the absolute adress of where the emails are stored
    emails_dir = "E:/School/1/"
    
    #Doesnt need to be used if we are not saving the results
    result_dir = "E:/School/1/"

    truth_filename = emails_dir + "!truth.txt"

    tr_dict = utils.read_classification_from_file(truth_filename)

    it = Analyser()
    it.test_this_analyzer(emails_dir, tr_dict)
