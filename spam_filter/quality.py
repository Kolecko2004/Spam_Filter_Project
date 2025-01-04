import utils
import confmat
import os


def quality_score(tp, tn, fp, fn):
    result = (tp + tn) / (tp + tn + 10 * fp + fn)
    return result


def compute_quality_for_corpus(corpus_dir):
    truth_file = os.path.join(corpus_dir, "!truth.txt")
    prediction_file = os.path.join(corpus_dir, "!prediction.txt")

    truth_dict = utils.read_classification_from_file(truth_file)
    pred_dict = utils.read_classification_from_file(prediction_file)

    conf_matrix = confmat.BinaryConfusionMatrix(pos_tag="SPAM", neg_tag="OK")
    conf_matrix.compute_from_dicts(truth_dict, pred_dict)
    
    score = quality_score(
        tp=conf_matrix.tp,
        tn=conf_matrix.tn,
        fp=conf_matrix.fp,
        fn=conf_matrix.fn
    )

    return score
