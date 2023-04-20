def predict(line_score, avg_value, n_a):

    try:
        if line_score >= avg_value:
            prediction = "Lower"
        else:
            prediction = "Higher"
    except Exception as e:
        prediction = n_a

    return prediction
