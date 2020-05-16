import email
from collections import defaultdict
import math
import os

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    tokens = []
    file = open(email_path)
    message = email.message_from_file(file)
    for line in email.iterators.body_line_iterator(message):
        line = line.strip()
        tokens.extend(line.split())
    return tokens

def log_probs(email_paths, smoothing):
    counts = defaultdict(int)
    log_prob = {}
    total_count = 0
    for path in email_paths:
        for token in load_tokens(path):
            counts[token] += 1
            total_count += 1
    denominator = total_count + smoothing * (len(counts.keys()) + 1)
    for word in counts.keys():
        log_prob[word] = math.log((counts[word] + smoothing)/denominator)
    log_prob["<UNK>"] = math.log(smoothing/denominator)
    return log_prob


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_files = [spam_dir + "/" + file for file in os.listdir(spam_dir)]
        ham_files = [ham_dir + "/" + file for file in os.listdir(ham_dir)]
        self.spam_log_prob = log_probs(spam_files, smoothing)
        self.ham_log_prob = log_probs(ham_files, smoothing)

        denominator = len(spam_files) + len(ham_files)
        self.prob_spam = math.log(len(spam_files)/denominator)
        self.prob_not_spam = math.log(len(ham_files)/denominator)
    
    def is_spam(self, email_path):
        spam_prob = self.prob_spam
        ham_prob = self.prob_not_spam

        email_tokens = load_tokens(email_path)
        counts = defaultdict(int)
        for token in email_tokens:
            counts[token] += 1

        for word in counts.keys():
            if word in self.spam_log_prob:
                spam_prob += counts[word] * self.spam_log_prob[word]
            else:
                spam_prob += counts[word] * self.spam_log_prob["<UNK>"]
            if word in self.ham_log_prob:
                ham_prob += counts[word] * self.ham_log_prob[word]
            else:
                ham_prob += counts[word] * self.ham_log_prob["<UNK>"]

        return spam_prob > ham_prob

    def most_indicative_spam(self, n):
        indicative = []
        for word in self.spam_log_prob.keys():
            if word in self.ham_log_prob.keys():
                prob = self.spam_log_prob[word] - math.log(math.exp(self.prob_spam)*math.exp(self.spam_log_prob[word]) +
                                                        math.exp(self.prob_not_spam)*math.exp(self.ham_log_prob[word]))
                indicative.append((word, prob))
        indicative.sort(key=lambda prob_tuple: prob_tuple[1], reverse=True)

        return [indicative[i][0] for i in range(n)]

    def most_indicative_ham(self, n):
        indicative = []
        for word in self.ham_log_prob.keys():
            if word in self.spam_log_prob.keys():
                prob = self.ham_log_prob[word] - math.log(math.exp(self.prob_spam) * math.exp(self.spam_log_prob[word]) +
                    math.exp(self.prob_not_spam) * math.exp(self.ham_log_prob[word]))
                indicative.append((word, prob))
        indicative.sort(key=lambda prob_tuple: prob_tuple[1], reverse=True)

        return [indicative[i][0] for i in range(n)]

