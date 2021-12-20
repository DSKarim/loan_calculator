import math
import argparse

parser = argparse.ArgumentParser(description='Loan calculator')
parser.add_argument('--principal', type=int, help='Loan principal')
parser.add_argument('--payment', type=int, help='Monthly payment')
parser.add_argument('--periods', type=int, help='Loan periods')
parser.add_argument('--interest', type=float, help='Interest rate')
parser.add_argument('--type', type=str, help='Loan type')
args = parser.parse_args()

# Check if all arguments are passed
num_of_args = 5
for arg in args.__dict__.values():
    if arg is None:
        num_of_args -= 1

if num_of_args < 4:
    print('Incorrect parameters')
    exit()
if args.type not in ['annuity', 'diff']:
    print('Incorrect parameters')
    exit()
if args.type == 'diff' and args.payment is not None:
    print('Incorrect parameters')
    exit()
if args.interest is not None and (args.interest < 0 or args.interest > 100):
    print('Incorrect parameters')
    exit()


def count_loan_principal(a, i, n):
    return a / ((i * (1 + i) ** n) / ((1 + i) ** n - 1))


def count_number_of_payments(a, i, p):
    return math.log(a / (a - i * p), 1 + i)


def count_annuity_payment(i, p, n):
    return p * ((i * (1 + i) ** n) / ((1 + i) ** n - 1))


def count_interest_payment(p, i, n):
    p = int(p)
    i = float(i) / 1200
    n = int(n)
    m = 1
    total_payment = 0
    while m <= n:
        d = p / n + i * (p - (p * (m - 1) / n))
        total_payment += int(math.ceil(d))
        print('Month {m}: payment is {d}' .format(m=m, d=int(math.ceil(d))))
        m += 1
    print('Overpayment = {overpayment}' .format(overpayment=int(total_payment - p)))


def get_annuity(user_choice, p, i, n, a):
    p = int(p)
    a = float(a)
    i = float(i) / 1200
    n = int(n)
    if user_choice == 'n':
        n = round(math.ceil(count_number_of_payments(a, i, p)))
        if n < 12:
            print('It will take', n, 'month to repay the loan')
        elif n == 12:
            print('It will take 1 year to repay the loan')
        elif n > 12 and n % 12 == 0:
            print('It will take', n // 12, 'years to repay the loan')
        else:
            print('It will take', n // 12, 'years and', n % 12, 'months to repay the loan')
    elif user_choice == 'a':
        a = int(math.ceil(count_annuity_payment(i, p, n)))
        print('Your annuity payment = {a}!' .format(a=a))
    elif user_choice == 'p':
        p = int(math.ceil(count_loan_principal(a, i, n)))
        print('Your loan principal = {p}!' .format(p=p))
    print('Overpayment = {overpayment}' .format(overpayment=int(a * n - p)))


if args.type == "annuity":
    if args.payment is None:
        get_annuity("a", args.principal, args.interest, args.periods, 0)
    elif args.principal is None:
        get_annuity("p", 0, args.interest, args.periods, args.payment)
    elif args.periods is None:
        get_annuity("n", args.principal, args.interest, 0, args.payment)
elif args.type == "diff":
    count_interest_payment(args.principal, args.interest, args.periods)
