[Analyzing the UBS Dark Pool](https://docs.imandra.ai/imandra-docs/notebooks/ubs-case-study/)

In this example, we model the order priority logic of the UBS ATS dark pool as described in UBS's [June 1st 2015 Form ATS submission to the SEC](https://storage.googleapis.com/imandra-notebook-assets/Form-ATS-June15.pdf) and analyse it using Imandra.

We observe that as described, the order priority logic suffers from a fundamental flaw: the order ranking function is not *transitive*.





