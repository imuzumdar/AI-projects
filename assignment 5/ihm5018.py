import string
import re
from collections import defaultdict
import math
import random

############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    # tokens = re.findall(r"\w+|[{}]".format(string.punctuation), text, re.UNICODE)
    space_between_puncutation = re.sub('([%s])'%re.escape(string.punctuation), r' \1 ', text)
    return space_between_puncutation.split()

def ngrams(n, tokens):
    tokens = (n - 1)*['<START>'] + tokens + ['<END>']
    ngrams = []
    for index in range(n - 1, len(tokens)):
        n_1_tuple = tuple(tokens[j] for j in range(index - (n - 1), index))
        ngrams.append((n_1_tuple, tokens[index]))
    return ngrams

class NgramModel(object):

    def __init__(self, n):
        self.order = n
        # nested dictionary of each token and tokens that follow that context along w counts
        self.context_with_tokens = {}
        # dictionary counting number of appearances of all contexts
        self.context_counts = defaultdict(int)

    def update(self, sentence):
        tokens = tokenize(sentence)
        for context, token in ngrams(self.order, tokens):
            # storing contexts and corresponding tokens
            if context not in self.context_with_tokens.keys():
                self.context_with_tokens[context] = defaultdict(int)
            self.context_with_tokens[context][token] += 1

            # Tracking counts of each context
            self.context_counts[context] += 1

    def prob(self, context, token):
        if context in self.context_counts:
            return float(self.context_with_tokens[context][token])/float(self.context_counts[context])
        else:
            return "this is undefined"

    def random_token(self, context):
        r = random.random()
        tokens_for_context = sorted(self.context_with_tokens[context].keys())
        prob_sum = 0
        for index in range(len(tokens_for_context)):
            token_i = tokens_for_context[index]
            if prob_sum <= r < prob_sum + self.prob(context, token_i):
                return tokens_for_context[index]
            else:
                prob_sum += self.prob(context, token_i)
        return tokens_for_context[-1]

    def random_text(self, token_count):
        string_list = []
        context = tuple('<START>' for i in range(self.order - 1))
        if self.order > 1:
            for i in range(token_count):
                token = self.random_token(context)
                string_list.append(token)
                if token == '<END>':
                    context = tuple('<START>' for i in range(self.order - 1))
                else:
                    context = context[1:] + (token,)
            return " ".join(string_list)
        else:
            for i in range(token_count):
                string_list.append(self.random_token(context))
            return " ".join(string_list)

    def perplexity(self, sentence):
        tokens = tokenize(sentence)
        log_prob = 0
        for context, token in ngrams(self.order, tokens):
            if self.prob(context, token) != 0:
                log_prob += math.log(self.prob(context, token))
        return (1/math.exp(log_prob))**(1/(len(tokens) + 1))

def create_ngram_model(n, path):
    m = NgramModel(n)
    with open(path, 'r') as f:
        for sentence in f:
            m.update(sentence)
    return m

