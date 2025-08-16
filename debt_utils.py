def snowball_strategy(debts, extra_payment=0):
    """
    Snowball method: pay smallest balance first.
    debts = list of dicts: [{"balance": x, "interest": y, "minimum": z}, ...]
    Returns a list of monthly debt states until all are paid.
    """
    debts = sorted(debts, key=lambda d: d["balance"])  # smallest first
    month = 0
    history = []

    while any(d["balance"] > 0 for d in debts):
        month += 1
        payment = extra_payment
        for d in debts:
            if d["balance"] <= 0:
                continue
            # Apply interest
            d["balance"] *= (1 + d["interest"] / 100 / 12)
            pay = d["minimum"]
            if d == debts[0]:  # target smallest debt
                pay += payment
            d["balance"] = max(0, d["balance"] - pay)
        history.append({"month": month, "debts": [round(d["balance"], 2) for d in debts]})
        debts = sorted(debts, key=lambda d: d["balance"])
    return history


def avalanche_strategy(debts, extra_payment=0):
    """
    Avalanche method: pay highest interest first.
    """
    debts = sorted(debts, key=lambda d: d["interest"], reverse=True)  # highest rate first
    month = 0
    history = []

    while any(d["balance"] > 0 for d in debts):
        month += 1
        payment = extra_payment
        for d in debts:
            if d["balance"] <= 0:
                continue
            d["balance"] *= (1 + d["interest"] / 100 / 12)
            pay = d["minimum"]
            if d == debts[0]:  # target highest interest
                pay += payment
            d["balance"] = max(0, d["balance"] - pay)
        history.append({"month": month, "debts": [round(d["balance"], 2) for d in debts]})
        debts = sorted(debts, key=lambda d: d["interest"], reverse=True)
    return history
