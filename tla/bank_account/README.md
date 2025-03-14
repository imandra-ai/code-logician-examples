https://old.learntla.com/introduction/example/

Consider a banking system with two clients, Alice and Bob, each maintaining individual account balances. Our task is to model a money transfer system where Alice wishes to transfer funds to Bob. How can we effectively model this scenario?

To ensure the robustness of our money transfer system, we will analyze its safety properties. Specifically, we will examine two distinct transfer mechanisms: standard transfers and safety-checked transfers that verify available balance. Our primary verification goal is to ensure that Alice's account balance remains non-negative throughout any transfer operation.
