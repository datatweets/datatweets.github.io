---
layout: post
title:  "Natural Language Processing with Python"
date:   2024-07-03 01:54:02 +0430
categories: jekyll update
---

Python has some powerful tools that enable you to perform [natural language processing](https://en.wikipedia.org/wiki/Natural_language_processing) (NLP). In this tutorial, we'll explore how to do some basic NLP in Python.

## Looking at the Data

We'll be examining a dataset of submissions to [Hacker News](https://news.ycombinator.com) from 2006 to 2015. The data was sourced from [this repository](https://github.com/arnauddri/hn). Arnaud Drizard used the Hacker News API to scrape the data. We've randomly sampled `10000` rows and removed all extraneous columns, leaving us with four columns:

- `sublesson_time` -- when the story was submitted.
- `url` -- the base URL of the submission.
- `upvotes` -- number of upvotes the submission received.
- `headline` -- the headline of the submission.

We'll use the headlines to predict the number of upvotes. The data is stored in the `sublessons` variable.

## Natural Language Processing — First Steps

Our goal is to train a machine learning algorithm to predict the number of upvotes a headline might receive. However, machine learning algorithms only understand numbers, not words. So, how do we convert our headlines into something an algorithm can understand?

The first step is to create a bag of words matrix, which provides a numerical representation of which words appear in which headlines. To build this matrix, we first identify the unique words across all headlines. We then create a matrix where each row represents a headline and each column represents one of the unique words. The cells are filled with the number of times each word occurs in the corresponding headline. This matrix will have many zeros unless the vocabulary is mostly shared between the headlines.

```python
from collections import Counter
import pandas

headlines = [
    "PretzelBros, airbnb for people who like pretzels, raises $2 million",
    "Top 10 reasons why Go is better than whatever language you use.",
    "Why working at apple stole my soul (I still love it though)",
    "80 things I think you should do immediately if you use python.",
    "Show HN: carjack.me -- Uber meets GTA"
]

# Find all the unique words in the headlines.
unique_words = list(set(" ".join(headlines).split(" ")))

def make_matrix(headlines, vocab):
    matrix = []
    for headline in headlines:
        # Count each word in the headline, and make a dictionary.
        counter = Counter(headline)
        # Turn the dictionary into a matrix row using the vocab.
        row = [counter.get(w, 0) for w in vocab]
        matrix.append(row)
    df = pandas.DataFrame(matrix)
    df.columns = unique_words
    return df

print(make_matrix(headlines, unique_words))
```

Output:
```plaintext
   why  HN:  for  people  immediately  like  I  Go  80  meets  ...   my  who  
0    0    0    0       0            0     0  0   0   0      0  ...    0    0   
1    0    0    0       0            0     0  0   0   0      0  ...    0    0   
2    0    0    0       0            0     0  1   0   0      0  ...    0    0   
3    0    0    0       0            0     0  1   0   0      0  ...    0    0   
4    0    0    0       0            0     0  0   0   0      0  ...    0    0   

   PretzelBros,  whatever  language  do  $2  still  than  soul  
0             0         0         0   0   0      0     0     0  
1             0         0         0   0   0      0     0     0  
2             0         0         0   0   0      0     0     0  
3             0         0         0   0   0      0     0     0  
4             0         0         0   0   0      0     0     0  

[5 rows x 51 columns]
```

## Removing Punctuation

The matrix we've made is very sparse, meaning many of the values are zero because the headlines don't share much vocabulary. We can improve this by lowercasing every word and removing punctuation. This helps the parser recognize that words like `Why` and `why` or `use` and `use.` are the same.

```python
import re

# Lowercase, then replace any non-letter, space, or digit character in the headlines.
new_headlines = [re.sub(r'[^wsd]', '', h.lower()) for h in headlines]
# Replace sequences of whitespace with a space character.
new_headlines = [re.sub("s+", " ", h) for h in new_headlines]

unique_words = list(set(" ".join(new_headlines).split(" ")))

print(make_matrix(new_headlines, unique_words))
```

Output:
```plaintext
   2  why  top  hn  for  people  immediately  like  python  80  ...   should  
0  1    0    0   0    0       0            0     0       0   0  ...        0   
1  0    0    0   0    0       0            0     0       0   0  ...        0   
2  0    0    0   0    0       0            0     0       0   0  ...        0   
3  0    0    0   0    0       0            0     0       0   0  ...        0   
4  0    0    0   0    0       0            0     0       0   0  ...        0   

   my  who  go  whatever  language  do  still  than  soul  
0   0    0   0         0         0   0      0     0     0  
1   0    0   0         0         0   0      0     0     0  
2   0    0   0         0         0   0      0     0     0  
3   0    0   0         0         0   0      0     0     0  
4   0    0   0         0         0   0      0     0     0  

[5 rows x 47 columns]
```

## Removing Stopwords

Certain words don't help distinguish between good and bad headlines. Words like `the`, `a`, and `also` appear commonly in all contexts and don't tell us much about whether something is good or not. By removing these stopwords, we can reduce the size of the matrix and make training faster.

```python
# Read in and split the stopwords file.
with open("stop_words.txt", 'r') as f:
    stopwords = f.read().split("n")

# Do the same punctuation replacement that we did for the headlines, 
# so we're comparing the right things.
stopwords = [re.sub(r'[^wsd]', '', s.lower()) for s in stopwords]

unique_words = list(set(" ".join(new_headlines).split(" ")))

# Remove stopwords from the vocabulary.
unique_words = [w for w in unique_words if w not in stopwords]

print(make_matrix(new_headlines, unique_words))
```

Output:
```plaintext
   2  top  hn  people  immediately  like  python  80  meets  pretzels  ...  
0  1    0   0       0            0     0       0   0      0         0  ...  
1  0    0   0       0            0     0       0   0      0         0  ...  
2  0    0   0       0            0     0       0   0      0         0  ...  
3  0    0   0       0            0     0       0   0      0         0  ...  
4  0    0   0       0            0     0       0   0      0         0  ...  

   gta  10  uber  raises  pretzelbros  go  whatever  language  still  soul  
0    0   0     0       0            0   0         0         0      0     0  
1    0   0     0       0            0   0         0         0      0    

 0  
2    0   0     0       0            0   0         0         0      0     0  
3    0   0     0       0            0   0         0         0      0     0  
4    0   0     0       0            0   0         0         0      0     0  

[5 rows x 34 columns]
```

## Generating a Matrix for All Headlines

Now that we understand the basics, we can create a bag of words matrix for the entire set of headlines. We'll use a class from [scikit-learn](https://scikit-learn.org/stable/) to automate the process, making it much easier and faster.

```python
from sklearn.feature_extraction.text import CountVectorizer

# Construct a bag of words matrix.
# This will lowercase everything, and ignore all punctuation by default.
# It will also remove stop words.
vectorizer = CountVectorizer(lowercase=True, stop_words="english")

matrix = vectorizer.fit_transform(headlines)
print(matrix.todense())

# Apply the same method to all the headlines in all 100000 sublessons.
# We'll also add the URL of the sublesson to the end of the headline so we can take it into account.
sublessons['full_text'] = sublessons["headline"] + " " + sublessons["url"]
full_matrix = vectorizer.fit_transform(sublessons["headline"])
print(full_matrix.shape)
```

Output:
```plaintext
[[0 0 1 0 0 0 0 0 0 0 1 0 0 1 1 1 1 0 1 0 0 0 0 0 0 0 0]
 [1 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0]
 [0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 0 0 0 0 1]
 [0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 1 1 0 1 0]
 [0 0 0 0 0 1 1 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0]]
(9356, 13631)
```

## Reducing Dimensionality

We've created a matrix, but it has `13631` unique words (or columns), which will take a long time to make predictions with. To speed things up, we'll reduce the number of columns by selecting the most informative ones using a [chi-squared](https://en.wikipedia.org/wiki/Chi-squared_test) test. A chi-squared test finds the words that most differentiate between highly upvoted posts and posts without upvotes.

```python
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

# Convert the upvotes variable to binary so it works with a chi-squared test.
col = sublessons["upvotes"].copy(deep=True)
col_mean = col.mean()
col[col < col_mean] = 0
col[(col > 0) & (col > col_mean)] = 1

# Find the 1000 most informative columns.
selector = SelectKBest(chi2, k=1000)
selector.fit(full_matrix, col)
top_words = selector.get_support().nonzero()

# Pick only the most informative columns in the data.
chi_matrix = full_matrix[:, top_words[0]]
```

## Adding Meta Features

Ignoring the "meta" features of the headlines means missing out on valuable information. These features include length, punctuation count, average word length, and other sentence-specific features. Adding these can significantly improve prediction accuracy. To incorporate them, we'll loop over our headlines and apply a function to each one.

```python
# Our list of functions to apply.
transform_functions = [
    lambda x: len(x),
    lambda x: x.count(" "),
    lambda x: x.count("."),
    lambda x: x.count("!"),
    lambda x: x.count("?"),
    lambda x: len(x) / (x.count(" ") + 1),
    lambda x: x.count(" ") / (x.count(".") + 1),
    lambda x: len(re.findall("d", x)),
    lambda x: len(re.findall("[A-Z]", x)),
]

# Apply each function and put the results into a list.
columns = []
for func in transform_functions:
    columns.append(sublessons["headline"].apply(func))
    # Convert the meta features to a numpy array.
meta = numpy.asarray(columns).T
```

## Adding More Features

We have more features available than just text features. The `sublesson_time` column, which indicates when a story was submitted, can provide additional insights. Often in NLP, adding external features can significantly improve predictions. Some machine learning algorithms can determine how these features interact with your textual features.

```python
columns = []

# Convert the sublesson dates column to datetime.
sublesson_dates = pandas.to_datetime(sublessons["sublesson_time"])

# Transform functions for the datetime column.
transform_functions = [
    lambda x: x.year,
    lambda x: x.month,
    lambda x: x.day,
    lambda x: x.hour,
    lambda x: x.minute
]

# Apply all functions to the datetime column.
for func in transform_functions:
    columns.append(sublesson_dates.apply(func))

# Convert the meta features to a numpy array.
non_nlp = numpy.asarray(columns).T

# Concatenate the features together.
features = numpy.hstack([non_nlp, meta, chi_matrix.todense()])
```

## Making Predictions

Now that we can convert words to numbers, we can make predictions using an algorithm. We'll randomly select `7500` headlines as a training set and evaluate the algorithm's performance on the test set of `2500` headlines. Predicting results on the same set we train on would result in [overfitting](https://en.wikipedia.org/wiki/Overfitting), where the algorithm is overly optimized to the training set.

```python
from sklearn.linear_model import Ridge
import random

train_rows = 7500
# Set a seed to get the same "random" shuffle every time.
random.seed(1)

# Shuffle the indices for the matrix.
indices = list(range(features.shape[0]))
random.shuffle(indices)

# Create train and test sets.
train = features[indices[:train_rows], :]
test = features[indices[train_rows:], :]
train_upvotes = sublessons["upvotes"].iloc[indices[:train_rows]]
test_upvotes = sublessons["upvotes"].iloc[indices[train_rows:]]
train = numpy.nan_to_num(train)

# Run the regression and generate predictions for the test set.
reg = Ridge(alpha=.1)
reg.fit(train, train_upvotes)
predictions = reg.predict(test)
```

## Evaluating Error

We have predictions, but how do we determine their accuracy? One way is to calculate the error rate between the predictions and the actual upvote counts for the test set. We can use a simple method to make baseline estimates and compare the error rate of our predictions to the baseline estimates.

A straightforward baseline is to take the average number of upvotes per sublesson in the training set and use that as a prediction for every sublesson. We'll use [mean absolute error](https://en.wikipedia.org/wiki/Mean_absolute_error) as our error metric. It’s simple: subtract the actual value from the prediction, take the absolute value of the difference, then find the mean of all differences.

```python
# We're going to use mean absolute error as an error metric.
print(sum(abs(predictions - test_upvotes)) / len(predictions))

# As a baseline, we'll use the average number of upvotes across all sublessons.
average_upvotes = sum(test_upvotes) / len(test_upvotes)
print(sum(abs(average_upvotes - test_upvotes)) / len(predictions))
```

Output:
```plaintext
13.6606593988
17.2759421912
```

## Next Steps

This method worked reasonably but not spectacularly well on this dataset. We discovered that the headlines and other columns have some predictive value. We could improve this approach by using different predictive algorithms, like a random forest or a neural network. We could also use n-grams, such as bigrams and trigrams, when generating our bag of words matrix.

Be careful when adding additional features to ensure they only consider information that existed before the sublesson you're predicting for was made. All of these additions will take longer to run but will reduce error. Hopefully, you'll have some time to try them out! If you'd like to delve deeper into NLP, you can check out our interactive [Natural Language Programming Course](https://www.dataquest.io/path/data-scientist/).

---

This blog post provides a comprehensive tutorial on natural language processing with Python, demonstrating how to clean and process text data to make predictions using machine learning algorithms.