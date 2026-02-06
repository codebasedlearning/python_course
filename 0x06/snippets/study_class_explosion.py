# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

""" This snippet deals with the problem of class explosions in inheritance. """


# class diagram from https://realpython.com/inheritance-composition-python
#   see https://files.realpython.com/media/ic-initial-employee-inheritance.b5f1e65cb8d1.jpg

from abc import ABC, abstractmethod


class Employee(ABC):
    def __init__(self, no, name):
        self.no, self.name = no, name

    @abstractmethod
    def calculate_payroll(self): ...


class SalaryEmployee(Employee):
    def __init__(self, no, name, weekly_salary):
        super().__init__(no, name)
        self.weekly_salary = weekly_salary

    def calculate_payroll(self): return self.weekly_salary


class HourlyEmployee(Employee):
    def __init__(self, no, name, hours_worked, hour_rate):
        super().__init__(no, name)
        self.hours_worked, self.hour_rate = hours_worked, hour_rate

    def calculate_payroll(self): return self.hours_worked * self.hour_rate


class CommissionEmployee(SalaryEmployee):
    def __init__(self, no, name, weekly_salary, commission):
        super().__init__(no, name, weekly_salary)
        self.commission = commission

    def calculate_payroll(self): return super().calculate_payroll() + self.commission


class PayrollSystem:
    @staticmethod
    def calculate_payroll(employees):
        print(f"0a| calculating payroll:")
        for employee in employees:
            print(f"    - '{employee.name}' ({employee.no}) -> {employee.calculate_payroll()}")


# class explosion from https://realpython.com/inheritance-composition-python
#   see https://files.realpython.com/media/ic-class-explosion.a3d42b8c9b91.jpg
#   and https://files.realpython.com/media/ic-diamond-problem.8e685f12d3c2.jpg

class Manager(SalaryEmployee):
    def work(self, hours):
        print(f'{self.name} screams and yells for {hours} hours.')


class Secretary(SalaryEmployee):
    def work(self, hours):
        print(f'{self.name} expends {hours} hours doing office paperwork.')


class SalesPerson(CommissionEmployee):
    def work(self, hours):
        print(f'{self.name} expends {hours} hours on the phone.')


class FactoryWorker(HourlyEmployee):
    def work(self, hours):
        print(f'{self.name} manufactures gadgets for {hours} hours.')

#class TemporarySecretary(Secretary, HourlyEmployee):
#    pass
#class TemporarySecretary(HourlyEmployee, Secretary):
#    pass
#class TemporarySecretary(HourlyEmployee, Secretary):
#    def __init__(self, id, name, hours_worked, hour_rate):
#        super().__init__(id, name, hours_worked, hour_rate)


class TemporarySecretary(Secretary, HourlyEmployee):
    def __init__(self, id, name, hours_worked, hour_rate):
        HourlyEmployee.__init__(self, id, name, hours_worked, hour_rate)

    def calculate_payroll(self):
        return HourlyEmployee.calculate_payroll(self)


class ProductivitySystem:
    @staticmethod
    def track(employees, hours):
        print(f"0b| tracking productivity:")
        for employee in employees:
            employee.work(hours)
        print()


def design_phase_payroll():
    PayrollSystem().calculate_payroll([
        SalaryEmployee(1, 'John Smith', weekly_salary=1500),
        HourlyEmployee(2, 'Jane Doe', hours_worked=40, hour_rate=15),
        CommissionEmployee(3, 'Kevin Bacon', weekly_salary=1000, commission=250),
    ])


def design_phase_work():
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
    design_phase_payroll()
    design_phase_work()
