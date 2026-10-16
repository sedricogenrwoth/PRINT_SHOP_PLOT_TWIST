from story import CoveredPrint, ReportSession, compare_outputs

covered = CoveredPrint("Student print with cover")

# Normal case
compare_outputs([covered], 4)

session = ReportSession("Nakato", 1000)
print("\nExpected quote: UGX 900")
print("Actual quote:", covered.quote(4))
print("Expected: successful production")
print("Actual:", session.produce(covered, 4))
print("Expected balance: UGX 100")
print("Actual balance:", session.credit.balance)

# Refused case
session2 = ReportSession("Okello", 800)
print("\nExpected: production refused")
print("Actual:", session2.produce(covered, 4))
print("Expected balance: UGX 800")
print("Actual balance:", session2.credit.balance)
print("Expected outputs: 0")
print("Actual outputs:", session2.completed_outputs)