# Unit 0x_tra_gropros – AI Hints

## Hints

### Task 'Design Memo'

- Keep it short: 1 page is enough if structured.
- IPO helps: Inputs, Processing, Outputs.
- Add a test plan: smoke tests, edge cases, and one performance check.

### AI 'Off-By-One Imp' – SRP Design

- Correct idea: split responsibilities (`PricingPolicy`, `Receipt`, `Station`).
- Bug in Answer B: one large class violates SRP and is hard to change.
- Quick test: list changes that would force the giant class to be edited.

### AI 'Off-By-One Imp' – Dependency Inversion

- Correct idea: depend on an abstraction (protocol/ABC), not a concrete DB.
- Bug in Answer B: direct dependencies make swapping implementations harder.
- Quick test: imagine replacing `MySQLDatabase` with a mock in tests.

### Task 'Comprehension Check'

- Q: How would you build a solution for a GroPro? <br>
  A: Clarify requirements, plan with IPO, design classes, then implement and test.
- Q: What can you prepare in advance? <br>
  A: Templates for IO, data parsing, testing, and common utilities.
- Q: How does the IPO approach help structure a solution? <br>
  A: It separates input, processing, and output to keep logic clear.
- Q: Give one example of a Single Responsibility Principle (SRP) violation. <br>
  A: A class that handles parsing, business logic, and UI output all together.
