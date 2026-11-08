from datetime import date

due_date = date(2026, 1, 5)
today = date(2026, 1, 15)

difference = today - due_date

print("Due Date:", due_date)
print("Today:", today)
print("Days Past Due:", difference.days)