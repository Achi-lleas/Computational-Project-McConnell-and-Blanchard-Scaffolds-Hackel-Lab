"""
Achilleas Thomas (Achi-lleas) 02/07/2025:
This is a script that searches for protein sequences inside UniProt and outputs them in FASTA format.
This script will be used to generate the sequences of the targets of the protein scaffolds identified by Blanchard et al. (2023) and McConnell et al. (2023).
"""

import urllib.request

from Bio import SeqIO

def main():
    
    with open("Target IDs.txt", "r") as file: # The name of the text files and other parameters can change for different applications.

        def sequence_uniprot(id):
            """
            Generates a list containing the protein of interest in FASTA format, after accessing it in the UniProt database.

            Args: the UniProt accession number of the protein.

            Returns: a list containing the protein of interest.
            """
            
            with open('Current Target Data.txt', 'w') as handle:
                
                page = urllib.request.urlopen(f"http://www.uniprot.org/uniprot/{id}.fasta")
                page = page.read().decode("utf-8")
                handle.write(page)
            
            with open("Current Target Data.txt", "r") as handle:
                
                proteins = list(SeqIO.parse(handle, "fasta"))
                return proteins
        
        with open("Target Sequences.txt", "a") as answer:
            
            for line in file:
        
                target, name, copies = line.strip().split(", ") # Each line has the following format "[UniProt Accession Number], [name of target], [number of copies of the chain to be modelled]".
                target = sequence_uniprot(target)
                target[0].id = name
                target[0].description = f"[copies={copies}]"
                SeqIO.write(target, answer, "fasta")
                answer.write("\n")

if __name__ == "__main__":
    
    main()
