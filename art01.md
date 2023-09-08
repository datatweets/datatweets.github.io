# Text Vectorizer and Word Embeddings
#DQ

In this lesson, you will learn how to use the `TextVectorizer` library in TensorFlow to transform text into numerical representations that can be used in deep learning models for text classification tasks.  You'll also learn about word embeddings, which are representations of words as vectors that capture semantic information about the words. Finally, you'll learn how to build a shallow neural network to perform text classification on the IMDB dataset.

* Use the TextVectorizer layer in TensorFlow for text transformation
* Use and vary parameters needed for building the vectorizer layer
* Perform word embedding using an embedding layer
* Build, train, and evaluate a shallow neural network text classification model

## Introduction
Welcome to the second lesson in **Natural Language Processing for Deep Learning!**

In the previous lesson, we learned how to differentiate between text and non-text data, explored the built-in datasets of TensorFlow Datasets, prepared text data for analysis, and learned how to create a WordCloud on a text corpus.

In this lesson, we will learn how to use the `TextVectorization` layer in TensorFlow to transform text into numerical data, and how to perform word embedding with the `Embedding` layer. Then we'll build, train, and evaluate a shallow neural network for text classification.

Specifically, we will cover the following topics:

* Using the `TextVectorization` layer in TensorFlow for text transformation.
* Varying the parameters necessary for building the vectorization layer.
* Performing word embedding using an `Embedding` layer.
* Building, training, and evaluating a shallow neural network for text classification.

This lesson is a great starting point for those who are building their first text classification model with TensorFlow.

So let's get started!

## Text Vectorization in TensorFlow

Before diving into the code for creating a text vectorization layer in TensorFlow, let's first discuss its significance in NLP.

Text vectorization plays a crucial role, as it allows our model to process, analyze, and interpret unstructured text data. This process involves converting text into numerical vectors, which can then serve as input for deep learning algorithms.

TensorFlow offers a powerful text vectorization layer, `tf.keras.layers.TextVectorization`, enabling the transformation of raw text into integer values. 

The `TextVectorization` layer accepts raw text as input and converts it into a numerical representation suitable for deep learning models. This process is accomplished by **tokenizing** the input text, meaning it's broken down into individual words or phrases. These smaller units, or **tokens**, are then assigned integer values for further processing. A simple workflow is illustrated below where a sample text, "**TensorFlow is great for NLP**" is processed in the `TextVectorization` layer, and the resulting output is an integer representation of those words. 

<center>
<img src="https://s3-us-east-2.amazonaws.com/dq-authoring-tmp-data/793-718/NLPTV.gif">
</center>

The `TextVectorization` layer also provides options for customizing the preprocessing step before vectorizing the text. These options include removing punctuation, converting all letters to lowercase, filtering out stopwords, and more.

Some of the parameters for the `TextVectorization` layer include:

* `max_tokens`: The maximum number of tokens to generate when tokenizing text. This represents the maximum size of the vocabulary.
* `output_mode`: How the output should be returned.
* `standardize`: Whether to apply standardization techniques (such as converting to lowercase) to the input data.
* `output_sequence_length`: The desired length of each sequence after tokenizing and preprocessing is completed.

