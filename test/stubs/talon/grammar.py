# This is a class in the Talon runtime, but is only used as a type in knausj. We
# stub it here as a blank class, since there are (for example) functions which
# check isinstance(some_input, Phrase), and for testing we want these tests to
# return False.
class Phrase:
    pass


# grammar.vm.Phrase is also used sometimes.
class vm:
    Phrase = Phrase
