def extract_number_from_money(string):
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


def extract_percentage(string):
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


def extract_todays_change(string):
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
            strings[i].replace("$", "").replace(
                ")", "").replace("%", "").strip()
        )

    return strings


def extract_number_from_sentence(string):
    """
    Extract number from a sentence string:
    This is a sentence contain 32 numbers -> [32]
    """
    trimmed = string.strip()
    return [int(s) for s in trimmed.split() if s.isdigit()]
