# Fungal analysis toolkits
* Assembly
* Annotation
* Phylogenetics

# Todo

### Reproducibility
* Conda export and pack environment for reusability
* Containerise application / version source code for manuscript

### Feature additions
* Implement error handling for assembly pipeline
* Build out annotation pipeline
* Build out phylogeny pipeline

### Docs
* Contributing file + rules
* Conventions for python files: functions, pipelines, classes, decorators
* docs/ [Assembly, Annotation, Phylogeny] modules

### Phylogenetics best practices?
* Fungal phylogeny best practices for WGS
    - Orthofinder + BUSCO ? (Ortholog inference across species)
    - FGMP: https://github.com/stajichlab/FGMP
    - fungphy: https://github.com/gamcil/fungiphy
    - UFCG pipeline: https://github.com/steineggerlab/ufcg

* Phylogenetic tree:
    1. MAFFT / MUSCLE alignment using AA sequence (https://github.com/GSLBiotech/mafft)
    2. trimAI / Gblocks to trim any poorly aligned regions and remove gaps (assuming many for fungi) (https://github.com/atmaivancevic/Gblocks)
    3. RAxML: Maximum likelihood tree drawing tool (https://github.com/amkozlov/raxml-ng)
        - Important to choose correct model
    4. Draw a cool looking tree
    5. Align with 'other' attributes
