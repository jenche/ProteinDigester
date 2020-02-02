# ProteinDigester
ProteinDigester is a small tool created to import and digest FASTA database. Once digested, it makes it possible to quickly determine which petpides are proteotypic and if they are not, from what other proteins they can be obtained.
# Requirements
ProteinDigester has not been packaged yet. To run it, you'll need Python (>=3.7) and PySide2. Then, run `proteindigester.py` script.
# Quick guide
- Launch ProteinDigester
- Create a digestion database (Ctrl+N)
- Import a FASTA file (Ctrl+I)
- Add a digestion (Ctrl+A)

You can add more than one digestion. If you do so, you can select the current digestion using the "Working digestion" menu.

You can search proteins by name, sequence or digest peptides. Once you've found the protein you want, just select it and ProteinDigester will show you all the peptides obtained and wether they are proteotypic or not. If you select a peptide, it will show you from what other proteins it can be obtained.
# Screenshot
![alt text](https://github.com/jenche/ProteinDigester/blob/master/snapshots/snapshot01.png)
