from story import Binding, ReportSession

binding = Binding("Simple binding")

# Normal case
session = ReportSession("Nakato", 1000)
print("Expected quote: UGX 500")
print("Actual quote:", binding.quote(4))
print("Expected: successful production")
print("Actual:", session.produce(binding, 4))
print("Expected balance: UGX 500")
print("Actual balance:", session.credit.balance)

# Boundary case
empty_session = ReportSession("Nakato", 1000)
print("\nExpected: zero pages refused")
print("Actual:", empty_session.produce(binding, 0))
print("Expected balance: UGX 1000")
print("Actual balance:", empty_session.credit.balance)