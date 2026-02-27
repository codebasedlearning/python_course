# Unit 0x04 – AI Hints

## Hints

### AI 'Off-By-One Imp' – Prompt Refinement: Protocol

- The AI's answer is not wrong but misses the key point: `Protocol` uses structural typing.
- A class does NOT need to inherit from a Protocol to satisfy it — that's the whole point.
- Quick test: a class with a `draw()` method satisfies `Drawable` without inheriting from it.

### AI 'Off-By-One Imp' – AI Said It's Fine: isinstance and Protocol

- Code crashes at runtime: `TypeError: Protocols with non-method members can't be used with isinstance()`.
- Fix: add `@runtime_checkable` decorator to the `Quackable` Protocol.
- Sneaky because it compiles fine and even passes mypy — only crashes at runtime.
- `isinstance` with `@runtime_checkable` only checks method names, not full signatures.

### Task 'Comprehension Check'

- Q: Characterize 'single inheritance', 'multiple inheritance' and 'composition'. <br>
  A: Single inheritance has one base class, multiple inheritance has several, composition builds
  behavior by containing objects.
- Q: Characterize 'abstract classes', 'mixins' and 'protocols'. <br>
  A: Abstract classes define required methods, mixins add reusable behavior, protocols define
  structural interfaces.
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
