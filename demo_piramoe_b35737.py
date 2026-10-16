from story import PrintCredit

# Normal case
credit = PrintCredit(500)
print("Expected: True")
print("Actual:", credit.top_up(300))
print("Expected balance: UGX 800")
print("Actual balance:", credit.balance)

# Boundary case
credit2 = PrintCredit(500)
print("\nExpected: False")
print("Actual:", credit2.top_up(0))
print("Expected balance: UGX 500")
print("Actual balance:", credit2.balance)