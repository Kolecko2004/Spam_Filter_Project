import os
import corpus
import email_text_analysis as e_t_a
import second_text_analysis as s_t_a
from utils import read_classification_from_file
from quality import compute_quality_for_corpus


class MyFilter():
    def __init__(self):
        self.second_analyser = s_t_a.Analyser()
        #Could be changed when training
        self.tiping_point = 0

    def train(self, path_to_train_folder: str) -> None:
        self.path_to_train_folder = path_to_train_folder
        self.truth_file = os.path.join(path_to_train_folder, "!truth.txt")
        self.classifications = read_classification_from_file(self.truth_file)

        #Training second analyser
        self.second_analyser.setup_properties(self.path_to_train_folder, self.classifications)

        predictions = {}

        for filename in self.load_emails(self.path_to_train_folder):
            path_to_file = os.path.join(self.path_to_train_folder, filename)

            classification = self.classifications.get(filename, "UNKNOWN")
            print(f"Email: {filename} is classified as: {classification}")

            predictions[filename] = self.get_prediction(path_to_file)
            # if classification == "SPAM":
            #     spam_num += 1
            #     average_points += points

            # if classification == "OK":
            #     ok_num += 1
            #     ok_average_points += points

        prediction_file = os.path.join(
            self.path_to_train_folder, "!prediction.txt")
        self.write_predictions_to_file(predictions, prediction_file)

        self.quality = self.get_quality()
        print(f"\nFinal quality score: {self.quality:.4f}")
        # print(f"Average spam score: {average_points / spam_num}")
        # print(f"aAverage ok score: {ok_average_points / ok_num}")

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

    def get_prediction(self, path_to_file):
        analyzer = e_t_a.AnalyseText(path_to_file)
        special_characters_points = analyzer.count_special_characters()
        money_mention_points = analyzer.count_money_mention()

        sta_results = self.second_analyser.results(path_to_file)
        capital_points = sta_results[0]
        html_points = sta_results[1]

        overall_points = special_characters_points + money_mention_points + html_points + capital_points

        if overall_points < self.tiping_point:
            return 'SPAM'
        result = 'OK'

        return result


if __name__ == "__main__":
    filter = MyFilter()
    test_dir = 'C:/Users/42073/Documents/Škola/Semestr-1/Reseni-Problemu-a-Hry/Home-Works/Spam_Filter_Project/spam_filter/test_files/1'
    sec_test_dir = "E:/School/1/"
    quality = filter.train(sec_test_dir)
    quality = filter.test(sec_test_dir)
    print(f"Quality score: {quality}")
