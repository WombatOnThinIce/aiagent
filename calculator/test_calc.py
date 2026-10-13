# Test that the fix works
from pkg.calculator import Calculator

c = Calculator()
result = c.evaluate("3 + 7 * 2")
print(f"3 + 7 * 2 = {result}")
assert result == 17.0, f"Expected 17.0, got {result}"
print("✓ Bug fixed: 3 + 7 * 2 now correctly equals 17, not 20")
