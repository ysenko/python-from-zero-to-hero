from nltk.tokenize import RegexpTokenizer


def sentiment_dict(sentiment_data):
    """This method takes content from AFINN and returns dict with scores."""
    scores = {}
    for line in sentiment_data:
        term, score = line.split('\t')
        scores[term] = int(score)
    return scores


def tokenize(sentence):
    """Takes a sentence and returns a list of words."""
    tokenizer = RegexpTokenizer(r'https?:\/\/[\w.\/]+|\w+')
    return tokenizer.tokenize(sentence)


def sentiment_score(sentence, word_scores):
    """Calculates sentiment score for given sentence with a given set
       of word scores."""
    words = tokenize(sentence)
    score = 0
    for word in words:
        score += word_scores.get(word, 0)
    return score
