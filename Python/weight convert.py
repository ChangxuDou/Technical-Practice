weight = int(input('please input your weight:'))
unit = input ("(L)bs or (K)g:")
if unit.upper() ==  "L":
    weight_new = weight * 0.45
    print(weight_new)
    print(f"your weight is {weight_new} kg")
elif unit.upper() == "K":
    weight_new = weight / 0.45
    print(f"your weight is {weight_new} pounds")