
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import nltk

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))
account_activation_token = AppTokenGenerator()

# Download SentiWordNet data
nltk.download('wordnet')
nltk.download('sentiwordnet')
def analyze_sentiment(comment_text, threshold=0.1):
    total_score = 0
    total_words = 0

    for word in comment_text.split():
        synsets = wn.synsets(word)
        if synsets:
            # Get the first synset (most common meaning)
            synset = synsets[0]
            senti_synset = swn.senti_synset(synset.name())
            if senti_synset:
                total_score += senti_synset.pos_score() - senti_synset.neg_score()
                total_words += 1

    if total_words > 0:
        sentiment_score = total_score / total_words
        
        # Categorize sentiment based on the threshold
        if sentiment_score > threshold:
            return "Positive"
        elif sentiment_score < -threshold:
            return "Negative"
        else:
            return "Neutral"
    else:
        return "Neutral"  # Default sentiment if no words with synsets are found