These parameters enable fine-grained control when preprocessing text data for use in deep learning models. For more details on these and other parameters, please refer to the TensorFlow [`TextVectorization` documentation](https://www.tensorflow.org/api_docs/python/tf/keras/layers/experimental/preprocessing/TextVectorization?version=stable).

Now that we have an understanding of the `TextVectorization` layer and its parameters, we'll use it to create our first text vectorizer layer on the next screen. Before doing that, however, we need to load our test data.

We'll be using the `imdb_reviews` dataset, the same one we used in the previous lesson. To refresh your memory, the code used to create the `imdb_sample` training set is provided in the code editor to the right.

Our first step is to load the test data using the [`tfds.load()` function](https://www.tensorflow.org/datasets/api_docs/python/tfds/load) and pass it the appropriate `split` argument. 

As we did with the training data, we'll randomly sample the test data so that we only use 5000 observations for testing purposes. 

Now, let's write some code!


### Instructions
1. Create the variables `X_train` and `y_train` by extracting the values from the `text` and `label` columns, respectively, of the provided `imdb_sample` training dataframe.

2. Load the `test` set of the `imdb_reviews` dataset and store it in a variable named `imdb_test`.

3. Convert the loaded dataset into a pandas DataFrame object and store it in a variable named `imdb_test_df`.

4. Use the pandas vectorized string method `str.decode()` to decode the byte strings in the `text` column of `imdb_test_df` and assign the results back to the same column.

5. Create a sample of the `imdb_test_df` dataset and store it in `imdb_test_sample`:
   * The sample should contain 20% of the original dataset
   * Set `random_state` to `100`


6. Create the variables `X_test` and `y_test` by extracting the values from the `text` and `label` columns, respectively, of the `imdb_test_sample` you just created.

7. Print the frequency distribution of the target variable in the sample test dataset.

8. Print the total number of missing values in the sample test dataset.

### Hint
* Use the `split` and `name` arguments of `tfds.load()` to load the `test` set of `imdb_reviews`.
* Use the `tfds.as_dataframe()` fuction to convert `imdb_test` into a pandas DataFrame.
* Use the `value_counts()` method on the target variable to get the frequency distribution.
* To print the total number of missing values, use method chaining (`isna()` and `sum()`) on `imdb_test_sample`.

```py
import tensorflow_datasets as tfds

imdb_data = tfds.load(name="imdb_reviews", split="train")
imdb_df = tfds.as_dataframe(imdb_data)
imdb_df['text'] = imdb_df['text'].str.decode('utf-8')
imdb_sample = imdb_df.sample(frac=0.2, random_state=100)

X_train = imdb_sample['text']
y_train = imdb_sample['label']

imdb_test = tfds.load(name="imdb_reviews", split="test")
imdb_test_df = tfds.as_dataframe(imdb_test)
imdb_test_df['text'] = imdb_test_df['text'].str.decode('utf-8')
imdb_test_sample = imdb_test_df.sample(frac=0.2, random_state=100)

X_test = imdb_test_sample['text']
y_test = imdb_test_sample['label']

print(imdb_test_sample['label'].value_counts())
print(imdb_test_sample.isna().sum())
```

## Creating a TextVectorization Layer
Now that we've loaded our testing dataset, confirmed it's balanced, and has no missing data, let's create the `TextVectorization` layer.

We begin by importing the required library. Then, we instantiate a [`TextVectorization` layer](https://www.tensorflow.org/api_docs/python/tf/keras/layers/TextVectorization?version=stable), which converts textual inputs into numerical vectors that can be processed efficiently by a neural network. The example code is provided below:

```python 
from tensorflow.keras.layers import TextVectorization

layer_name = TextVectorization(max_tokens, output_mode, standardize, output_sequence_length, ...)
```
* `max_tokens`: The maximum number of tokens to generate when tokenizing text. This represents the **maximum size of the vocabulary**.
* `output_mode`: How the output should be returned.
* `standardize`: Whether to apply standardization techniques (such as converting to lowercase) to the input data.
* `output_sequence_length`: The desired length of each sequence after tokenizing and preprocessing is completed.

After creating the layer, we call the `adapt()` method on the `TextVectorization` layer and pass it our training text corpus. When we do this, the layer analyzes the provided text data and builds an internal vocabulary based on the text. The `adapt()` method essentially "fits" the `TextVectorization` layer to the given data. This allows it to learn the statistical properties of the text corpus, such as word frequencies and the overall distribution of words.

The `TextVectorization` layer tokenizes the text data, standardizes it (e.g., lowercasing and removing punctuation), and then builds a vocabulary by selecting the most frequent words up to the specified `max_tokens` parameter. This vocabulary is used to map each unique token (word, subword, or character) to a corresponding integer ID. This mapping allows the `TextVectorization` layer to convert input text into integer-encoded sequences when it processes new data. The example code is as follows:

```python 
layer_name.adapt(textdata)
```

The `output_sequence_length` parameter of the `TextVectorization` layer plays an important role in the text preprocessing pipeline. After the layer tokenizes and integer-encodes the input text based on the vocabulary built during the call to the `adapt()` method, it ensures that the output sequences have a consistent length by using the `output_sequence_length` parameter.

Here's how it works:

* If a tokenized input sequence has fewer tokens than the specified `output_sequence_length`, the layer pads the sequence with zeros at the end until it reaches the desired length. This is called **zero-padding** and ensures that shorter sequences match the expected input size for the neural network.

* If a tokenized input sequence has more tokens than the specified `output_sequence_length`, the layer truncates the sequence, removing tokens from the end until it reaches the desired length. This is called **truncation** and ensures that longer sequences do not exceed the expected input size for the neural network.

By setting the `output_sequence_length` parameter, we standardize the size of the input data fed into the neural network. This consistency is essential for training deep learning models because it ensures that the input tensors have uniform shapes across all samples, allowing for efficient batch processing during training and inference.

In the exercise below, we'll specify which parameters to use to create the layer and we'll also use the following arguments:

```python 
max_tokens = 7500
output_sequence_length = 128
 
```

Please note that these values were chosen based on our IMDB dataset. When working with other datasets, feel free to experiment with other values. Since selecting these hyperparameters requires some experimentation, it's best practice to assign them to a variable to facilitate this experimental process.

Let's create a vectorizer layer in the exercise below. On the next screen, we'll build the text classification model.

### Instructions
1. Create a `TextVectorization` object and assign it to the `vectorizer_layer` variable:
   * Import the `TextVectorization` layer from `tensorflow.keras.layers`

* Use the [official documentation](https://www.tensorflow.org/api_docs/python/tf/keras/layers/TextVectorization?version=stable) for `TextVectorization` to help you specify the following arguments:
  * `max_tokens` set to `max_tokens`
  * `output_mode` set to output integer indices
  * `standardize` set to convert all text to lowercase and remove all punctuation 
  * `output_sequence_length` set to `output_sequence_length`

    
2. Fit the `vectorizer_layer` to our training text data by using the `adapt()` method.

### Hint
* To output integer indices, set `output_mode='int'`.
* To convert all text to lowercase and remove all punctuation, set `standardize='lower_and_strip_punctuation'`.
* Pass the `X_train` array to your call to the `adapt()` method on `vectorizer_layer`. 

```py
X_train = imdb_sample['text']
y_train = imdb_sample['label']

imdb_test = tfds.load(name="imdb_reviews", split="test")
imdb_test_df = tfds.as_dataframe(imdb_test)
imdb_test_df['text'] = imdb_test_df['text'].str.decode('utf-8')
imdb_test_sample = imdb_test_df.sample(frac=0.2, random_state=100)

X_test = imdb_test_sample['text']
y_test = imdb_test_sample['label']

max_tokens = 7500
output_sequence_length = 128

from tensorflow.keras.layers import TextVectorization

vectorizer_layer = TextVectorization(max_tokens=max_tokens,
                                     output_mode='int',
                                     standardize='lower_and_strip_punctuation',
                                     output_sequence_length=output_sequence_length)

vectorizer_layer.adapt(X_train)
```

## Building the Model with the Vectorizer Layer
On the previous screen, we learned how to create a text vectorization layer. Now, we're ready to use that layer to construct a shallow neural network model for text classification. Let's get to it!

First, we instantiate a model using TensorFlow's Sequential API in Keras. We can use the sample code below to create the `Input` layer:

```python
tf.keras.Input(shape=(1,), dtype=tf.string)
```

The code above creates an `Input` layer with a shape of `(1,)` and the data type set to `tf.string`. This shape is used to indicate that each instance in the batch contains one string input. The data type `tf.string` ensures that the input layer is designed to accept text data represented as strings. This allows the model to process the raw text data correctly and pass it to the subsequent layers. 

After adding the input layer, we'll incorporate the `vectorizer_layer`. Then, we'll append a dense layer with one output neuron and a `sigmoid` activation function. This will provide an output between `0` or `1` based on the prediction. Since we're building a shallow neural network, we won't add any more hidden layers; we'll explore deeper networks in a subsequent lesson.

Once the model is assembled, we compile it by specifying a loss function and an optimizer for training. Use the sample code below as a guide:

```python
optimizer_name = tf.optimizers.optimizername(learning_rate=learning_rate)

model.compile(loss='loss_function',
              optimizer=optimizer_name, 
              metrics=['selected_metrics'])
```

After compiling the model, it can then be trained by passing in training inputs and labels to a `fit()` method call, like so: 

```python
model.fit(training_inputs, training_labels, epochs=10, verbose=0)
```
Once the model is trained, we evaluate its performance using the `evaluate()` method by asking the model to make predictions on the test dataset, like so:

```python
model.evaluate(test_inputs, test_labels)
```

By making these predictions and comparing them against the expected output, we can assess the model's performance using the test set we created earlier.

In the exercise below, we'll build, compile, train, and evaluate our first text classification model using the `TextVectorization` layer. Given that we're building a shallow neural network, we might not achieve stellar results, which is fine, as the objective is to learn the process. We'll improve the model results as we try out deep neural networks and other techniques in the lessons to come. 


### Instructions
1. Instantiate a Sequential model using Keras and give it the name `model`. 

2. Add an `Input` layer as demonstrated in the **Learn** section above. Use the same arguments as in the example. 

3. Add the `vectorizer_layer` to the model.   

4. Add an output layer with `1` node and use `sigmoid` as an activation function.   

5. Instantiate an `Adam` optimizer with a learning rate of `0.01` and save it to `opt`.

6. Compile the model using `opt` for the optimizer and binary crossentropy as the `loss` function. Use accuracy for `metrics`. 

7. Fit the model to the training data for `10` epochs, and pass the `verbose=2` argument to the call to the `fit()` method to print the training output. 

8. Evaluate the trained model on the test data. 

### Hint
* To add the `vectorizer_layer`, we add it to the `model` like any other layer: `model.add(vectorizer_layer)`.
* Use `'binary_crossentropy'` and `['accuracy']` for the `loss` and `metrics` arguments, respectively. 

```py
vectorizer_layer = TextVectorization(max_tokens=max_tokens, 
                                    output_mode='int', 
                                    standardize='lower_and_strip_punctuation',
                                    output_sequence_length=output_sequence_length)

vectorizer_layer.adapt(X_train)

model = tf.keras.models.Sequential()
model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
model.add(vectorizer_layer)
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

opt = tf.optimizers.Adam(learning_rate=0.01)
model.compile(loss='binary_crossentropy', 
              optimizer=opt, 
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, verbose=2)
model.evaluate(X_test, y_test)
```


## Create an Embedding Layer
On the previous screen, we learned how to use the `vectorizer_layer` to build a text classification neural network model. We achieved <span style = "background-color:#FF8080">51%</span> accuracy on the train set and <span style = "background-color:#FF8080">50%</span> accuracy on the test set – admittedly not that great, but certainly a good starting point for us to improve upon! Keep in mind that your results may vary slightly, and that's totally fine. Understanding the process is what's most important.

To improve our model's predictive power beyond a random guess, we'll explore creating an embedding layer in TensorFlow. Using an embedding layer can enhance a model's ability to recognize patterns in large amounts of unlabeled data by learning the relationships and meanings of different words. This is incredibly valuable in text classification modeling tasks. So let's dive into word embeddings!

### Word Embeddings

Word embeddings are vector representations of words used in NLP. Each word is represented by a fixed-length vector of numbers, with the values capturing meaningful relationships between words. Word embeddings help identify semantic relationships and concepts among words, which can be utilized for downstream tasks such as text classification, sentiment analysis, and machine translation. You can read more about word embeddings [here](https://www.tensorflow.org/text/guide/word_embeddings). 

### TensorFlow's Embedding Layer


The Embedding layer in TensorFlow maps words to a vector of numbers. It takes a sequence of integer-encoded words as input and returns a matrix where each row contains the numerical representation (embedding) of the corresponding word.



<mark>**FOR THE DESIGN TEAM**: Use the image below as a reference. MODIFICATIONS: Everything in the diagram to the left of "Embedding layer" should be labelled as "`TextVectorization`". Replace the two example texts on the left with: 1) "TensorFlow for NLP: Text analysis and text classification." and 2) "Using TensorFlow in NLP for text-based question answering." Then follow what the reference image does: make a table of unique words based on the first example text (all lowercase, no punctuation) and number the words starting at 1. Add the other unique words found in the second example text. IOW, the table will look like this: 
[tensorflow: 1, for: 2, nlp: 3, text: 4, analysis: 5, and: 6, classification: 7, using: 8, in: 9, based: 10, question: 11, answering: 12] then represent the two example texts using these indices. IOW: fist example text = [1, 2, 3, 4, 5, 6, 4, 7] and second example text = [8, 1, 9, 3, 2, 4, 10, 11, 12]. The "Embedding layer (output dim = 4)" should be changed to "Embedding Layer (output_dim=4)". Change the final output so that the first example text has 8 rows because that text has 8 words; change the final output of the second example text so that it has 9 rows because it has 9 words. Since we will keep `output_dim=4` in the embedding layer, both example texts should have four columns. The actual numeric values we use don't matter so much but any repeated words should also repeat their associated values. Keeping all values within (-1, 1) like the reference image will be fine.</mark>

<center>
<img src="https://s3-us-east-2.amazonaws.com/dq-authoring-tmp-data/793-718/EmbeddingLayerForDesignTeam.png">
</center>

This numerical representation can be used in downstream models, such as neural networks, to better capture semantic relationships between words.

To instantiate an embedding layer in TensorFlow, we use the `tf.keras.layers.Embedding` class. The three main parameters for an embedding layer are:

* `input_dim`: size of our vocabulary 
* `output_dim`: dimension of the dense embedding
* `input_length`: length of input sequences the layer receives

To ensure that the `Embedding` layer works correctly with the output of the `TextVectorization` layer we created previously, we should set the `input_dim` equal to the `max_tokens` value used for the `TextVectorization` layer. This way, the `Embedding` layer will be able to handle the integer indices generated by the `TextVectorization` layer for all tokens in the vocabulary.

The `output_dim` parameter specifies the number of dimensions in the output embedding vectors, which represent the words in the input text. These vectors are dense representations of the words, and the `output_dim` determines the size of this dense representation. We can choose the value of `output_dim` based on the complexity of our problem and the size of our dataset. A larger value may capture more detailed semantic information about the words, but it can also increase the number of model parameters and the computational requirements for training the model. In the example image above, this value was set to `4`. 

The `input_length` parameter in the `Embedding` layer specifies the expected length of the input sequences that the layer will receive. This parameter should match the `output_sequence_length` of the `TextVectorization` layer to ensure that the data being fed into the embedding layer has the appropriate shape. If there is a mismatch between these two lengths, it can lead to errors or incorrect behavior during model training.

You can learn more about the other parameters of TensorFlow's `Embedding` layer [here](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Embedding). 

In the exercise below, we'll create an embedding layer. On the next screen, we'll use this embedding layer for modeling.

### Instructions
1. Define an embedding dimension variable, `output_dim`, and assign it a value of `128`.

2. Import the `Embedding` layer from `tensorflow.keras.layers`.

3. Instantiate an embedding layer and give it the name `embedding_layer`. Pass the three arguments for setting the vocabulary size, embedding dimension, and input length.

### Hint
* To import the `Embedding` layer module directly from TensorFlow, use: `import Embedding from tf.keras.layers`.
* To set the vocabulary size, set `input_dim` to `max_tokens`.
* To set the embedding dimension, set `output_dim` to `output_dim` after initializing `output_dim = 128`.
* To set the input length, set `input_length` to `output_sequence_length`.

```py
max_tokens = 7500
output_sequence_length = 128
output_dim = 128

from tensorflow.keras.layers import Embedding 

embedding_layer = Embedding(input_dim=max_tokens, 
                            output_dim=output_dim, 
                            input_length=output_sequence_length)
```


## Text Classification Model with Embedding Layer
On the previous screen, we learned how to create an embedding layer. Now, we'll incorporate this layer into our text classifier neural network model.

To refresh your memory, here's the model we built using the `TextVectorization` layer: 

```python
model = tf.keras.models.Sequential()
model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
model.add(vectorizer_layer)
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
```

Adding the `embedding_layer` to our model is straightforward and can be done in the same manner as the `vectorizer_layer` was added in the code above. 

In addition to integrating the embedding layer into our model, we're also going to modify some arguments and add one new argument when instantiating our `TextVectorization` layer. The full list of arguments can be found [here](https://www.tensorflow.org/api_docs/python/tf/keras/layers/TextVectorization).

The new argument we'll add to our `TextVectorization` layer is `ngram`. An **n-gram** is a contiguous sequence of n words or tokens from a given text or document. N-grams are used in NLP and text analysis to model and capture the context and relationships between words in a text. They help in identifying patterns and predicting the next word or sequence of words, which is particularly useful for applications such as language modeling, text classification, and information retrieval.

For example, consider the sentence: "I love natural language processing."

* When `ngrams = 1` (unigram), the n-grams are individual words: 
  * `["i", "love", "natural", "language", "processing"]`
* When `ngrams = 2` (bigram), the n-grams are pairs of consecutive words: 
  * `["i love", "love natural", "natural language", "language processing"]`
* When `ngrams = 3` (trigram), the n-grams are sequences of three consecutive words: 
  * `["i love natural", "love natural language", "natural language processing"]`

As the value of n increases, n-grams capture more context and the relationships between words, but the number of unique n-grams also increases, which can lead to a larger and more complex feature space. We can also use a tuple to set the value for `ngrams` to set a range of n-grams we would like to generate. 

For example, when `ngrams=(1, 3)`, the `TextVectorization` layer will generate the following tokenized text (assuming no punctuation and lowercased):

* Unigrams: `['i', 'love', 'natural', 'language', 'processing']`
* Bigrams: `['i love', 'love natural', 'natural language', 'language processing']`
* Trigrams: `['i love natural', 'love natural language', 'natural language processing']`

The combined output will include all unigrams, bigrams, and trigrams:

`['i', 'love', 'natural', 'language', 'processing', 'i love', 'love natural', 'natural language', 'language processing', 'i love natural', 'love natural language', 'natural language processing']`

In the exercise below, we'll add the `ngram` argument to our `vectorizer_layer` along with adding the `embedding_layer` to our model and evaluate its performance.

The general flow we'll be using for model building is illustrated below:

<center>
<img src="https://s3-us-east-2.amazonaws.com/dq-authoring-tmp-data/793-718/NLPmodelflow.png">
</center>

We have already imported both the `TextVectorization` and `Embedding` layers for your convenience.


### Instructions
1. Create a `TextVectorization` object and assign it to the `vectorizer_layer` variable.

   1.1 Specify the following arguments:

* `max_tokens` set to `max_tokens`
  * `output_mode` set to integer-encode the text
  * `standardize` set to make everything lowercase only
  * `ngrams` set to use unigrams and bigrams, combined
  * `output_sequence_length` to `output_sequence_length`

    
3. Use the `adapt()` method on `vectorizer_layer` to fit it to the training text data.

4. Create a Sequential model using Keras and give it the name `model`. 

5. Add an `Input` layer followed by the vectorizer layer, and an embedding layer like we created on the previous screen.

6. Add an output layer with `1` node and `sigmoid` as an activation function.   

7. Compile the model with the same configurations we used previously: 
   * Instantiate an `Adam` optimizer with a learning rate of `0.01` and store it as `opt`
     * Use a binary crossentropy loss function
     * Use accuracy for `metrics`

8. Fit the model to the training data for `10` epochs. Be sure to pass `verbose=2` to the method call to print the training output.

9. Evaluate the trained model on test data. 

### Hint
* To make everything lower case only, set `standardize='lower'`.
* To use a combination of unigrams and bigrams, set `ngrams=(1, 2)`.
* To create the `embedding_layer` we created on the previous screen, use: `tf.keras.layers.Embedding(input_dim=max_tokens, output_dim=output_dim, input_length=output_sequence_length)`.

```py
from tensorflow.keras.layers import TextVectorization, Embedding

max_tokens = 7500
output_sequence_length = 128
output_dim = 128

vectorizer_layer = TextVectorization(max_tokens=max_tokens, 
                                     output_mode='int', 
                                     standardize='lower', 
                                     ngrams=(1, 2), 
                                     output_sequence_length=output_sequence_length)

vectorizer_layer.adapt(X_train)
embedding_layer = Embedding(input_dim=max_tokens, 
                            output_dim=output_dim, 
                            input_length=output_sequence_length)

model = tf.keras.models.Sequential()
model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
model.add(vectorizer_layer)
model.add(embedding_layer),
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

opt = tf.optimizers.Adam(learning_rate=0.01)
model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, verbose=2)
model.evaluate(X_test, y_test)
```

## Review
Congratulations on completing your second lesson in **Natural Language Processing for Deep Learning**! We've made significant progress by building text classification models using shallow neural networks.

In this lesson, we've learned how to:

* Use the `TextVectorization` layer in TensorFlow for text transformation.

* Apply and modify parameters needed for building the vectorizer layer.

* Perform word embedding using an embedding layer.

* Build, train, and evaluate a shallow neural text classification model.

During this lesson, we constructed a neural network model with a vectorizer layer and then added an embedding layer to it. The model performance summary is presented below.

We achieved an accuracy of:

* <span style = "background-color:#FF8080">51%</span> on train data and <span style = "background-color:#FF8080">50%</span> on test data for the `model` with just a text vectorization layer.

* <span style = "background-color:#FF8080">55%</span> on train data and <span style = "background-color:#FF8080">53%</span> on test data for the `model` with text vectorization and embedding layers.

The comparison above shows that the model with the embedding layer performs better than the one without. This suggests that the embedding layer contributes positively to the model's performance. However, it's important to note that the overall performance of the model is not exceptional, and you may obtain slightly different results, which is completely fine! The key takeaway is that you've learned how to build, train, and evaluate a neural network for text classification purposes.

Fantastic job in this lesson! With the knowledge gained here, we're now ready to tackle building multi-layer text classification models with TensorFlow in the next lesson. We'll explore whether these improvements enhance the model's performance and yield better results than what we achieved here. Good luck, and see you in the next lesson!



## Takeaways
## Syntax


* Loading the required libraries:

  ```
  import tensorflow as tf
  import tensorflow_datasets as tfds
  from tensorflow.keras.layers import TextVectorization
  ```

* Loading TensorFlow datasets and extracting the subsets: 

  ```
  imdb_data = tfds.load(name="imdb_reviews", split="train")
  imdb_df = tfds.as_dataframe(imdb_data)
  imdb_df['text'] = imdb_df['text'].str.decode('utf-8')
  imdb_sample = imdb_df.sample(frac=0.2, random_state=100)
  imdb_test = tfds.load(name="imdb_reviews", split="test")
  imdb_test_df = tfds.as_dataframe(imdb_test)
  imdb_test_df['text'] = imdb_test_df['text'].str.decode('utf-8')
  imdb_test_sample = imdb_test_df.sample(frac=0.2, random_state=100)
  ```

* Split the data into train and test dataset:

  ```
  X_train = imdb_sample['text']
  y_train = imdb_sample['label']
  X_test = imdb_test_sample['text']
  y_test = imdb_test_sample['label']
  ```

* Model parameters:

  ```
  max_tokens = 7500
  input_length = 128
  output_dim = 128
  ```

* Building the model with `vectorizer_layer`:

  ```
  vectorizer_layer = tf.keras.layers.TextVectorization(max_tokens=max_tokens, output_mode='int', standardize='lower_and_strip_punctuation', output_sequence_length=input_length)
  vectorizer_layer.adapt(X_train)
  model = tf.keras.models.Sequential()
  model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
  model.add(vectorizer_layer)
  model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
  opt = tf.optimizers.Adam(learning_rate=0.01)
  model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
  model.fit(X_train, y_train, epochs=10, verbose=2)
  print(model.evaluate(X_test, y_test))
  ```

* Creating and Embedding Layer:

  ```
  embedding_layer = tf.keras.layers.Embedding(input_dim, output_dim) 
  ```

* Building the model with vectorizer layer and embedding layer:

  ```
  vectorizer_layer = tf.keras.layers.TextVectorization(max_tokens=max_tokens, output_mode='int', standardize='lower_and_strip_punctuation', output_sequence_length=input_length)
  vectorizer_layer.adapt(X_train)
  embedding_layer = tf.keras.layers.Embedding(input_dim, output_dim, input_length=input_length)
  model = tf.keras.models.Sequential()
  model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
  model.add(vectorizer_layer)
  model.add(tf.keras.layers.Embedding(input_dim, output_dim, input_length=input_length)),
  model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
  opt = tf.optimizers.Adam(learning_rate=0.01)
  model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
  model.fit(X_train, y_train, epochs=10, verbose=2)
  model.evaluate(X_test, y_test)
  ```  

## Concepts

* Text vectorization is an important process in NLP because it enables computers to understand, analyze, and interpret unstructured text data. Text vectorization involves transforming text into numerical vectors which can then be used as input for deep learning algorithms.

* One of the powerful features of TensorFlow is its text vectorization layer, `tf.keras.layers.TextVectorization`, which allows us to transform raw text into numerical vectors and use it to feed data into a model. The `TextVectorization` layer takes raw text as its input and converts it into numerical values that are suitable for use in machine learning models. It does this by tokenizing the input text into words or phrases, which are then converted into numerical values based on their frequency in the corpus of data being analyzed. 

* The `TextVectorization` layer also provided options to customize the preprocessing step prior to vectorizing the text. This includes options to remove punctuation, change all letters to lowercase, filter out stopwords, and more. 

* Word embeddings are vector representations of words used in NLP. Each word is represented by a fixed-length vector of numbers, where the values represent meaningful relationship between words. The idea behind word embeddings is to capture semantic relationships and concepts among words that can be utilized for downstream tasks such as text classification, sentiment analysis, and machine translation.

* The Embedding layer in TensorFlow is responsible for mapping words to a vector of numbers. It takes as input a list of words and returns a matrix with each row containing the numerical representation of the corresponding word. This numerical representation can then be used in downstream models such as neural networks to better capture semantic relationships between words. 

* In simple terms, the Embedding layer is like a dictionary that takes in integer indices (which represent specific words) and outputs dense vectors (their embeddings). The embedding layer in TensorFlow can be instantiated using the `tf.keras.layers.Embedding` class.


## Resources

* [TextVectorization](https://www.tensorflow.org/api_docs/python/tf/keras/layers/experimental/preprocessing/TextVectorization?version=stable)

* [Word Embeddings](https://www.tensorflow.org/text/guide/word_embeddings).  

* [Embedding layer](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Embedding)


