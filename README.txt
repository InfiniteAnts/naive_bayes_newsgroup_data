Name: Anant Ahuja
Programming Language used: Python 3.7.3

1. Download and install Python 3 from here (https://wiki.python.org/moin/BeginnersGuide/Download). >= Python 3.5 is required to run this code.

2. Run the code by navigating to the directory and type the following command in the terminal: "python3 train.py 20_newsgroups > output.txt"

3. The output.txt file lists the seed used for random shuffling, the total number of items in the Vocabulary, total accuracy, categorical accuracy and label specific accuracy for all the labels.

Summary: Text classification of the given Newsgroup data was done by building a Naive Bayes classifier. Accuracy of the built classifier = 76%.

Preprocessing:
1. Common English Words: First step which was taken was to build a list of
common English words. All prepositions, articles etc. were added to this list. For example: words like the, a, an, below, under, of, from etc. are pretty common in any form of English text and no useful information can be gleaned from them so we can safely ignore these words while parsing. Infact they increased the size of the Vocabulary and thus hampered the performance and accuracy of the model so ignoring these words was very much needed.
2. Single characters: All single alphabetical characters were added to this list too because no information can be gleaned for them either and they serve no purpose.
3. Headers: Each document in our data came with a header specifying the newsgroup it was obtained from, it’s label, email, date etc. Since the header contained the label of the data, removing it was essential as we would be getting a fake boosted accuracy if it wasn’t removed. The accuracy observed without removing headers was intact 86%, around 10% more than the actual accuracy of our model. The header also came with a lot of other tokens like email, date etc. which were useless for our purposes. Keeping the headers may have made our model biased towards certain newsgroups too, for example: If a certain newsgroup appears in a lot of Atheism documents during training, while testing a document from that same newsgroup may be inaccurately classified as belonging to the Atheism newsgroup. Hence, removing any identifying information is crucial to avoid biases in a ML model.
4. Footers: Most documents in our data also came with a footer which was basically a signature of the poster which often included email, name etc. Again this wasn’t needed since the signature wouldn’t contain label identifying information and would just expand our Vocabulary. Removing
Footers had no noticeable effect on the accuracy but the size of our Vocabulary definitely decreased.
5. Symbols: The document was rife with symbol characters like >,@.?! etc. and were replaced by whitespace while parsing the file. Python’s string.punctuation constant was queried to remove these characters.
6. Numeric characters: All the numeric characters and all the words in our common English words list were removed from the text.
7. Lowercase: All the characters in this preprocessed text are now converted to lowercase.
8. Tokenizing: The preprocessed text is then tokenised and we begin training the classifier.

Training:
1. The data is shuffled and split 50-50 into training and testing data.
2. Vocabulary: Each unique token from each document is added to a Dictionary and it’s frequency is updated.
3. Label Specific Dictionary: A list of label specific dictionaries are maintained and each token encountered in a specific labelled document is added to it’s corresponding dictionary and it’s frequency is updated.
4. Label Specific Text Count: A dictionary of total token count of each label is also stored.

Output:
Even though the model’s accuracy is 76%, for the files it is not able to predict correctly, it is still able to predict the category of that document correctly. For example: there are 2 classes, windows.x and windows.misc, a lot of windows.x documents are incorrectly classified as windows.misc. Similarly alt.atheism and talk.religion are incorrectly predicted as each other quite often because of the presence of the same unique tokens in both the classes. A rudimentary categorical accuracy is also calculated and included in the output file though it only accounts for labels having the same substrings. So alt.atheism and talk.religion inaccuracies are not accounted in that categorical accuracy.
