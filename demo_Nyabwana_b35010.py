from story import EmailCopy, ReportSession, compare_outputs

email = EmailCopy()

# Normal case
compare_outputs([email], 4)

session = ReportSession("Nakato", 1000)
print("\nExpected: successful output costing UGX 0")
print("Actual:", session.produce(email, 4))
print("Expected balance: UGX 1000")
print("Actual balance:", session.credit.balance)

# Boundary case
session2 = ReportSession("Nakato", 1000)
print("\nExpected: zero pages refused")
print("Actual:", session2.produce(email, 0))
print("Expected outputs: 0")
print("Actual outputs:", session2.completed_outputs)