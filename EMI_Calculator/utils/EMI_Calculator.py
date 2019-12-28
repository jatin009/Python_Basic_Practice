from utils import date_functionality


class EMI_Calculator:
    """ Simple class to calculate EMI and Total repayment for a loan """

    def __init__(self, principal, tenure, interest, last_repayment_date, accumulated_month_emi=0, cumulative_interest_paid = 0):
        self._principal = principal
        self._tenure = tenure
        self._interest = interest
        self._last_repayment_date = last_repayment_date
        self._accumulated_month_amt = accumulated_month_emi
        self._cumulative_interest_paid = cumulative_interest_paid

    @property
    def principal(self):
        return self._principal

    @property
    def tenure(self):
        return self._tenure

    @property
    def interest(self):
        return self._interest

    @property
    def repayment_date(self):
        return self._last_repayment_date

    @property
    def accumulated_month_amt(self):
        return self._accumulated_month_amt

    @property
    def cumulative_interest_paid(self):
        return self._cumulative_interest_paid

    @property
    def total_repayment(self):
        """ Total amount that you'll eventually pay """
        return self.emi*self._tenure*12

    @property
    def emi(self):
        """ Equated monthly installment EMI = (P*R/1200)*(x/(x-1)) where x = pow((1 + R/1200), 12*tenure) """
        monthly_rate = self._interest/1200
        calc_factor = pow((1 + monthly_rate), self._tenure*12)
        return (self._principal * monthly_rate)*(calc_factor)/(calc_factor-1)

    def repay(self, inst, repay_date):
        """ Repayment of loan at given repay date and installment """
        diff_in_month = date_functionality.month_diff(repay_date, self._last_repayment_date)

        if diff_in_month < 0:
            return "Repay date provided is less than the previous repayment date. Please try again"

        # if more than one payments made within the same month
        if diff_in_month == 0:
            self._accumulated_month_amt += inst
            self._last_repayment_date = repay_date
            return "Your installment successfully saved for the current month."

        elif diff_in_month >= 1 :

            output_list = []
            while diff_in_month >= 1:
                
                curr_interest = self._principal * self._interest/1200
                curr_principal_repayment = self._accumulated_month_amt - curr_interest
                curr_installment = self._accumulated_month_amt
                self._principal -= curr_principal_repayment
                self._cumulative_interest_paid += curr_interest

                curr_month_details = {'installment': curr_installment, 'month_interest': curr_interest, 'last_repayment_date': self._last_repayment_date,
                        'month_principal': curr_principal_repayment, 'remaining_principal': self._principal, 'cumulative_interest_paid': self._cumulative_interest_paid}

                if date_functionality.month_diff(repay_date, self._last_repayment_date) == 1:
                    self._accumulated_month_amt = inst
                    self._last_repayment_date = repay_date                    
                else:
                    self._accumulated_month_amt = 0
                    self._last_repayment_date = date_functionality.add_month(self._last_repayment_date, 1)

                diff_in_month = date_functionality.month_diff(repay_date, self._last_repayment_date)
                output_list.append(curr_month_details)
                
            return output_list
        

    def __repr__(self):
        return f"EMICalculator: Principal Rs. {self._principal} for tenure of {self._tenure} years at interest {self._interest}%p.a."

