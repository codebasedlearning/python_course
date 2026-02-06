# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This snippet discusses component-based design. """

# composition design from https://realpython.com/inheritance-composition-python
#   see https://files.realpython.com/media/ic-policy-based-composition.6e78bdb5824f.jpg

from abc import ABC, abstractmethod


class Employee:
    def __init__(self, no, name, role, payroll):
        self.no = no
        self.name = name
        self.role = role
        self.payroll = payroll

    def work(self, hours):
        duties = self.role.perform_duties(hours)
        print(f'Employee {self.no} - {self.name}:')
        print(f'- {duties}')
        self.payroll.track_work(hours)

    def calculate_payroll(self):
        return self.payroll.calculate_payroll()


class PayrollPolicy(ABC):
    def __init__(self):
        self.hours_worked = 0

    def track_work(self, hours):
        self.hours_worked += hours

    @abstractmethod
    def calculate_payroll(self):
        ...


class SalaryPolicy(PayrollPolicy):
    def __init__(self, weekly_salary):
        super().__init__()
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


class HourlyPolicy(PayrollPolicy):
    def __init__(self, hour_rate):
        super().__init__()
        self.hour_rate = hour_rate

    def calculate_payroll(self):
        return self.hours_worked * self.hour_rate


class CommissionPolicy(SalaryPolicy):
    def __init__(self, weekly_salary, commission_per_sale):
        super().__init__(weekly_salary)
        self.commission_per_sale = commission_per_sale

    @property
    def commission(self):
        sales = self.hours_worked / 5
        return sales * self.commission_per_sale

    def calculate_payroll(self):
        fixed = super().calculate_payroll()
        return fixed + self.commission


class ManagerRole:
    @staticmethod
    def perform_duties(hours):
        return f'screams and yells for {hours} hours.'

class SecretaryRole:
    @staticmethod
    def perform_duties(hours):
        return f'does paperwork for {hours} hours.'

class SalesRole:
    @staticmethod
    def perform_duties(hours):
        return f'expends {hours} hours on the phone.'

class FactoryRole:
    @staticmethod
    def perform_duties(hours):
        return f'manufactures gadgets for {hours} hours.'


class PayrollSystem:
    @staticmethod
    def calculate_payroll(employees):
        print(f"0a| calculating payroll:")
        for employee in employees:
            print(f"    - '{employee.name}' ({employee.no}) -> {employee.calculate_payroll()}")


class ProductivitySystem:
    @staticmethod
    def track(employees, hours):
        print(f"0b| tracking productivity:")
        for employee in employees:
            employee.work(hours)
        print()


def design_phase_composition():
    # plus DI (DI via ctor inj.)
    employees = [
        Employee(1, 'Mary Poppins', ManagerRole(), SalaryPolicy(weekly_salary=3000)),
        Employee(2, 'John Smith', SecretaryRole(), SalaryPolicy(weekly_salary=1500)),
        Employee(3, 'Kevin Bacon', SalesRole(), CommissionPolicy(weekly_salary=1000, commission_per_sale=250)),
        Employee(4, 'Jane Doe', FactoryRole(), HourlyPolicy(hour_rate=15)),
        Employee(5, 'Robin Williams', SecretaryRole(), HourlyPolicy(hour_rate=9)),
    ]
    ProductivitySystem().track(employees, 40)
    PayrollSystem().calculate_payroll(employees)


if __name__ == "__main__":
    design_phase_composition()
