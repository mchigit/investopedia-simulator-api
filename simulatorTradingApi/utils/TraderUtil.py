def extractNumberFromSentence(string):
    trimmed = string.strip()

    return [int(s) for s in trimmed.split() if s.isdigit()]