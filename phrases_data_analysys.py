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

    #This is the function that we can use in our filter
    def count_in_file(self, filename, phrase):
        with open(self.data_dir + filename, "r", encoding='utf-8') as file:
            content = file.read()
            count = content.count(phrase)
        return count

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
            print("on " + str(i) + " all is " + str(all_in_interval[i])
                  + " and spam is " + str(spam_in_interval[i]))
            if all_in_interval[i] == 0:
                #To distinquish empty and all hamm
                ratio[i] = -20
                continue
            if all_in_interval[i] - spam_in_interval[i] == 0:
                ratio[i] = 100
                continue
            ratio[i] = (spam_in_interval[i] / all_in_interval[i]) * 100

        plt.scatter(interval_set, ratio)

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
    
    #Phrases list to choose     - html_phrases, link_ends, file_types
    #for phrase in html_phrases:
    #   analyze.create_graph(5, tr_dict, phrase)


    #If you want to try just one specific phrase
    phrase = "<img"
    
    analyze.create_graph(5, tr_dict, phrase)
