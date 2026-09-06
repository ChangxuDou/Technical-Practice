high_income = False
good_credit = True
student = True
if high_income or (good_credit and student):
    print("Eligible for loan")
else:
    print("Not eligible for loan")

# in Python,logical operators are short-circuit evaluated.
