from collections import defaultdict
from math import log, inf

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    pos_list = []
    with open(path, 'r') as f:
        for sentence in f:
            pos = sentence.split()
            pos_list.append([tuple(line.split("=")) for line in pos])
    return pos_list

class Tagger(object):

    def __init__(self, sentences):
        self.tag = {'NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'DET', 'ADP', 'NUM', 'CONJ', 'PRT', '.', 'X'}
        self.log_pi = {}
        self.log_a = {}
        self.log_b = {}

        initial_tag_counts = defaultdict(int)
        transition_counts = {}
        emission_counts = {}
        a = 1e-10

        # initializing dictionaries for counting and probabilities
        for tag in self.tag:
            transition_counts[tag] = defaultdict(int)
            emission_counts[tag] = defaultdict(int)
            self.log_a[tag] = {}
            self.log_b[tag] = {}

        # find all unique words in corpus
        words = set()

        # calculating pi and b counts. Calculating transition counts within each sentence
        for sentence in sentences:
            pos = sentence[0][1]
            word = sentence[0][0]
            initial_tag_counts[pos] += 1
            emission_counts[pos][word] += 1
            # count number of unique words in corpus
            words.add(word)
            for index in range(1, len(sentence)):
                prev_pos = sentence[index - 1][1]
                word = sentence[index][0]
                pos = sentence[index][1]
                transition_counts[prev_pos][pos] += 1
                emission_counts[pos][word] += 1
                words.add(word)

        # calculating transition counts between sentences
        for index in range(1, len(sentences)):
            length_prev = len(sentences[index - 1])
            end_tag_prev = sentences[index - 1][length_prev - 1][1]
            start_tag_current = sentences[index][0][1]
            transition_counts[end_tag_prev][start_tag_current] += 1

        # pi probabilities
        pi_denominator = len(sentences) + (a * len(self.tag))
        for tag in self.tag:
            self.log_pi[tag] = log((initial_tag_counts[tag] + a)/pi_denominator)

        # transition totals for a probabilities
        transition_totals = defaultdict(int)
        for tag in self.tag:
            for tag2 in self.tag:
                transition_totals[tag] += transition_counts[tag][tag2]

        # a probabilities with smoothing
        for tag in self.tag:
            a_denominator = transition_totals[tag] + (a * len(transition_counts.keys()))
            for tag2 in self.tag:
                self.log_a[tag][tag2] = log((transition_counts[tag][tag2] + a)/a_denominator)

        # emission totals for b probabilities
        emission_totals = defaultdict(int)
        for tag in self.tag:
            for word in emission_counts[tag]:
                emission_totals[tag] += emission_counts[tag][word]

        # count of all unique words for laplace smoothing
        num_unique_words = len(words)

        # b probabilities with smoothing and unknown token
        for tag in self.tag:
            b_denominator = emission_totals[tag] + (a * (num_unique_words + 1))
            self.log_b[tag]["<UNK>"] = log(a/b_denominator)
            for word in emission_counts[tag]:
                self.log_b[tag][word] = log((emission_counts[tag][word] + a)/b_denominator)

    def most_probable_tags(self, tokens):
        tags = []
        for token in tokens:
            max_prob = -inf
            max_prob_tag = None
            for tag in self.tag:
                if token in self.log_b[tag].keys():
                    if self.log_b[tag][token] > max_prob:
                        max_prob = self.log_b[tag][token]
                        max_prob_tag = tag
                else:
                    if self.log_b[tag]['<UNK>'] > max_prob:
                        max_prob = self.log_b[tag]['<UNK>']
                        max_prob_tag = tag
            tags.append(max_prob_tag)
        return tags

    def viterbi_tags(self, tokens):
        if not tokens:
            return tokens
        delta = {0: {}}
        phi = {}
        for tag in self.tag:
            if tokens[0] in self.log_b[tag].keys():
                delta[0][tag] = (self.log_pi[tag]) + (self.log_b[tag][tokens[0]])
            else:
                delta[0][tag] = (self.log_pi[tag]) + (self.log_b[tag]['<UNK>'])
        for index in range(1, len(tokens)):
            delta[index] = {}
            phi[index] = {}
            for current_tag in self.tag:
                max_prob = -inf
                max_prob_tag = None
                if tokens[index] in self.log_b[current_tag].keys():
                    word = tokens[index]
                else:
                    word = '<UNK>'
                for prev_tag in self.tag:
                    prob = delta[index - 1][prev_tag] + (self.log_a[prev_tag][current_tag])
                    if prob > max_prob:
                        max_prob = prob
                        max_prob_tag = prev_tag
                delta[index][current_tag] = max_prob + (self.log_b[current_tag][word])
                phi[index][current_tag] = max_prob_tag

        path_list = []
        max_prob = -inf
        max_prob_tag = None
        for tag in self.tag:
            if delta[len(tokens) - 1][tag] > max_prob:
                max_prob = delta[len(tokens) - 1][tag]
                max_prob_tag = tag

        tag = max_prob_tag
        for index in range(len(tokens) - 1, 0, -1):
            path_list.append(tag)
            tag = phi[index][tag]
        path_list.append(tag)
        return list(reversed(path_list))

