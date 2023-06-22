import math
# First we must found out what type of calculation that the user wants to make. They can choose between investment and bond
calculation_type = input("Enter either \"investment\" or \"bond\" depending on which type of interest calculation you would like to make: ")

# Depending on what the user has inputted, the calculator will ask for different information in order to actually make the calculation
# If the user has selected investment, the calculator will then ask for the following information:
if calculation_type.lower() == "investment": 
    deposit_amount = float(input("Please enter how much money in £s are you despositing: "))
    investment_interest = float(input("Please enter the interest rate (%): "))
    years = int(input("Please enter how many years you will be investing this deposit for: "))
    interest = input("Please enter \"simple\" for simple enterest or enter \"compound\" for compound interest: ")

# Now the user has another choice to make about the type of interest they would like to make
# If the user picks simple then it is calculated:
    if interest.lower() == "simple":
          calculation = deposit_amount * (1 + (investment_interest/ 100)* years)
#If they pick compound it calculate compound interest instead
    elif interest.lower() == "compound":
          calculation = deposit_amount * math.pow((1 + (investment_interest / 100)),years)
# Then print the calculation
    print("Your total amount will be: £ {:.2f} " .format(calculation))     



#If the user has selected bond, the calculator will then ask for the following information:
elif calculation_type.lower() == "bond": 
    present_value = float(input("Please enter the present value of the house in £s: "))
    bond_interest = float(input("Please enter the interest rate (%): "))
    months = int(input("Please enter how many months you plan you plan on taking to repay the bond: "))
                 
#Now this will be calculated
    repayment = (bond_interest / 12) * present_value / (1 - (1 + (bond_interest / 12)) ** (-months))
#Then printed
    print("Your total amount will be: £ {:.2f} " .format(repayment)) 

# If the user does not put in "investment" or "bond" then the calculator will give an error
else:
    print("Input not accepted, please enter \"investment\" or \"bond\" to continue ")
