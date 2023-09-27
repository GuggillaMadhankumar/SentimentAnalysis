# -*- coding: utf-8 -*-
"""SentimentAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iul96YYuaY0B0OU3wCIUbysPevpbsUlD

# In this project we are supposed to predict the sentiment of a given text, And predict if the text is positive, negative or neutral in nature.

### Importing necessary libraries.
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')

!pip install nlp-utils

!pip install contractions

import re
import nltk
import string
import nlp_utils
import collections
import contractions
import nlp_utils as nu
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize,sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer

import nltk
nltk.download('punkt')

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Loading data.
with open('TextAnalytics.txt','r') as f:
    text = f.read()

text
### The data is in the form of a text.

"""# Text Normalization

### Text normalization is the process of transforming a text into a canonical (standard) form. For example, the word “gooood” and “gud” can be transformed to “good”, its canonical form. Another example is mapping of near identical words such as “stopwords”, “stop-words” and “stop words” to just “stopwords”
"""

# splitting at ( \n ).
text=text.split('\n')
# Separating at new line using '\n'

# splitting at ( \t ).
corpus = [text]
for sent in text:
    corpus.append(sent.split('\t'))
# Splitting String by tab(\t)

letters_only = re.sub(r'[^a-zA-Z]',
                          " ",
                          str(corpus))
# Taking only letters

"""### Tokenization
What is Tokenization?
Tokenization is the process by which big quantity of text is divided into smaller parts called tokens.

Natural language processing is used for building applications such as Text classification, intelligent chatbot, sentimental analysis, language translation, etc. It becomes vital to understand the pattern in the text to achieve the above-stated purpose. These tokens are very useful for finding such patterns as well as is considered as a base step for stemming and lemmatization.

Sentence tokenization is the process of splitting text into individual sentences. ... It does this by looking for the types of textual constructs that confuse the tokenizer and replacing them with single words.
"""

# converting to lowercase.
letters_only=letters_only.lower()

token=nltk.sent_tokenize(letters_only)
token

"""### Alphanumeric characters"""

def num_dec_al(word):
    if word.isnumeric():
        return 'xxxxxx'
    elif word.isdecimal():
        return 'xxx...'
    elif word.isalpha():
        return word
    else:
        return 'xxxaaa'

def clean_nda(token):
    tokens = tokens = token.split()
    map_list = list(map(num_dec_al,tokens))
    return " ".join(map_list)

corpus_nda = list(map(clean_nda,token))

corpus_nda
### Alpha numeric characters and decimals have been replaced with characters

"""### Removing Contractions.
It is a process where words like isn't, didn't are expanded to is not did not.
isn't --> is not,
I'm --> I am,
they're --> they are,
shouldn't --> should not,
can't --> can not
"""

!pip install --upgrade contractions

import contractions
import re
import string
import nltk

corpus_nda
## corpus_nda with expanded contractions and converted to lowercase.

data = [corpus_nda]
for sent in text:
    data.append(sent.split('\t'))
# Separating at tab

data.append(sent.split('\n'))
# Separating at newline

data
# Cleaned text

df = pd.DataFrame(data)
## Saving the data into a dataframe.

df

df.drop([1,2,3,4,5,6],axis=1,inplace=True)
# dropping unnecessary columns.

df
# Resulting dataframe.

df= df.rename(columns={0: 'Text'})
# Renaming the column 0 as 'Text'

"""#### Final Dataset."""

df

"""### Rows 0,1 and 1000 and 1001 have repeated hence needs to be cleaned."""

df.drop(df.index[:1], inplace=True)
# row 1 has repeated so it is dropped.

df.drop(df.index[1000:], inplace=True)
# row 1000 has repeated aswell, so it is dropped.

df

"""### Removing additional characters present in the dataframe."""

