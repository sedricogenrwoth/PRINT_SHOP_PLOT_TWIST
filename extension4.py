# Extension 4: Return the cheapest option without producing a report.
def cheapest_output(options, pages):
    if not options:
        return None

    return min(options, key=lambda option: option.quote(pages))
from story import (
    BlackAndWhite, Colour, StudentPrint, PDFSubmission,
    cheapest_output, ReportSession
)

options = [
    BlackAndWhite(),
    Colour("Colour print"),
    StudentPrint("Student print"),
    PDFSubmission()
]

# Normal case
winner = cheapest_output(options, 4)
print("Expected: PDF for the group archive")
print("Actual:", winner.name if winner else None)

# Read-only check
session = ReportSession("Nakato", 1000)
before_balance = session.credit.balance
before_count = session.completed_outputs

cheapest_output(options, 4)

print("\nExpected balance unchanged:", before_balance)
print("Actual balance:", session.credit.balance)
print("Expected output count unchanged:", before_count)
print("Actual output count:", session.completed_outputs)

# Boundary case
print("\nExpected: None")
print("Actual:", cheapest_output([], 4))
    
    