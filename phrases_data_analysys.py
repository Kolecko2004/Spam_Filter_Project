import matplotlib.pyplot as plt
import utils

"""
First I am building a program to analyze the given data
"""

"""
I am including many html phrases which format the email
The end phrase ( </ > ) is more reliable
I have also noticed that some emails use these phrases capitalized
"""
html_phrases = ["<img", "<IMG", "</a>", "</A>", "color=", "COLOR=", "bgcolor=", "BGCOLOR=", "<br>", "<BR>", "</font>", "</FONT>", "</td>", "</TD>", "</tr>", "</TR>"]

"""
File types and link endings might also be interesting
"""
file_types = [".gif", ".img", ".png", ".mp4"]
link_ends = [".cz", ".com", ".news", ".gov"]

"""
By looking at the results we can see that when emails contain any 
"""

class AnalyzeData():
    def __init__(self, data_directory, result_directory, spam_tag):
        #Used if we want to save the results
        #But we can just cycle through
        self.result_dir = result_directory
        self.data_dir = data_directory
        self.spam_tag = spam_tag
        self.spam_rel = 1
        self.html_phrases = [
            "<img", "<IMG", "</a>", "</A>", "color=", "COLOR=", "bgcolor=", 
            "BGCOLOR=", "<br>", "<BR>", "</font>", "</FONT>", "</td>", "</TD>", 
            "</tr>", "</TR>"
            ]

    #This is the function that we can use in our filter
    def count_in_file(self, filename, phrase):
        with open(self.data_dir + filename, "r", encoding='utf-8') as file:
            content = file.read()
            count = content.count(phrase)
        return count

    #To figure out how many hams and spams the set has
    #The proportion needs to be taken into account when reading the data
    def spam_ham_emails(self, truth_dict):
        spams = 0
        for filename in truth_dict:
            if truth_dict[filename] == self.spam_tag:
                spams += 1

        print("In the set there is " + str(spams) + " spam emails out of " +
              str(len(truth_dict)) + " total emails")
        self.spam_rel = spams/len(truth_dict)

    def average_spam_ham_count(self, truth_dict, phrase):
        spam_avrg = 0
        spam_i = 0
        ham_avrg = 0
        ham_i = 0

        #This is an inneficent method for a bulk of phrases
        for filename in truth_dict:
            count = self.count_in_file(filename, phrase)
            if count == 0:
                continue
            if truth_dict[filename] == self.spam_tag:
                spam_i += 1
                #We will divide once we have gathered all
                spam_avrg += count
            else:
                ham_i += 1
                ham_avrg += count
        
        if spam_i != 0:
            spam_avrg = round(spam_avrg/spam_i, 2)
        if ham_i != 0:
            ham_avrg = round(ham_avrg/ham_i)

        print("For phrase " + phrase)
        print("Among spam it was found in " + str(spam_i) + 
                " files and the average among those is " + str(spam_avrg))
        print("Among ham it was found in " + str(ham_i) + 
                " files and the average among those is " + str(ham_avrg))

    def bulk_avrg_spam_ham_count(self, truth_dict, words):
        spam_avrg = [0] * len(words)
        spam_i = [0] * len(words)
        ham_avrg = [0] * len(words)
        ham_i = [0] * len(words)

        #By touched I mean where we found at least one words
        already_touched = False
        spam_touched = 0
        ham_touched = 0

        for filename in truth_dict:
            already_touched = False
            for n in range(len(words)):
                count = self.count_in_file(filename, words[n])
                if count == 0:
                    continue
                if truth_dict[filename] == self.spam_tag:
                    spam_i[n] += 1
                    #We will divide once we have gathered all
                    spam_avrg[n] += count
                    if not already_touched:
                        spam_touched += 1
                        already_touched = True
                else:
                    ham_i[n] += 1
                    ham_avrg[n] += count
                    if not already_touched:
                        ham_touched += 1
                        already_touched = True

        for n in range(len(words)):
            if spam_i[n] != 0:
                spam_avrg[n] = round(spam_avrg[n]/spam_i[n], 2)
            if ham_i[n] != 0:
                ham_avrg[n] = round(ham_avrg[n]/ham_i[n])

            print("For phrase " + words[n])
            print("Among spam it was found in " + str(spam_i[n]) + 
                    " files and the average among those is " + str(spam_avrg[n]))
            print("Among ham it was found in " + str(ham_i[n]) + 
                    " files and the average among those is " + str(ham_avrg[n]))

        print("Total spam touched is " + str(spam_touched)
                  + " and ham " + str(ham_touched))
        """
        When testing this on the first set I found that when using html_phrases
        we touch only 269 spam (out of 461 spam emails in the set) 
        and only 11 hams (which is nice)

        From this I conclude testing spam through html_phrases is realiable
        Theoretically catching up to a half of spams and only up to 5% hams
        """



    """
    Interval decides how many points there will be on the x axis (100/interval)
    If interval is 10, then it separates the emails into groups where the phrase
    was found in the given intervals -> 0 - 9, 10 - 19, 20 - 29, and so on
    And for each group it gives the ratio of spam/all_emails
    If no emails where found in an interval group, the ration is -20
    """
    def create_graph(self, interval, truth_dict, phrase):
        interval_set = [0] #will be on x axis
        current = interval
        
        while current < 100:
            interval_set.append(current)
            current += interval
        
        all_in_interval = [0] * len(interval_set)
        spam_in_interval = [0] * len(interval_set)
        ratio = [0] * len(interval_set)

        for filename in truth_dict:
            count = self.count_in_file(filename, phrase)
            for ri in range(len(interval_set)):
                i = len(interval_set) - ri - 1
                if interval_set[i] <= count:
                    all_in_interval[i] += 1
                    if truth_dict[filename] == self.spam_tag:
                        spam_in_interval[i] += 1
                    break

        for i in range(len(ratio)):
            #print("on " + str(i) + " all is " + str(all_in_interval[i])
            #      + " and spam is " + str(spam_in_interval[i]))
            if all_in_interval[i] == 0:
                #To distinquish empty and all hamm
                ratio[i] = -20
                continue
            if all_in_interval[i] - spam_in_interval[i] == 0:
                ratio[i] = 100
                continue
            ratio[i] = (spam_in_interval[i] / all_in_interval[i]) * 100

        plt.plot(interval_set, ratio)

        plt.xlabel(phrase + "- intervals")
        plt.ylabel("spam/all")

        plt.title('Graph of ' + phrase)
        
        #If we want to savre the results
        #plt/savefig(phrase + "_graph.svg", format="svg")
        plt.show()

        #Right now this is just kinda cool data
        #What will be more usefull is to find a number for each word
        #       that we would see as a tipping point for SPAM

if __name__ == "__main__":
    #This is the absolute adress of where the emails are stored
    emails_dir = "/home/leon/School/rph/spam_filtr/1/"
    
    #Doesnt need to be used if we are not saving the results
    result_dir = "/home/leon/School/rph/spam_filtr/data_analysys/"

    truth_filename = emails_dir + "!truth.txt"

    tr_dict = utils.read_classification_from_file(truth_filename)

    analyze = AnalyzeData(emails_dir, result_dir, "SPAM")

    analyze.spam_ham_emails(tr_dict)
    
    #Phrases list to choose     - html_phrases, link_ends, file_types
    #for phrase in html_phrases:
        #analyze.create_graph(1, tr_dict, phrase)
    
    analyze.bulk_avrg_spam_ham_count(tr_dict, html_phrases)

    #If you want to try just one specific phrase
    #phrase = ""
    #analyze.create_graph(5, tr_dict, phrase)
