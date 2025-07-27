def convert_digit(d):
    digits = {
        1: "GK", 2: "`yB", 3: "wZb", 4: "Pvi", 5: "cvuP",
        6: "Qq", 7: "mvZ", 8: "AvU", 9: "bq", 0: ""
    }
    return digits.get(int(d), "")

def convert_tens(n):
    n = str(int(n))  # Remove leading zeros
    val = int(n)
    result_map = {
        # 1-19
        1: "GK", 10: "`k", 11: "GMvi", 12: "evi", 13: "†Zi", 14: "†PŠÏ",
        15: "c‡bi", 16: "†lvj", 17: "m‡Zi", 18: "AvVvi", 19: "Ewbk",
        # 20-29
        2: "`yB", 20: "wek", 21: "GKzk", 22: "evBk", 23: "†ZBk",
        24: "PweŸk", 25: "cuwPk", 26: "QvweŸk", 27: "mvZvk", 28: "AvVvk", 29: "EbwÎk",
        # 30-39
        3: "wZb", 30: "wÎk", 31: "GKwÎk", 32: "ewÎk", 33: "†ZwÎk", 34: "†PŠwÎk",
        35: "cuqwÎk", 36: "QwÎk", 37: "mvuBwÎk", 38: "AvUwÎk", 39: "EbPwjøk",
        # 40-49
        4: "Pvi", 40: "Pwjøk", 41: "GKPwjøk", 42: "weqvwjøk", 43: "†ZZvwjøk",
        44: "Pzqvwjøk", 45: "cuqZvwjøk", 46: "†QPwjøk", 47: "mvZPwjøk", 48: "AvUPwjøk", 49: "EbcÂvk",
        # 50-59
        5: "cvuP", 50: "cÂvk", 51: "GKvbœ", 52: "evqvbœ", 53: "wZàvbœ",
        54: "Pzqvbœ", 55: "cÂvbœ", 56: "Qvàvbœ", 57: "mvZvbœ", 58: "AvUvbœ", 59: "EblvU",
        # 60-69
        6: "Qq", 60: "lvU", 61: "GKlwÆ", 62: "evlwÆ", 63: "†ZlwÆ", 64: "†PŠlwÆ",
        65: "cuqlwÆ", 66: "†QlwÆ", 67: "mvZlwÆ", 68: "AvUlwÆ", 69: "EbmËi",
        # 70-79
        7: "mvZ", 70: "mËi", 71: "GKvËi", 72: "evnvËi", 73: "wZqvËi", 74: "PzqvËi",
        75: "cuPvËi", 76: "wQqvËi", 77: "mvZvËi", 78: "AvUvËi", 79: "EbAvwk ",
        # 80-89
        8: "AvU", 80: "Avwk", 81: "GKvwk", 82: "weivwk", 83: "wZivwk", 84: "Pzivwk",
        85: "cuPvwk", 86: "wQqvwk", 87: "mvZvwk", 88: "AvUvwk", 89: "EbbeŸB",
        # 90-99
        9: "bq", 90: "beŸB", 91: "GKvbeŸB", 92: "weivbeŸB", 93: "wZivbeŸB", 94: "PzivbeŸB",
        95: "cuPvbeŸB", 96: "wQqvbeŸB", 97: "mvZvbeŸB", 98: "AvUvbeŸB", 99: "wbivbeŸB",
    }
    return result_map.get(val, "")

def convert_hundreds(n):
    n = str(n).zfill(3)
    result = ""
    if int(n) == 0:
        return ""
    if n[0] != "0":
        result += convert_digit(n[0]) + "kZ "
    if n[1] != "0":
        result += convert_tens(n[1:])
    else:
        result += convert_digit(n[2])
    return result.strip()

def taka(amount):
    amount = str(round(float(amount), 2))
    if '.' in amount:
        taka_part, poisha_part = amount.split('.')
        poisha_part = poisha_part.ljust(2, '0')[:2]
    else:
        taka_part, poisha_part = amount, ""

    places = ["", " nvRvi ", " j¶ ", " †KvwU "]  # skip [0], use index from 1
    rupees = ""
    count = 1

    while taka_part:
        if count == 1:
            chunk = taka_part[-3:]
            taka_part = taka_part[:-3]
            temp = convert_hundreds(chunk)
        else:
            chunk = taka_part[-2:]
            taka_part = taka_part[:-2]
            temp = convert_tens(chunk)
        if temp:
            rupees = temp + places[count - 1] + rupees
        count += 1

    if rupees:
        rupees += " UvKv"

    paise = ""
    if poisha_part and int(poisha_part) > 0:
        paise = " " + convert_tens(poisha_part) + " cqmv"

    return (rupees + paise).strip()
print(taka(486324))