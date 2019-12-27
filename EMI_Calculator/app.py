from utils.EMI_Calculator import EMI_Calculator
from utils.date_functionality import *
import json


def take_loan_input():
    try:
        p = float(input("\n\nPrincipal amount: "))
        r = float(input("Rate of interest (in %pa): "))
        t = float(input("Loan tenure (in yrs): "))
        d = date_input("01/" + input("Please input loan repayment commencement month-year(in MM/YYYY format): "))

        if not d:
            raise ValueError
        
    except ValueError:
        print("Principal, Interest and Tenure should be integer of float values. And yes, date in the mentioned format only :) Please try again.")
    else:
        return {'p':p, 'r':r, 't':t, 'd':d}


def process_new_loan(loan):
    
        homeloan_emi = EMI_Calculator(loan['p'], loan['t'], loan['r'], loan['d'])

        print(f"\nEMI: {homeloan_emi.emi:,.2f}")
        print(f"Total Repayment: {homeloan_emi.total_repayment:,.2f}\n")

        obj_for_json = {'base_values': {'principal': loan['p'], 'tenure': loan['t'], 'interest': loan['r'], 'commencement_date': date_conversion(DateFormat.YEAR_MON_DAY, loan['d'])}}
        obj_for_json = keep_paying(homeloan_emi, obj_for_json)

        save = input("You wish to save the loan repayments in a file (y/n): ")

        if save == 'y':
            with open('utils/loan.json', 'w') as file:
                json.dump(obj_for_json, file)
        return


def estimated_time_loan_completion(homeloan_emi):
    try:
        estimate_emi = float(input("Input the emi you wish to deposit every month: "))
    except ValueError:
        print("Kindly provide valid float or integer values only.")
    else:
        completion_output = []
        while homeloan_emi.principal > 1:
            completion_output = homeloan_emi.repay(estimate_emi, add_month(homeloan_emi.repayment_date, 1))

        if len(completion_output) > 0:
            print(f"You shall be able to waive off the full loan by {date_conversion(DateFormat.MON_YEAR, completion_output[0]['last_payment_date'])} if you pay an emi of Rs. {estimate_emi:,.2f} every month.")


def estimated_emi_loan_completion(homeloan_emi):

    last_repayment_date = date_input( "01/" + input("Please input month-year by which you wish your loan to be ended(in MM/YYYY format): "))

    rem_months = month_diff(last_repayment_date, homeloan_emi.repayment_date)
    monthly_rate = homeloan_emi.interest/1200
    
    calc_factor = pow((1+monthly_rate), rem_months)
    emi = (homeloan_emi.principal*monthly_rate)*(calc_factor)/(calc_factor-1)
    print(f"You require an EMI of Rs. {emi} per month till {date_conversion(DateFormat.MON_YEAR, last_repayment_date)}")


def keep_paying(homeloan_emi, obj_for_json):
    
    key_input = 'n'
    month_installment = []

    while key_input == 'n':

        repay_date = date_input(input("Repayment date(DD/MM/YYYY): "))
        if not repay_date:
            continue

        try:
            amt_input = float(input("Repayment amount: "))
        except ValueError:
            print("Input float values for repay amount. Please try again.")
            continue

        output_repayment = homeloan_emi.repay(amt_input, repay_date)

        if isinstance(output_repayment, list):
            
            for month_output in output_repayment:
                print(f"Repayment for {date_conversion(DateFormat.MON_YEAR, month_output['last_repayment_date'])}: \nActual EMI paid: {month_output['installment']:,.2f} | Interest: {month_output['month_interest']:,.2f} | Repayment Principal: {month_output['month_principal']:,.2f} | Remaining Principal: {month_output['remaining_principal']:,.2f}\n\n")

                month_output['last_repayment_date'] = date_conversion(DateFormat.YEAR_MON_DAY, month_output['last_repayment_date'])
                month_installment.append(month_output)

        else:
            print(output_repayment + "\n\n")

        key_input = input("Keep pressing 'n' for next repayment: ")

        if key_input != 'n' and len(month_installment) > 0:

            obj_for_json['installments'].extend(month_installment)
            obj_for_json['remaining_values'] = {'principal': homeloan_emi.principal, 'tenure': homeloan_emi.tenure, 'interest': homeloan_emi.interest,
                                  'last_repayment_date': date_conversion(DateFormat.YEAR_MON_DAY, homeloan_emi.repayment_date),
                                                'accumulated_month_emi': homeloan_emi.accumulated_month_amt, 'cumulative_interest_paid': homeloan_emi.cumulative_interest_paid}
            return obj_for_json


def menu():

    print("Welcome to the EMI Calculator program!\n")
    choice = ''
    while choice.lower() != 'exit':

        choice = input("""We provide following facilities:
    - Start a new loan (new)
    - Repay an existing loan (repay)
    - Exit (exit)
    """)

        if choice.lower() == 'repay':

            try:
                with open('utils/loan.json', 'r') as file:
                    loan_obj = json.load(file)
            except FileNotFoundError:
                print("\nLooks like nothing to repay, better start a fresh loan :)\n")
                continue

            
            p = loan_obj['remaining_values']['principal']
            r = loan_obj['remaining_values']['interest']
            t = loan_obj['remaining_values']['tenure']
            d = date_input(loan_obj['remaining_values']['last_repayment_date'], DateFormat.YEAR_MON_DAY)
            e = loan_obj['remaining_values']['accumulated_month_emi']
            c = loan_obj['remaining_values']['cumulative_interest_paid']
            homeloan_emi = EMI_Calculator(p, t, r, d, e, c)

            print(f"""\n\nYour loan details are:
    Remaining Principal: {homeloan_emi.principal:,.2f}
    Interest Paid Till Date: {homeloan_emi.cumulative_interest_paid:,.2f}
    Loan Tenure: {homeloan_emi.tenure} yrs
    Loan Interest: {homeloan_emi.interest}% p.a.
    Last accumulated emi: {homeloan_emi.accumulated_month_amt:,.2f}
    Made on: {date_conversion(DateFormat.DAY_MON_YEAR, homeloan_emi.repayment_date)}""")

            option = ''

            while option != 'g':

                option = input("""\n\n- Continue repayment (r)
- Given an emi, get an estimate by when will you be loan-free (e)
- Given last repayment month, emi required to be loan-free by then (m)
- Go to main menu (g)
""")                
                if option == 'r':        
                    obj_for_json = keep_paying(homeloan_emi, loan_obj)

                    with open('utils/loan.json', 'w') as file:
                        json.dump(obj_for_json, file)

                elif option == 'e':
                    local_obj = EMI_Calculator(p, t, r, d, e)
                    estimated_time_loan_completion(local_obj)

                elif option == 'm':
                    local_obj = EMI_Calculator(p, t, r, d, e)
                    estimated_emi_loan_completion(local_obj)
        
        elif choice.lower() == 'new':

            loan_details = None
            while not loan_details:
                loan_details = take_loan_input()

            process_new_loan(loan_details)


menu()
