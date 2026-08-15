from mini.mod import classify


def describe_classify():
    def it_returns_a_label():
        assert isinstance(classify(-1), str)
        assert isinstance(classify(1), str)
