# UMLS CUI & Semantic Type Data

This repo generates tabular and JSON-lines data on UMLS CUIs, concept names, semantic type names and abbreviations.

Tabular data example:

|CUI      |concept_name                        | semantic_type_name                    | semantic_type_abbreviation |
|---------|------------------------------------|---------------------------------------|----------------------------|
|C0000005 | (131)I-Macroaggregated Albumin     | Amino Acid, Peptide, or Protein       | aapp                       |
|C0000005 | (131)I-Macroaggregated Albumin     | Pharmacologic Substance               | phsu                       |
|C0000005 | (131)I-Macroaggregated Albumin     | Indicator, Reagent, or Diagnostic Aid | irda                       |
|C0000039 | 1,2-dipalmitoylphosphatidylcholine | Organic Chemical                      | orch                       |
|C0000039 | 1,2-dipalmitoylphosphatidylcholine | Pharmacologic Substance               | phsu                       |
|C0000052 | 1,4-alpha-Glucan Branching Enzyme  | Amino Acid, Peptide, or Protein       | aapp                       |
|C0000052 | 1,4-alpha-Glucan Branching Enzyme  | Enzyme                                | enzy                       | 
|C0000074 | 1-Alkyl-2-Acylphosphatidates       | Organic Chemical                      | orch                       |

JSON-lines data example (formatted for readability):

```json
{
    "CUI": "C0000005",
    "concept_name": "(131)I-Macroaggregated Albumin",
    "semantic_type": [
        {
            "name": "Amino Acid, Peptide, or Protein",
            "abbreviation": "aapp"
        },
        {
            "name": "Pharmacologic Substance",
            "abbreviation": "phsu"
        },
        {
            "name": "Indicator, Reagent, or Diagnostic Aid",
            "abbreviation": "irda"
        }
    ]
}
{
    "CUI": "C0000039",
    "concept_name": "1,2-dipalmitoylphosphatidylcholine",
    "semantic_type": [
        {
            "name": "Organic Chemical",
            "abbreviation": "orch"
        },
        {
            "name": "Pharmacologic Substance",
            "abbreviation": "phsu"
        }
    ]
}
{
    "CUI": "C0000052",
    "concept_name": "1,4-alpha-Glucan Branching Enzyme",
    "semantic_type": [
        {
            "name": "Amino Acid, Peptide, or Protein",
            "abbreviation": "aapp"
        },
        {
            "name": "Enzyme",
            "abbreviation": "enzy"
        }
    ]
}
{
    "CUI": "C0000103",
    "concept_name": "1-Naphthylisothiocyanate",
    "semantic_type": [
        {
            "name": "Organic Chemical",
            "abbreviation": "orch"
        },
        {
            "name": "Indicator, Reagent, or Diagnostic Aid",
            "abbreviation": "irda"
        },
        {
            "name": "Hazardous or Poisonous Substance",
            "abbreviation": "hops"
        }
    ]
}
```

## TODO List

- [ ] NIH License Requirement
- [ ] Publish as an API
- [ ] Add Equivalent IDs from Node Normalizer?
