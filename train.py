# Anant Ahuja
# axa9357
#--------#---------#---------#---------#--------#--------#---------#---------#---------#--------#
import os
import sys
import string
import math
import random
#--------#---------#---------#---------#--------#--------#---------#---------#---------#--------#
def main():

    # Path supplied by command line argument
    if len(sys.argv) != 2:
        print("Usage: python3 train.py directory_name")
        return

    path = sys.argv[1]

    # Our seed for random shuffling
    seed = random.random()
    print('Seed = {}'.format(seed))

    # Dictionary D of all words in X
    D = {}

    # Label IDs, File Counts and Dictionaries
    label_ids = {}
    label_file_counts = {}
    label_dicts = []
    label_text_counts = {}

    # Total number of files in training set
    no_of_training_files = 0

    # Common English words list
    common_words = []

    # Label ID initialising
    label_id = 0

    # Building our common English words list
    with open('stop-word-list.txt') as f:
        lines = f.readlines()
        for line in lines:
            common_words.append(line)

    for char in string.ascii_lowercase:
        common_words.append(char)

    # Traversing each label folder in our data directory
    for folder in os.listdir(path):

        # Hidden file in Macs. Ignoring it.
        if folder == '.DS_Store':
            continue
        
        random.seed(seed)

        # Splitting the shuffled documents into training set
        files = os.listdir(path + '/' + folder)
        random.shuffle(files)
        training_set = files[0:500]

        # Counting number of files belonging to each label
        label_file_counts[folder] = len(training_set)

        # Assigning a label ID to each label
        label_ids[folder] = label_id
        label_dicts.append({})
        label_id += 1

        # Counting the number of files in our training set
        no_of_training_files += len(training_set)

        text_count = 0

        # For each document, open it
        for file in training_set:
            with open(path + '/' + folder + '/' + file, 'r', encoding='latin-1') as f:
                content = f.read()

                # Removing the headers
                header, newline, content = content.partition('\n\n')

                # Removing all symbols
                for char in string.punctuation:
                    content = content.replace(char, ' ')

                tokens = (content.lower()).split()

                for token in tokens:
                    if token in common_words or token.isnumeric():
                        pass

                    elif token in D and token in label_dicts[label_ids[folder]]:
                        D[token] += 1
                        label_dicts[label_ids[folder]][token] += 1
                        text_count += 1

                    elif token in D and token not in label_dicts[label_ids[folder]]:
                        label_dicts[label_ids[folder]][token] = 1
                        text_count += 1

                    else:
                        D[token] = 1
                        label_dicts[label_ids[folder]][token] = 1
                        text_count += 1

        # Counting number of tokens(not unique) belonging to each label
        label_text_counts[folder] = text_count

    print('Number of items in Vocabulary = {}'.format(len(D)))
    #print('Files incorrectly predicted below:')

    # Storing number of tokens(not unique) for each class
    label_priorc = {}
    label_accuracy = {}
    for label in label_ids:
        label_priorc[label] = label_file_counts[label] / no_of_training_files

    correct_count = 0
    categorical_count = 0
    no_of_testing_files = 0


    for folder in os.listdir(path):
        if folder == '.DS_Store':
            continue

        random.seed(seed)

        label_count = 0

        files = os.listdir(path + '/' + folder)
        random.shuffle(files)
        testing_set = files[500:]
        no_of_testing_files += len(testing_set)

        # For each doucment in our testing set,
        for file in testing_set:
            with open(path + '/' + folder + '/' + file, 'r', encoding='latin-1') as f:
                content = f.read()

                # Removing the headers
                header, newline, content = content.partition('\n\n')

                # Removing all symbols
                for char in string.punctuation:
                    content = content.replace(char, ' ')

                tokens = (content.lower()).split()

                file_scores = {}

                # Each document will be tested for each label
                for label in label_ids:
                    score = math.log(label_priorc[label])
                    for token in tokens:
                        if token in common_words or token.isnumeric():
                            pass
                        else:
                            try:
                                condprob = (label_dicts[label_ids[label]][token] + 1) / (label_text_counts[label] + len(D))

                            except KeyError:
                                condprob = 1 / (label_text_counts[label] + len(D))

                            score += math.log(condprob)

                    # Storing the score for each label in a dict
                    file_scores[label] = score

                # The label corresponding to the max score is chosen
                file_label = max(file_scores, key=file_scores.get)

            # Checking if the label predicted is correct
            if file_label == folder:
                correct_count += 1
                label_count += 1
            else:
                prediction_list = file_label.split('.')
                actual_list = folder.split('.')

                if len(prediction_list) > 2 and len(actual_list) > 2 and prediction_list[0] == actual_list[0] and prediction_list[1] == actual_list[1]:
                    categorical_count += 1

                elif len(prediction_list) <= 2 and len(actual_list) <= 2 and prediction_list[0] == actual_list[0]:
                    categorical_count += 1 
                #else:
                #    print('Actual label = {}, Predicted Label = {}'.format(folder, file_label))

        # Checking accuracy for each class
        label_accuracy[folder] = (label_count / len(testing_set)) * 100

    accuracy = (correct_count / no_of_testing_files) * 100
    categorical_accuracy = ((correct_count + categorical_count) / no_of_testing_files) * 100
    print('Accuracy = {}'.format(accuracy))
    print('Categorical Accuracy = {}'.format(categorical_accuracy))
    print('Label Accuracies = {}'.format(label_accuracy))

if __name__ == '__main__':
    main()