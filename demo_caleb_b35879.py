from story import ReportSession, StudentPrint, PDFSubmission

session = ReportSession("Nakato", 1000)
session.produce(StudentPrint("Student print"), 4)
session.produce(PDFSubmission(), 4)

# Normal case
before_balance = session.credit.balance
before_count = session.completed_outputs

print("Expected receipt: Nakato, 2 outputs, UGX 400 remaining")
print("Actual receipt:", session.receipt())

# Read-only check
print("\nExpected balance unchanged:", before_balance)
print("Actual balance:", session.credit.balance)
print("Expected count unchanged:", before_count)
print("Actual count:", session.completed_outputs)

# Boundary case
empty_session = ReportSession("Okello", 800)
print("\nExpected count: 0")
print("Actual count:", empty_session.receipt()["count"])
print("Expected remaining credit: UGX 800")
print("Actual remaining credit:",
      empty_session.receipt()["remaining_credit"])