import math
import argparse

parser = argparse.ArgumentParser(description="This program is loan calculator.")
parser.add_argument("--type", type=str, help="Chose type of payment")
parser.add_argument("--payment", type=float, help="Amount payment")
parser.add_argument("--principal", type=float, help="Principal value")
parser.add_argument("--periods", type=int, help="Number of payments")
parser.add_argument("--interest", type=float, help="interest without percent sign")

args = parser.parse_args()


def scan():
    count_wrong = 0
    if args.payment is None:
        count_wrong = +1
    if args.principal is None:
        count_wrong = +1
    if args.periods is None:
        count_wrong = +1
    if args.interest is None:
        count_wrong = +1
    if count_wrong >= 2:
        return True
    else:
        return False


if args.type != "annuity" and args.type != "diff":
    print("Incorrect parameters")
    exit()

if args.type == "diff" and args.payment is not None:
    print("Incorrect parameters")
    exit()

if args.interest is None:
    print("Incorrect parameters")
    exit()

if args.type == "diff" and (args.principal is None or args.periods is None or args.interest is None):
    print("Incorrect parameters")
    exit()

if args.type == "annuity" and scan():
    print("Incorrect parameters")
    exit()

if (args.principal is not None and args.principal < 0) or (args.periods is not None and args.periods < 0) \
        or (args.interest is not None and args.interest < 0):
    print("Incorrect parameters")
    exit()

if args.type == "annuity" and args.payment is None:
    loan_principal = args.principal
    number_of_payments = args.periods
    interest = args.interest

    monthly_payment = math.ceil(loan_principal * (interest / 1200) * math.pow(1 + interest / 1200, number_of_payments) / \
                                (pow(1 + interest / 1200, number_of_payments) - 1))

    print(f"Your annuity payment = {monthly_payment}!")
    print("Overpayment =", round(monthly_payment * number_of_payments - loan_principal))

if args.type == "annuity" and args.principal is None:
    monthly_payment = args.payment
    number_of_payments = args.periods
    interest = args.interest

    loan_principal = math.floor(monthly_payment / (interest / 1200 * math.pow(1 + interest / 1200, number_of_payments) /
                                                   (math.pow(1 + interest / 1200, number_of_payments) - 1)))
    print(f"Your loan principal = {loan_principal}!")
    print("Overpayment =", round(monthly_payment * number_of_payments - loan_principal))

if args.type == "annuity" and args.periods is None:
    loan_principal = args.principal
    monthly_payment = args.payment
    interest = args.interest

    number_of_payments = math.ceil(math.log(monthly_payment / (monthly_payment - loan_principal *
                                                               (interest / 1200)), 1 + (interest / 1200)))
    years = number_of_payments // 12
    months = number_of_payments % 12
    if years != 0 and months != 0:
        print(f"It will take {years} years and {months} months to repay this loan!")
    elif years != 0 and months == 0:
        print(f"It will take {years} years to repay this loan!")
    elif years == 0 and months != 0:
        print(f"It will take {months} months to repay this loan!")
    print("Overpayment =", round(monthly_payment * number_of_payments - loan_principal))

if args.type == "diff":
    loan_principal = args.principal
    number_of_payments = args.periods
    interest = args.interest
    total_payment = 0
    for i in range (1, args.periods+1):
        monthly_payment = math.ceil(loan_principal/number_of_payments + interest/1200*\
                          (loan_principal-(loan_principal*(i-1))/number_of_payments))
        print(f"Month {i}: payment is {monthly_payment}")
        total_payment += monthly_payment
    print()
    print("Overpayment =", round(total_payment - loan_principal))
