from mini.mod import classify


def describe_classify():
    def it_labels_negative_numbers():
        assert classify(-1) == "negative"

    def it_labels_zero_and_positive_numbers():
        assert classify(0) == "non-negative"
