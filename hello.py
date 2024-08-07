weight = input("Enter weight: ")
unit = input("(K)g or (L)bs: ")
if unit.upper() == "K":
    print(str(int(weight)/2.205) + " lbs")
elif unit.upper() == "L":
    print(str(int(weight)*2.205) + " kg")
else:
    print("error")
