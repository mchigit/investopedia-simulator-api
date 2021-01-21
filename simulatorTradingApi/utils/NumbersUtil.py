def extractNumberFromMoney(string):
    """
    Extract number from string following this pattern:
    $130,321 -> 130321
    Also will round to 2 decimal places
    """
    try:
        trimmed = string.strip().replace(",", "")
        number = float(trimmed[1:])
        return round(number, 2)
    except ValueError:
        print("could not parse string")


def extractPercentage(string):
    """
    Extract number from string following this pattern:
    78.80% -> 78.8
    Also will round to 2 decimal places
    """
    try:
        trimmed = string.strip().replace(",", "")
        number = float(trimmed[:-1])
        return round(number, 2)
    except ValueError:
        print("could not parse string")


def extractTodaysChange(string):
    """
    Extract number from string following this pattern:
    $300(3.00%) -> [300, 3]
    -$123(-3.2%) -> [-123, -3.20]
    Also will round to 2 decimal places
    """
    trimmed = string.strip()
    strings = trimmed.split("(")
    for i in range(len(strings)):
        strings[i] = (
            strings[i].replace("$", "").replace(")", "").replace("%", "").strip()
        )

    return strings
