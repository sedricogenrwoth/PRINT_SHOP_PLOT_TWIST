"""The Print-Shop Plot Twist: the report is ready, but will it fit the budget?
Run: python3 story.py. Printing prices are invented classroom values.
"""
from abc import ABC, abstractmethod


# ACT 1: The print account owns its money and validates every public change.
class PrintCredit:
    def __init__(self, money):
        self.balance = money

    @property
    def balance(self):
        return self.__balance

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

    def top_up(self, amount):
        if amount <= 0:
            return False
        self.balance = self.balance + amount
        return True


# ACT 2: Every output option must quote a cost for the same report.
class OutputOption(ABC):
    currency = "UGX"

    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} is available from the Mukono print desk."

    @abstractmethod
    def quote(self, pages):
        pass


class BlackAndWhite(OutputOption):
    def __init__(self, name="Black-and-white print", per_page=200):
        super().__init__(name)
        self.per_page = per_page

    def quote(self, pages):
        return pages * self.per_page


class Colour(OutputOption):
    def __init__(self, name="Colour print", per_page=1000):
        super().__init__(name)
        self.per_page = per_page

    def quote(self, pages):
        return pages * self.per_page


class StudentPrint(BlackAndWhite):
    def quote(self, pages):
        return max(0, super().quote(pages) - 200)


# ACT 3: A reusable extra ability, combined with the print hierarchy.
class FriendlyMixin:
    def describe(self):
        return f"We believe in your report! {super().describe()}"


class FriendlyStudentPrint(FriendlyMixin, StudentPrint):
    pass


class PDFSubmission:
    name = "PDF for the group archive"

    def quote(self, pages):
        return 0

    def describe(self):
        return "PDF archive: zero printing cost, no paper to lose in a taxi."


class Binding(OutputOption):
    def __init__(self, name="Simple binding"):
        super().__init__(name)

    def quote(self, pages):
        return 500


class EmailCopy:
    def __init__(self, name="Email report"):
        self.name = name

    def quote(self, pages):
        return 0

    def describe(self):
        return f"{self.name} is delivered electronically at no printing cost."


class CoveredPrint(StudentPrint):
    def quote(self, pages):
        return super().quote(pages) + 300


# ACT 4: A report session HAS-A credit object and borrows an output option.
class ReportSession:
    def __init__(self, student, money):
        self.student = student
        self.credit = PrintCredit(money)
        self._outputs = []
        self.output = None

    @property
    def completed_outputs(self):
        return len(self._outputs)

    def produce(self, output, pages):
        if pages <= 0:
            return "A report needs at least one page. Nothing produced."
        self.output = output
        cost = output.quote(pages)
        if cost == 0 or self.credit.pay(cost):
            self._outputs.append(output)
            return f"{self.student} produces {output.name}: UGX {cost:,}."
        return f"{output.name} is over budget. The cover can survive without colour."

    def receipt(self):
        return {
            "student": self.student,
            "successful_outputs": [output.name for output in self._outputs],
            "count": self.completed_outputs,
            "remaining_credit": self.credit.balance,
        }


def compare_outputs(options, pages):
    for option in options:
        print(option.describe())
        print(f"Quote: UGX {option.quote(pages):,}")


def cheapest_output(options, pages):
    if not options:
        return None
    return min(options, key=lambda option: option.quote(pages))