## We can further see that there are still some special characters in the dataframe which have to be treated.
df.replace('\d+', '', regex=True, inplace=True)
df.replace(',', '', regex=True, inplace=True)
df.replace('br', '', regex=True, inplace=True)
df.replace('"', '', regex=True, inplace=True)
df.replace("'", '', regex=True, inplace=True)
df.replace('?', '', inplace=True)
df.replace("-", '', regex=True, inplace=True)
df.replace("*", '', inplace=True)
df.replace("***", '', inplace=True)
df.replace("< />", '', regex=True, inplace=True)

df['Text'] = df['Text'].str.strip('[')
df['Text'] = df['Text'].str.strip(']')
df['Text'] = df['Text'].str.strip(')')
df['Text'] = df['Text'].str.strip('(')
## Using the strip function in order to delete the special characters.

df

"""## Lemmatization of the text column

Lemmatization usually refers to doing things properly with the use of a vocabulary and morphological analysis of words, normally aiming to remove inflectional endings only and to return the base or dictionary form of a word, which is known as the lemma.
Lemmatization will generate the root form of the inflected words
"""

Text=df['Text']

token=nltk.sent_tokenize(str(token))
## Sentence tokenization

data = np.array(token)
## Saving token in form of array

nltk.download('stopwords')

stop = stopwords.words('english')
## Saving stopwords in stop

"""### Removing stopwords from the dataframe"""

text = data
text_tokens = word_tokenize(str(text))

tokens_without_sw = [word for word in text_tokens if not word in stop]

print(tokens_without_sw)
## Removing stopwords from the text and printing the words without stopwords

"""# Visualization"""

stopwords = set(stopwords.words("english"))
## Removing stopwords for wordcloud visualization

wordcloud = WordCloud(stopwords=stop, background_color="white", max_words=1000).generate(str(tokens_without_sw))
## WordCloud is a technique to show which words are the most frequent among the given text

"""### Visualizing the highest repeating words in the dataframe using  the wordcloud."""

rcParams['figure.figsize'] = 10, 20
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

"""### Counting the number of times a word has repeated through out the data."""

tokens_without_sw=(str(tokens_without_sw))

filtered_words = [word for word in tokens_without_sw.split() if word not in stopwords]
counted_words = collections.Counter(filtered_words)

words = []
counts = []
for letter, count in counted_words.most_common(10):
    words.append(letter)
    counts.append(count)
# Removing stopwords as creating two lists to display the words and their counts

counted_words.most_common(100) # the word 'movie' has repeated for 2081 times.

"""# Visualizing top 10 repeated/common words using bar graph."""

colors = cm.rainbow(np.linspace(0, 1, 10))
rcParams['figure.figsize'] = 20, 10

plt.title('Top words in the headlines vs their count')
plt.xlabel('Count')
plt.ylabel('Words')
plt.barh(words, counts, color=colors)

"""# Sentiment Analysis.

### Vader sentiment analysis is done in order to find if a given (Word) is positive, negative or  neutral in nature.
VADER belongs to a type of sentiment analysis that is based on lexicons of sentiment-related words. In this approach, each of the words in the lexicon is rated as to whether it is positive or negative, and in many cases, how positive or negative. Below you can see an excerpt from VADER’s lexicon, where more positive words have higher positive ratings and more negative words have lower negative ratings.
Vader sentiment analysis for a given (word) if positive, negative or  neutral in nature.
"""

!pip install vaderSentiment

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentence = tokens_without_sw
tokenized_sentence = nltk.word_tokenize(sentence)

sid = SentimentIntensityAnalyzer()
pos_word_list=[]
neu_word_list=[]
neg_word_list=[]

for word in tokenized_sentence:
    if (sid.polarity_scores(word)['compound']) >= 0.1:
        pos_word_list.append(word)
    elif (sid.polarity_scores(word)['compound']) <= -0.1:
        neg_word_list.append(word)
    else:
        neu_word_list.append(word)

print('Positive:',pos_word_list)
print('Neutral:',neu_word_list)
print('Negative:',neg_word_list)
# score = sid.polarity_scores(sentence)
# print('\nScores:', score)

