import json

def copy_ngram_dict(parent_dict, new_dict = {}, trained_values = None):
    """
    Recurses through ngram style dictionary, casting each key/value
    to equivalent string in order to be parsed as json.
    """

    for k, v in parent_dict.items():

        if not isinstance(v, dict):
            new_dict[repr(k)] = v

            if isinstance(trained_values, list):
                trained_values[0] = trained_values[0] + 1

        else:
            new_dict[repr(k)] = {}
            copy_ngram_dict(parent_dict[k], new_dict[repr(k)], trained_values)

def ppGramJson(ngram):
    """
    Pretty print given ngram as json.
    """

    pdict = {}

    copy_ngram_dict(ngram, pdict)

    ppitem = json.dumps(
        pdict,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )

    return ppitem


class UnigramModel():

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable.

        This function is done for you.
        """

        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.

        This function is done for you.
        """

        return ppGramJson(self.nGramCounts)

    ###############################################################################
    # Begin Core >> FOR CORE IMPLEMENTION, DO NOT EDIT ABOVE OF THIS SECTION <<
    ###############################################################################

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary,
                  which is a dictionary of {string: integer} pairs.
                  For further explanation of UnigramModel's version of
                  self.nGramCounts, see the spec.
                  Returns self.nGramCounts
        """

        for i in range(0, len(text)):
            for j in range(0, len(text[i])):
                if text[i][j] == r'^::^' or text[i][j] == r"^:::^":
                    print("WHOA")
                    continue
                elif text[i][j] in self.nGramCounts:
                    self.nGramCounts[text[i][j]] = self.nGramCounts[text[i][j]] + 1
                else:
                    print("PAPPY")
                    self.nGramCounts[text[i][j]] = 1

                    # check following word in ngrams[i]
        return self.nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """
        if self.nGramCounts == {}:
            return False
        else:
            return True

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  UnigramModel sees as candidates, see the spec.
        """

        return self.nGramCounts


###############################################################################
# End Core
###############################################################################

###############################################################################
# Main
###############################################################################

# This is the code python runs when unigramModel.py is run as main
if __name__ == '__main__':
    # An example trainModel test case
    uni = UnigramModel()
    text = [['brown']]
    uni.trainModel(text)
    # Should print: { 'brown' : 1 }
    print(uni)

    text = [['the', 'brown', 'fox'], ['the', 'lazy', 'dog']]
    uni.trainModel(text)
    # Should print: { 'brown': 2, 'dog': 1, 'fox': 1, 'lazy': 1, 'the': 2 }
    print(uni)

    # An example trainingDataHasNGram test case
    uni = UnigramModel()
    sentence = "Eagles fly in the sky"
    print(uni.trainingDataHasNGram(sentence))  # should be False
    uni.trainModel(text)
    print(uni.trainingDataHasNGram(sentence))  # should be True