def main():
    print("=== THE PRINT-SHOP PLOT TWIST ===")
    print("Nakato's report has 4 pages. Her budget is less colourful than the cover.")
    options = [
        BlackAndWhite(),
        Colour("Colour print"),
        FriendlyStudentPrint("Student black-and-white"),
        PDFSubmission(),
    ]
    compare_outputs(options, 4)
    nakato = ReportSession("Nakato", 1000)
    okello = ReportSession("Okello", 800)
    print(nakato.produce(options[1], 4))
    print(nakato.produce(options[2], 4))
    print(nakato.produce(options[3], 4))
    print(okello.produce(options[0], 4))
    print(f"Nakato: UGX {nakato.credit.balance:,}; outputs: {nakato.completed_outputs}")
    print(f"Okello: UGX {okello.credit.balance:,}; outputs: {okello.completed_outputs}")
    print("MRO (look left to right):")
    for parent in FriendlyStudentPrint.__mro__:
        print(parent.__name__)
    print("Ending: report printed, PDF archived, and the group can finally exhale.")

    print("\n=== EXTENSION: Binding ===")
    binding = Binding("Simple binding")
    session = ReportSession("Nakato", 1000)
    print("Expected quote: UGX 500")
    print("Actual quote:", binding.quote(4))
    print("Expected: successful production")
    print("Actual:", session.produce(binding, 4))
    print("Expected balance: UGX 500")
    print("Actual balance:", session.credit.balance)

    empty_session = ReportSession("Nakato", 1000)
    print("\nExpected: zero pages refused")
    print("Actual:", empty_session.produce(binding, 0))
    print("Expected balance: UGX 1000")
    print("Actual balance:", empty_session.credit.balance)

    print("\n=== EXTENSION: Top up ===")
    credit = PrintCredit(500)
    print("Expected: True")
    print("Actual:", credit.top_up(300))
    print("Expected balance: UGX 800")
    print("Actual balance:", credit.balance)

    credit2 = PrintCredit(500)
    print("\nExpected: False")
    print("Actual:", credit2.top_up(0))
    print("Expected balance: UGX 500")
    print("Actual balance:", credit2.balance)

    print("\n=== EXTENSION: Email copy ===")
    email = EmailCopy()
    compare_outputs([email], 4)

    session = ReportSession("Nakato", 1000)
    print("\nExpected: successful output costing UGX 0")
    print("Actual:", session.produce(email, 4))
    print("Expected balance: UGX 1000")
    print("Actual balance:", session.credit.balance)

    session2 = ReportSession("Nakato", 1000)
    print("\nExpected: zero pages refused")
    print("Actual:", session2.produce(email, 0))
    print("Expected outputs: 0")
    print("Actual outputs:", session2.completed_outputs)

    print("\n=== EXTENSION: Cheapest output ===")
    options = [
        BlackAndWhite(),
        Colour("Colour print"),
        StudentPrint("Student print"),
        PDFSubmission(),
    ]
    winner = cheapest_output(options, 4)
    print("Expected: PDF for the group archive")
    print("Actual:", winner.name if winner else None)

    session = ReportSession("Nakato", 1000)
    before_balance = session.credit.balance
    before_count = session.completed_outputs
    cheapest_output(options, 4)
    print("\nExpected balance unchanged:", before_balance)
    print("Actual balance:", session.credit.balance)
    print("Expected output count unchanged:", before_count)
    print("Actual output count:", session.completed_outputs)
    print("\nExpected: None")
    print("Actual:", cheapest_output([], 4))

    print("\n=== EXTENSION: Receipt ===")
    session = ReportSession("Nakato", 1000)
    session.produce(StudentPrint("Student print"), 4)
    session.produce(PDFSubmission(), 4)
    print("Expected receipt: Nakato, 2 outputs, UGX 400 remaining")
    print("Actual receipt:", session.receipt())
    before_balance = session.credit.balance
    before_count = session.completed_outputs
    print("\nExpected balance unchanged:", before_balance)
    print("Actual balance:", session.credit.balance)
    print("Expected count unchanged:", before_count)
    print("Actual count:", session.completed_outputs)

    empty_session = ReportSession("Okello", 800)
    print("\nExpected count: 0")
    print("Actual count:", empty_session.receipt()["count"])
    print("Expected remaining credit: UGX 800")
    print("Actual remaining credit:", empty_session.receipt()["remaining_credit"])

    print("\n=== EXTENSION: Covered print ===")
    covered = CoveredPrint("Student print with cover")
    compare_outputs([covered], 4)

    session = ReportSession("Nakato", 1000)
    print("\nExpected quote: UGX 900")
    print("Actual quote:", covered.quote(4))
    print("Expected: successful production")
    print("Actual:", session.produce(covered, 4))
    print("Expected balance: UGX 100")
    print("Actual balance:", session.credit.balance)

    session2 = ReportSession("Okello", 800)
    print("\nExpected: production refused")
    print("Actual:", session2.produce(covered, 4))
    print("Expected balance: UGX 800")
    print("Actual balance:", session2.credit.balance)
    print("Expected outputs: 0")
    print("Actual outputs:", session2.completed_outputs)


if __name__ == "__main__":
    main()