#pos_word_list[:100]
#neg_word_list[:100]

"""### Top 100 Positive words."""

print(list(iter(pos_word_list[:100]))) # These are the top 100 positive words found in the dataset.

"""### Top 100 Negative words."""

print(list(iter(neg_word_list[:100]))) # These are the top 100 negative words found in the dataset.

"""## Vader sentiment analysis for a given (Sentence) if positive, negative or  neutral in nature."""

sid = SentimentIntensityAnalyzer()
for sentence in Text:
     print(sentence)

     ss = sid.polarity_scores(sentence)
     for k in ss:
         print('{0}: {1}, ' .format(k, ss[k]), end='')
     print()

"""### Converting all Polarity scores and sentences into a dataframe."""

analyzer = SentimentIntensityAnalyzer()
df['rating'] = Text.apply(analyzer.polarity_scores)
df=pd.concat([df.drop(['rating'], axis=1), df['rating'].apply(pd.Series)], axis=1)
### Creating a dataframe.

df.head()

"""## Arranging the dataset in descending order based on (Compound score) to find the most important sentence from the given data."""

imp_sent=df.sort_values(by='compound', ascending=False)
## arranging the compound column in descending order to find the best sentence.

imp_sent

print(df['Text'].iloc[410] ) # sentence with index 410 has the highest compound score
                             # and hence it is the most important sentence among all the sentences.

"""## Finding top positive sentence in the data."""

pos_sent=df.sort_values(by='pos', ascending=False)
## Arranging the dataframe by positive column in descending order to find the best postive sentence.

pos_sent

print(df['Text'].iloc[160] ) # sentence with index 160 has the highest positive score and is the most postive.

"""## Finding top negative sentence in the data."""

neg_sent=df.sort_values(by='neg', ascending=False)
## Arranging the dataframe by negative column in descending order to find the best negative sentence.

neg_sent

print(df['Text'].iloc[413] )# sentence with index 413 has the highest negative score and is the most negative sentence

sentences=df

"""## Giving threshold values to classify if a given sentence is positive, negative or neutral in nature."""

#Assigning score categories and logic
i = 0

predicted_value = [ ] #empty series to hold our predicted values

while(i<len(sentences)):
    if ((sentences.iloc[i]['compound'] >= 0.5)):
        predicted_value.append('positive')
        i = i+1
    elif ((sentences.iloc[i]['compound'] > 0) & (sentences.iloc[i]['compound'] < 0.5)):
        predicted_value.append('neutral')
        i = i+1
    elif ((sentences.iloc[i]['compound'] <= 0)):
        predicted_value.append('negative')
        i = i+1
## The threshold value will categorize if a given sentence is positive negative or neutral in nature.

predicted_value

"""### Adding the target or sentiment column to our data frame."""

df['Target'] = predicted_value
## A new column has been created called as 'Target' with sentiments assigned to a given text.

df.head()

"""### Removing/dropping the 'neg', 'neu', 'pos', and 'compound' columns."""

df.drop(['neg','neu','pos','compound'],axis=1,inplace=True)
## Dropping the neg, neu, pos, and compound columns.

df
## Final dataframe with sentiments.

df['Target'].value_counts()
### There are 568 positive, 369 negative and 63 neutral columns present in the dataset.

cat_cols=['Target']
le=LabelEncoder()
for i in cat_cols:
    df[i]=le.fit_transform(df[i])
df.dtypes
### Label Encoding the target column.

df['Target'].value_counts()
## Label encoded value_counts()

df

# Vectorizing training data.
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df['Text'])
Y = df['Target']
## Applying Tf-Idf vectorizer on the Text column.

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=40)
print(X_train.shape,X_test.shape,Y_train.shape,Y_test.shape)
### Splitting the dataset.

"""### Logistic Regression"""

log_reg = LogisticRegression().fit(X_train, Y_train)

#predict on train
train_preds = log_reg.predict(X_train)
#accuracy on train
print("Model accuracy on train is: ", accuracy_score(Y_train, train_preds))

