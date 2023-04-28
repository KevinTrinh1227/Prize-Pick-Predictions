""" =============================================
* This func compares the betting value (line_score)
* to the program's prediction value
============================================= """

def predict(line_score, avg_value, n_a):
    try:
        if line_score >= avg_value:
            prediction = "Lower"
            color = ""
        else:
            prediction = "Higher"
            color = ""
    except Exception as e:
        prediction = n_a

    return prediction