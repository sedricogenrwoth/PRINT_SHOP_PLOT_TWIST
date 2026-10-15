"""The Print-Shop Plot Twist: the report is ready, but will it fit the budget?
Run: python3 story.py. Printing prices are invented classroom values.
"""
from abc import ABC, abstractmethod


# ACT 1: The print account owns its money and validates every public change.
class PrintCredit:
    def __init__(self, money):
        self.balance = money  # Use the setter from the first assignment.

    @property
    def balance(self):
        return self.__balance  # Name mangling, not encryption or a real vault.

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Print credit cannot be negative.")
        self.__balance = amount

    def pay(self, amount):
        if amount <= 0 or amount > self.balance:
            return False
        self.balance = self.balance - amount
        return True


# ACT 2: Every output option must quote a cost for the same report.
class OutputOption(ABC):
    currency = "UGX"  # Class attribute shared by the output family.

    def __init__(self, name):
        self.name = name  # Instance attribute.

    def describe(self):
        return f"{self.name} is available from the Mukono print desk."

    @abstractmethod
    def quote(self, pages):
        pass  # Can't instantiate OutputOption until this requirement is met.


class BlackAndWhite(OutputOption):  # IS-A OutputOption: single inheritance.
    def __init__(self, name="Black-and-white print", per_page=200):
        super().__init__(name)  # Parent handles the common name.
        self.per_page = per_page

    def quote(self, pages):
        return pages * self.per_page  # Concrete override.


class Colour(OutputOption):  # Same parent: hierarchical inheritance.
    def quote(self, pages):
        return pages * 1000


class StudentPrint(BlackAndWhite):  # Three levels: multilevel inheritance.
    def quote(self, pages):
        return max(0, super().quote(pages) - 200)  # First page sponsored.


# ACT 3: A reusable extra ability, combined with the print hierarchy.
class FriendlyMixin:
    def describe(self):
        return f"We believe in your report! {super().describe()}"


class FriendlyStudentPrint(FriendlyMixin, StudentPrint):
    pass  # Multiple + multilevel inheritance: hybrid. MRO determines super().


class PDFSubmission:  # Unrelated class with the same calling interface.
    name = "PDF for the group archive"

    def quote(self, pages):
        return 0

    def describe(self):
        return "PDF archive: zero printing cost, no paper to lose in a taxi."


# ACT 4: A report session HAS-A credit object and borrows an output option.
class ReportSession:
    def __init__(self, student, money):
        self.student = student
        self.credit = PrintCredit(money)  # Owned component: composition.
        self._outputs = []  # Single underscore: internal by convention.
        self.output = None

    @property
    def completed_outputs(self):  # Read-only, derived from actual successful outputs.
        return len(self._outputs)

    def produce(self, output, pages):
        if pages <= 0:
            return "A report needs at least one page. Nothing produced."
        self.output = output  # Borrowed/swappable collaborator: aggregation.
        cost = output.quote(pages)  # Abstraction: don't duplicate pricing here.
        if cost == 0 or self.credit.pay(cost):
            self._outputs.append(output)  # Keep a collection of collaborating objects.
            return f"{self.student} produces {output.name}: UGX {cost:,}."
        return f"{output.name} is over budget. The cover can survive without colour."


def compare_outputs(options, pages):  # Week 1 function + parameter + list + loop.
    for option in options:
        print(option.describe())
        print(f"Quote: UGX {option.quote(pages):,}")  # Same call: polymorphism.


def main():
    print("=== THE PRINT-SHOP PLOT TWIST ===")
    print("Nakato's report has 4 pages. Her budget is less colourful than the cover.")
    options = [BlackAndWhite(), Colour("Colour print"),
               FriendlyStudentPrint("Student black-and-white"), PDFSubmission()]
    compare_outputs(options, 4)  # PDFSubmission joins by duck typing.
    nakato = ReportSession("Nakato", 1000)
    okello = ReportSession("Okello", 800)  # Separate accounts and history lists.
    print(nakato.produce(options[1], 4))  # 4000: refused.
    print(nakato.produce(options[2], 4))  # 600.
    print(nakato.produce(options[3], 4))  # Swap output: archive costs zero.
    print(okello.produce(options[0], 4))  # 800.
    print(f"Nakato: UGX {nakato.credit.balance:,}; outputs: {nakato.completed_outputs}")
    print(f"Okello: UGX {okello.credit.balance:,}; outputs: {okello.completed_outputs}")
    print("MRO (look left to right):")
    for parent in FriendlyStudentPrint.__mro__:
        print(parent.__name__)
    print("Ending: report printed, PDF archived, and the group can finally exhale.")




# Extension 1: Binding charges UGX 500 for the whole job.
class Binding(OutputOption):
    def quote(self, pages):
        return 500

if __name__ == "__main__":
    main()