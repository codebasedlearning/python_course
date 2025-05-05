# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This snippet discusses policy-based design. """

# policy-based from https://realpython.com/inheritance-composition-python
#   see https://files.realpython.com/media/ic-inheritance-policies.0a0de2d42a25.jpg

from abc import ABC, abstractmethod


class Employee(ABC):
    def __init__(self, no, name):
        self.no, self.name = no, name


class PayrollPolicy(ABC):
    @abstractmethod
    def calculate_payroll(self): ...


class SalaryPolicy(PayrollPolicy):
    def __init__(self, weekly_salary):
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


class HourlyPolicy(PayrollPolicy):
    def __init__(self, hours_worked, hour_rate):
        self.hours_worked = hours_worked
        self.hour_rate = hour_rate

    def calculate_payroll(self):
        return self.hours_worked * self.hour_rate


class CommissionPolicy(SalaryPolicy):
    def __init__(self, weekly_salary, commission):
        super().__init__(weekly_salary)
        self.commission = commission

    def calculate_payroll(self):
        fixed = super().calculate_payroll()
        return fixed + self.commission


class RolePolicy(ABC):
    @staticmethod
    @abstractmethod
    def work(hours): ...


class ManagerRole(RolePolicy):
    @staticmethod
    def work(hours):
        return f'screams and yells for {hours} hours.'


class SecretaryRole(RolePolicy):
    @staticmethod
    def work(hours):
        return f'expends {hours} hours doing office paperwork.'


class SalesRole(RolePolicy):
    @staticmethod
    def work(hours):
        return f'expends {hours} hours on the phone.'


class FactoryRole(RolePolicy):
    @staticmethod
    def work(hours):
        return f'manufactures gadgets for {hours} hours.'


class Manager(Employee, ManagerRole, SalaryPolicy):
    def __init__(self, no, name, weekly_salary):
        SalaryPolicy.__init__(self, weekly_salary)
        super().__init__(no, name)


class Secretary(Employee, SecretaryRole, SalaryPolicy):
    def __init__(self, no, name, weekly_salary):
        SalaryPolicy.__init__(self, weekly_salary)
        super().__init__(no, name)


class SalesPerson(Employee, SalesRole, CommissionPolicy):
    def __init__(self, no, name, weekly_salary, commission):
        CommissionPolicy.__init__(self, weekly_salary, commission)
        super().__init__(no, name)


class FactoryWorker(Employee, FactoryRole, HourlyPolicy):
    def __init__(self, no, name, hours_worked, hour_rate):
        HourlyPolicy.__init__(self, hours_worked, hour_rate)
        super().__init__(no, name)


class TemporarySecretary(Employee, SecretaryRole, HourlyPolicy):
    def __init__(self, no, name, hours_worked, hour_rate):
        HourlyPolicy.__init__(self, hours_worked, hour_rate)
        super().__init__(no, name)


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
            print(f"    - '{employee.work(hours)}'")
        print()


def design_phase_policies():
    employees = [
        Manager(1, 'Mary Poppins', 3000),
        Secretary(2, 'John Smith', 1500),
        SalesPerson(3, 'Kevin Bacon', 1000, 250),
        FactoryWorker(4, 'Jane Doe', 40, 15),
        TemporarySecretary(5, 'Robin Williams', 40, 9),
    ]
    ProductivitySystem().track(employees, 40)
    PayrollSystem().calculate_payroll(employees)


if __name__ == "__main__":
    design_phase_policies()
