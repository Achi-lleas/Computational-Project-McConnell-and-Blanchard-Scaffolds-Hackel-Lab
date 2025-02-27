# Achilleas Thomas (Achi-lleas) 02/20/2025:
# This is a sample Linux script that can be used to replicate the sequence of steps used to perform our project, by running each of the scripts one at a time.
# Make sure to have every file in the correct place and with the correct format. For the correct format look into each individual script.

$ mkdir "./Blanchard-McConnell files"
$ cd "./Blanchard-McConnell files"
# Make sure to have the following files in the new directory correctly formatted: Parental sequences.txt, Initial paratope designs.txt, Mutations.txt and all the scripts
$ python3 "Get McConnell sequences given parental sequence, initial paratope design and mutations.py"
# Make sure to have the following file in the directory correctly formatted: Target IDs.txt
$ python3 "Access sequences of targets through UniProt.py"
# Make sure to have the following files in the directory correctly formatted: McConnell sequences.txt, Blanchard sequences.txt, Target sequences.txt
$ python3 "Generate JSON for McConnell sequences.py"
$ python3 "Generate JSON for Blanchard sequences.py"
# Make sure to have the following files in the directory: Blanchard JSON.json, McConnell JSON.json
$ Rscript "Split JSON file.r"
# Run the jobs on AlphaFold3 and download the models
$ unzip ~/Downloads/*.zip
$ mkdir "./Scaffold models"
$ mv -v ~/Downloads/* "~/Blanchard-McConnell files/Scaffold models"
$ mkdir "./Best seeds"
$ mkdir "./cif files"
$ python3 "Loop through AlphaFold3 models and compare scores.py"
$ python3 "Move cif files for each scaffold into new directory.py"
# Do the analysis on ChimeraX and make sure to have the following file in the directory correctly formatted: Amino acids participating in binding.txt
$ python3 "Find amino acid enrichment.py"
