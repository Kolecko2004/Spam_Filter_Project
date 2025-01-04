import os
import corpus
import count_special_character as csc
from utils import read_classification_from_file
from quality import compute_quality_for_corpus


class MyFilter():
    def train(self, path_to_train_folder: str) -> None:
        self.truth_file = os.path.join(path_to_train_folder, "!truth.txt")
        self.classifications = read_classification_from_file(self.truth_file)

    def test(self, path_to_folder: str) -> None:
        self.path_to_folder = path_to_folder

        predictions = {}
        
        for filename in self.load_emails():
            path_to_file = os.path.join(self.path_to_folder, filename)

            classification = self.classifications.get(filename, "UNKNOWN")
            print(f"Email: {filename} is classified as: {classification}")

            analyzer = csc.AnalyseText()
            prediction = analyzer.result(path_to_file)
            points = analyzer.overall_points()
            predictions[filename] = prediction

        # Write predictions to file
        prediction_file = os.path.join(self.path_to_folder, "!prediction.txt")
        self.write_predictions_to_file(predictions, prediction_file)

        # Calculate quality score
        quality = compute_quality_for_corpus(self.path_to_folder)
        print(f"\nFinal quality score: {quality:.4f}")
        # print(f"Average spam score: {average_points / spam_num}")

        return quality

    def write_predictions_to_file(self, predictions: dict, filename: str) -> None:
        # Write predictions to a file
        file_prediction = open(filename, 'w', encoding='UTF-8')
        for email_file, classification in predictions.items():
            file_prediction.write(f"{email_file} {classification}\n")

    def load_emails(self):
        test_file = corpus.Corpus(self.path_to_folder)
        count = 0
        for filename, body in test_file.emails():
            print(f'FILENAME: {filename}')
            print('--------------------------------------')
            yield filename
            count += 1
        print(f"Finished: {count} files processed")

    def get_quality(self):
        return compute_quality_for_corpus(self.path_to_folder)


if __name__ == "__main__":
    filter = MyFilter()
    test_dir = 'C:/Users/42073/Documents/Škola/Semestr-1/Reseni-Problemu-a-Hry/Home-Works/Spam_Filter_Project/spam_filter/test_files/1'
    quality = filter.train(test_dir)
    quality = filter.test(test_dir)
    print(f"Quality score: {quality}")
