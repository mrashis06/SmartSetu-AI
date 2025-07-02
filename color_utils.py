# color_utils.py

def get_score_color(score, kind="credit"):
    if kind == "credit":
        if score >= 80:
            return "green"
        elif score >= 50:
            return "orange"
        else:
            return "red"
    elif kind == "risk":
        if score < 20:
            return "green"
        elif score <= 50:
            return "orange"
        else:
            return "red"

def get_level_color(level):
    level = level.lower()
    if "low" in level:
        return "green"
    elif "medium" in level:
        return "orange"
    else:
        return "red"
