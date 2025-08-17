def snowball_strategy(debts, extra_payment=0):
    """
    Snowball: focus on smallest balance first.
    This simulates monthly payments until everything is paid off.
    """
    # Sort debts so smallest balance is first in line
    debts = sorted(debts, key=lambda d: d["balance"])
    month = 0
    history = []

    # Loop until all debts are gone
    while any(d["balance"] > 0 for d in debts):
        month += 1
        payment = extra_payment
        for d in debts:
            if d["balance"] <= 0:
                continue
            # Apply monthly interest
            d["balance"] *= (1 + d["interest"] / 100 / 12)
            pay = d["minimum"]
            if d == debts[0]:  # target smallest debt with extra
                pay += payment
            # Reduce balance (no negative values allowed)
            d["balance"] = max(0, d["balance"] - pay)
        # Save snapshot of this month
        history.append({"month": month, "debts": [round(d["balance"], 2) for d in debts]})
        # Re-sort in case a new smallest debt emerges
        debts = sorted(debts, key=lambda d: d["balance"])
    return history

def avalanche_strategy(debts, extra_payment=0):
    """
    Avalanche: focus on highest interest rate first.
    """
    debts = sorted(debts, key=lambda d: d["interest"], reverse=True)
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
            if d == debts[0]:  # target high interest with extra
                pay += payment
            d["balance"] = max(0, d["balance"] - pay)
        history.append({"month": month, "debts": [round(d["balance"], 2) for d in debts]})
        debts = sorted(debts, key=lambda d: d["interest"], reverse=True)
    return history