#predict on test
test_preds = log_reg.predict(X_test)
#accuracy on test
print("Model accuracy on test is: ", accuracy_score(Y_test, test_preds))

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.metrics import accuracy_score, auc, confusion_matrix, roc_auc_score, roc_curve, recall_score

"""## Decision Tree Classifier"""

DT = DecisionTreeClassifier().fit(X,Y)

#predict on train
train_preds2 = DT.predict(X_train)
#accuracy on train
print("Model accuracy on train is: ", accuracy_score(Y_train, train_preds2))

#predict on test
test_preds2 = DT.predict(X_test)
#accuracy on test
print("Model accuracy on test is: ", accuracy_score(Y_test, test_preds2))
print('-'*50)

#Confusion matrix
print("confusion_matrix train is: ", confusion_matrix(Y_train, train_preds2))
print("confusion_matrix test is: ", confusion_matrix(Y_test, test_preds2))
print('Wrong predictions out of total')
print('-'*50)

# Wrong Predictions made.
print((Y_test !=test_preds2).sum(),'/',((Y_test == test_preds2).sum()+(Y_test != test_preds2).sum()))
print('-'*50)

# Kappa Score
print('KappaScore is: ', metrics.cohen_kappa_score(Y_test,test_preds2))

#fit the model on train data
RF=RandomForestClassifier().fit(X_train,Y_train)
#predict on train
train_preds3 = RF.predict(X_train)
#accuracy on train
print("Model accuracy on train is: ", accuracy_score(Y_train, train_preds3))

#predict on test
test_preds3 = RF.predict(X_test)
#accuracy on test
print("Model accuracy on test is: ", accuracy_score(Y_test, test_preds3))
print('-'*50)

#Confusion matrix
print("confusion_matrix train is: ", confusion_matrix(Y_train, train_preds3))
print("confusion_matrix test is: ", confusion_matrix(Y_test, test_preds3))
print('Wrong predictions out of total')
print('-'*50)

# Wrong Predictions made.
print((Y_test !=test_preds3).sum(),'/',((Y_test == test_preds3).sum()+(Y_test != test_preds3).sum()))
print('-'*50)

"""# Support Vector Machine"""

#fit the model on train data
SVM = SVC(kernel='linear')
SVM.fit(X_train, Y_train)

#predict on train
train_preds5 = SVM.predict(X_train)
#accuracy on train
print("Model accuracy on train is: ", accuracy_score(Y_train, train_preds5))

#predict on test
test_preds5 = SVM.predict(X_test)
#accuracy on test
print("Model accuracy on test is: ", accuracy_score(Y_test, test_preds5))
print('-'*50)

#Confusion matrix
print("confusion_matrix train is: ", confusion_matrix(Y_train, train_preds5))
print("confusion_matrix test is: ", confusion_matrix(Y_test, test_preds5))
print('Wrong predictions out of total')
print('-'*50)

# Wrong Predictions made.
print((Y_test !=test_preds5).sum(),'/',((Y_test == test_preds5).sum()+(Y_test != test_preds5).sum()))
print('-'*50)

#fit the model on train data
KNN = KNeighborsClassifier().fit(X_train,Y_train)
#predict on train
train_preds4 = KNN.predict(X_train)
#accuracy on train
print("Model accuracy on train is: ", accuracy_score(Y_train, train_preds4))

#predict on test
test_preds4 = KNN.predict(X_test)
#accuracy on test
print("Model accuracy on test is: ", accuracy_score(Y_test, test_preds4))
print('-'*50)

#Confusion matrix
print("confusion_matrix train is: ", confusion_matrix(Y_train, train_preds4))
print("confusion_matrix test is: ", confusion_matrix(Y_test, test_preds4))
print('Wrong predictions out of total')
print('-'*50)

# Wrong Predictions made.
print((Y_test !=test_preds4).sum(),'/',((Y_test == test_preds4).sum()+(Y_test != test_preds4).sum()))
print('-'*50)