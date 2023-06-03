emotions = {
    ":D": 4,
    ":)": 3,
    ":|": 2,
    ":(": 1,
    "T_T": 0
    }

def sort_emotions(arr, order):
    return sorted(arr, key=lambda x: emotions[x], reverse=order)