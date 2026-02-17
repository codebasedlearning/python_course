# Unit 0x04 – AI Hints

## Hints

### Task 'AI Snapshot' – Protocol Match

- Correct idea: `Protocol` uses structural typing; inheritance is not required.
- Bug in Answer B: it treats `Protocol` like an ABC with nominal typing.
- Quick test: a class with the right methods should satisfy the protocol in type checking.

### Task 'AI Snapshot' – `runtime_checkable`

- Correct idea: `@runtime_checkable` enables `isinstance` checks for protocols.
- Bug in Answer B: without the decorator, `isinstance` should not be used for protocol checks.
- Quick test: `isinstance(Duck(), Quackable)` should be `True` only with `@runtime_checkable`.

### Task 'Comprehension Check'

- Q: Characterize 'single inheritance', 'multiple inheritance' and 'composition'. <br>
  A: Single inheritance has one base class, multiple inheritance has several, composition builds behavior by containing objects.
- Q: Characterize 'abstract classes', 'mixins' and 'protocols'. <br>
  A: Abstract classes define required methods, mixins add reusable behavior, protocols define structural interfaces.
- Q: What is 'nominal typing', 'structural typing' and 'duck typing'? <br>
  A: Nominal: explicit inheritance; structural: method shape matches; duck: runtime behavior only.
- Q: What is the famous phrase for 'duck typing'? And what does it mean? <br>
  A: If it walks like a duck and quacks like a duck, it is a duck. Behavior defines type.
- Q: What is the problem with the 'MRO' and calling the `super` function? <br>
  A: In diamond inheritance, incorrect `super()` usage can skip or duplicate calls.
- Q: What does `@runtime_checkable` enable for a `Protocol`? <br>
  A: It allows runtime `isinstance`/`issubclass` checks against the protocol.
- Q: When would you prefer composition over inheritance? <br>
  A: When you need flexibility without a strict is-a relationship or tight coupling.

