class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def as_dict(self):
        return {'tp': self.tp, 'tn': self.tn, 'fp': self.fp, 'fn': self.fn}

    def check_param_value(self, param):
        if param not in (self.pos_tag, self.neg_tag):
            raise ValueError('The parametr can be either %s or %s' %
                            (self.pos_tag, self.neg_tag))

    def update(self, truth, prediction):
        self.check_param_value(truth)
        self.check_param_value(prediction)

        if prediction == self.pos_tag:
            if truth == prediction:
                self.tp += 1
            else:
                self.fp += 1
        else:
            if truth == prediction:
                self.tn += 1
            else:
                self.fn += 1

    def compute_from_dicts(self, truth_dict, pred_dict):
        for key in truth_dict:
            self.update(truth_dict[key], pred_dict[key])


# DU dokoncit kro 4 a pokracovat dale
if __name__ == "__main__":
    cm1 = BinaryConfusionMatrix(pos_tag=True, neg_tag=False)
    print(cm1.as_dict())
    # {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
    cm1.update(True, True)
    print(cm1.as_dict())
    # {'tp': 1, 'tn': 0, 'fp': 0, 'fn': 0}
    truth_dict = {'em1': 'SPAM', 'em2': 'SPAM',
                  'em3': 'OK', 'em4': 'OK', 'em5': 'OK'}
    pred_dict = {'em1': 'SPAM', 'em2': 'OK',
                 'em3': 'OK', 'em4': 'SPAM', 'em5': 'SPAM'}
    cm2 = BinaryConfusionMatrix(pos_tag='SPAM', neg_tag='OK')
    cm2.compute_from_dicts(truth_dict, pred_dict)
    print(cm2.as_dict())
    # {'tp': 1, 'tn': 1, 'fp': 1, 'fn': 1}
    # truth OK filter SPAM == fp
    # # truth SPAM filter OK == fn
    # truth SPAM filter SPAM == tp
    # # truth OK filter SPAM == tn
