def obfuscate_string(mystr: str) -> str:
    """Only shows the first and last letters of a string


    Args:
        mystr (str): the string to obfuscate
    Returns
        str : the obfuscated string
    """
    if len(mystr) <= 2:
        return "**"
    elif len(mystr) <= 5:
        return mystr[0] + "**" + mystr[-1]
    else:
        return mystr[:2] + "**" + mystr[-2:]
