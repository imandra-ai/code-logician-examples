Financial exchanges and other venues like 'dark pools' and MTFs operate notoriously complex trading systems. In this example, we'll use Imandra's Region Decomposition feature to enumerate all of the 'edge-cases' of a component of the SIX Swiss trading logic (as described [here](https://www.six-group.com/dam/download/sites/education/preparatory-documentation/trading-module/trading-on-ssx-module-1-trading-en.pdf)).


In particular, we will use Imandra to:
  - Model a fragment of the logic (the one dealing with fill price determination)
  - Decompose the state-space of the logic to enumerate all of its regions (or 'edge cases')