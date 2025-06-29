# loan.py

def determine_loan_offer(credit_score):
    if credit_score >= 80:
        return 100000, 4
    elif credit_score >= 60:
        return 50000, 6
    elif credit_score >= 40:
        return 20000, 8
    elif credit_score >= 30:
        return 10000, 10
    else:
        return 0, 0

def calculate_emi(loan_amount, months, interest_rate):
    total_repayment = loan_amount + (loan_amount * interest_rate * months / (12 * 100))
    emi = round(total_repayment / months, 2)
    return emi, round(total_repayment)
