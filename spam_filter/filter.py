import os
import corpus
import email_text_analysis as e_t_a
import second_text_analysis as s_t_a
from utils import read_classification_from_file
from quality import compute_quality_for_corpus


class MyFilter():
    """
    Our filter looks for suspicious phrases and symbols in a file
    """
    def __init__(self):
        self.second_analyser = s_t_a.Analyser()
        #Could be changed when training
        self.tiping_point = 0
        self.koefs = [1] * 4            #Must be set manually set to be the length of points we get
        self.koef_margin = 0.05         #How much will we move the koef on a succesful or unsuccesful classification

        self.spam_to_all = 0.5          #When training is set to (number of spam emails)/(number of all emails)

    def train(self, path_to_train_folder: str) -> None:
        """
        Filter goes through the data two times, after each itteration getting a bit better
        """
        self.path_to_train_folder = path_to_train_folder
        self.truth_file = os.path.join(path_to_train_folder, "!truth.txt")
        self.classifications = read_classification_from_file(self.truth_file)

        #Training second analyser
        self.second_analyser.setup_properties(self.path_to_train_folder, self.classifications)
        
        train_results = self.try_train_settings(path_to_train_folder)
        resulting_points = train_results[0]
        average_points = train_results[1]
        ok_average_points = train_results[2]
        
        truth_file = os.path.join(self.path_to_train_folder, "!truth.txt")
        truth_dict = read_classification_from_file(truth_file)

        self.spam_to_all = self.calculate_spam_to_all(truth_dict)
        self.tiping_point = self.spam_to_all*(ok_average_points - average_points)

        
        for index, key in enumerate(truth_dict):
            for idx, number in enumerate(resulting_points[index]):
                if number < 0:      #NOT TIPPING POINT, these are individual points from each category
                    if truth_dict[key] == 'SPAM':     #True positive
                        self.koefs[idx] += self.koef_margin * 4
                    else:                   #False positive
                        self.koefs[idx] -= self.koef_margin * 3
                if number > 0:
                    if truth_dict[key] == 'SPAM':     #False positive
                        self.koefs[idx] -= self.koef_margin * 2
                    else:                   #True positive
                        self.koefs[idx] += self.koef_margin * 4
        
        for i in range(len(self.koefs)):
            if self.koefs[i] < 0.2:
                self.koefs[i] = 0.2

        train_results = self.try_train_settings(path_to_train_folder)
        resulting_points = train_results[0]
        average_points = train_results[1]
        ok_average_points = train_results[2]

        #Changing the tiping point at last
        self.tiping_point = self.spam_to_all*(ok_average_points - average_points)

        #Uncomment to see the progress
        #train_results = self.try_train_settings(path_to_train_folder)

    def test(self, path_to_folder: str) -> None:
        self.path_to_folder = path_to_folder

        predictions = {}

        for filename in self.load_emails(self.path_to_folder):
            path_to_file = os.path.join(self.path_to_folder, filename)

            predictions[filename] = self.get_prediction(path_to_file)
            print(f"Prediction for {filename}: {predictions[filename]}")

        # Write predictions to file
        prediction_file = os.path.join(self.path_to_folder, "!prediction.txt")
        self.write_predictions_to_file(predictions, prediction_file)

    def try_train_settings(self, path_to_file):
        """
        Tries classificating the train file, returns resulting points and spam and ok averages
        """
        predictions = {}

        spam_num = 0
        average_points = 0
        ok_num = 0
        ok_average_points = 0

        resulting_points = [] #A list of lists of points from evaluating each email

        for filename in self.load_emails(self.path_to_train_folder):
            path_to_file = os.path.join(self.path_to_train_folder, filename)

            classification = self.classifications.get(filename, "UNKNOWN")
            #print(f"Email: {filename} is classified as: {classification}")

            resulting_points.append(self.get_points(path_to_file))

            points = sum(self.get_points(path_to_file))

            predictions[filename] = self.get_prediction(path_to_file)
            if classification == "SPAM":
                spam_num += 1
                average_points += points

            if classification == "OK":
                ok_num += 1
                ok_average_points += points

        prediction_file = os.path.join(
            self.path_to_train_folder, "!prediction.txt")
        self.write_predictions_to_file(predictions, prediction_file)

        self.quality = self.get_quality()
        print(f"\nQuality before setting koefs: {self.quality:.4f}")

        if spam_num != 0:
            average_points = average_points / spam_num
        else: 
            average_points = 0

        if ok_num != 0:
            ok_average_points = ok_average_points / ok_num
        else: 
            ok_average_points = 0

        print(f"Average spam score: {average_points}")
        print(f"Average ok score: {ok_average_points}")

        return [resulting_points, average_points, ok_average_points]


    def write_predictions_to_file(self, predictions: dict, filename: str) -> None:
        # Write predictions to a file
        file_prediction = open(filename, 'w', encoding='UTF-8')
        for email_file, classification in predictions.items():
            file_prediction.write(f"{email_file} {classification}\n")

    def load_emails(self, emails_folder):
        file = corpus.Corpus(emails_folder)
        count = 0
        for filename in file.emails():
            yield filename
            count += 1
        print(f"Finished: {count} files processed")

    def get_quality(self):
        return compute_quality_for_corpus(self.path_to_train_folder)
    
    def get_points(self, path_to_file):
        """
        Returns a list of points from each test
        """
        analyzer = e_t_a.AnalyseText(path_to_file)
        special_characters_points = analyzer.count_special_characters()
        money_mention_points = analyzer.count_money_mention()

        sta_results = self.second_analyser.results(path_to_file)
        capital_points = sta_results[0]
        html_points = sta_results[1]

        points = [
                    special_characters_points * self.koefs[0], 
                    money_mention_points  * self.koefs[1],
                    html_points  * self.koefs[2],
                    capital_points * self.koefs[3]
                  ]

        return points
    
    def calculate_spam_to_all(self, tr_dict):
        all = 0
        spam = 0
        for key in tr_dict:
            all += 1
            if tr_dict[key] == "SPAM":
                spam += 1

        return (spam/all)


    def get_prediction(self, path_to_file):
        """
        Returns OK or SPAM
        """
        overall_points = sum(self.get_points(path_to_file))

        if overall_points < self.tiping_point:
            return 'SPAM'
        result = 'OK'

        return result


if __name__ == "__main__":
    filter = MyFilter()
    test_dir = 'C:/Users/42073/Documents/Škola/Semestr-1/Reseni-Problemu-a-Hry/Home-Works/Spam_Filter_Project/spam_filter/test_files/1'
    sec_test_dir = "E:/School/1"
    quality = filter.train(sec_test_dir)
    #quality = filter.test(sec_test_dir)
    print(f"Quality score: {quality}")
