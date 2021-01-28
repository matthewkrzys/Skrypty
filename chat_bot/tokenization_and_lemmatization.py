
from nltk.stem import WordNetLemmatizer


wordnet_lemmatizer = WordNetLemmatizer()

print(wordnet_lemmatizer.lemmatize('do',pos='v'))
print(wordnet_lemmatizer.lemmatize('does',pos='v'))
print(wordnet_lemmatizer.lemmatize('doing',pos='v'))