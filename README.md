# mezzanine_PU_fixing
Postprocessing of the ROG exb corpus after manual interventions

# Directory structure

```
├── manual_corrections
│   ├── Rog-Art-J-Gvecg-P500014.exb
│   └── Rog-Art-J-Gvecg-P500028.exb
└── Rog-Art-PU-popravljeno-mar2025.zip

```
* Rog-Art-PU-popravljeno-mar2025.zip : input data from annotators
* manual_corrections: the two exbs that were later ammended by annotators

The rest of the dir structure is constructed automatically when running it.

# 2025-04-08T11:17:36

Summary of what was done:
* If PU labels look like PU.tok123PU124, we take only the first token, i.e.
  PU.tok123
* For every PU not conforming to the naming convention, we try to find the token
  ID starting at the same time
* If not, label it as PU.XXX
* For PU.XXX, manual interventions were performed


Notably, no edits were done to assure that the prosodic units don't start before
the words do. This can introduce further issues when done automatically and
would require manual inspection.