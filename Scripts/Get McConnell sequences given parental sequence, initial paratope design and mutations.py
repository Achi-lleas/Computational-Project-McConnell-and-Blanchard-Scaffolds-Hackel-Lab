"""
Achilleas Thomas (Achi-lleas) 02/05/2025:
This is a script to get a specific variant when we know its parental sequence, its initial paratope design, and its mutations relative to the parental sequence.
This will be used for the McConnell et al. paper (26 sequences in total).
"""

from Bio import SeqIO

class get_sequence(): 
    
    def __init__(self, parental_sequence, initial_paratope_design, mutations):
        
        self.parent = parental_sequences[int(parental_sequence)-1]
        self.inidesign = initial_paratope_designs[int(initial_paratope_design)-1]
        self.mut = mutations
    
    def write_sequence(self, number):
        """Generates the variant given its parental sequence, its initial paratope design, and its mutations relative to the parental sequence.
        
        Args: the number of the sequence, in the order it appears in the document.
        
        Returns: a string of the sequence.
        """
        
        with open("./McConnell sequences.txt", "a") as file: # The names of the documents can change for different applications.

            sequence_list = [aminoacid for aminoacid in self.parent]
            
            for mutation in self.mut.split(" "): # The mutations are given in the following format: "[position][amino acid][space]". This can be easily modified to be used with the standard way of representing mutations.
                sequence_list[int(mutation[:len(mutation)-1])-1] = mutation[-1] 
            
            if self.parent != -1:    
                for mutation in self.inidesign.split(" "):
                    sequence_list[int(mutation[:len(mutation)-1])-1] = mutation[-1]
            
            file.write(">MC" + str(number) + "\n") # The sequences are written in FASTA format.
            file.write("".join(i for i in sequence_list))
            file.write("\n"*2)

if __name__ == "__main__":

    parental_sequences = list(SeqIO.parse("./Parental sequences.txt", "fasta")) # Parental sequences are given in FASTA format and the order they appear in the document is specific.

    parental_sequences = [i.seq for i in parental_sequences]

    with open("./Initial paratope designs.txt", "r") as file: # The order of initial paratope designs is also specific. Initial paratope designs were only used for Parental Sequence 1, but this can change for future uses.
        
        initial_paratope_designs = []
        
        for line in file:
            initial_paratope_designs.append(line.strip())

    repeats = 0

    with open("Mutations.txt", "r") as file:
        
        Mutations = file.readlines()
        repeats = len(Mutations)      

    with open("Mutations.txt", "r") as file:
        
        for i in range(1, repeats//4+2):    
            x = get_sequence(file.readline().strip(), file.readline().strip(), file.readline().strip()) # First line is the number of the parental sequence, second line is the number of the initial paratope design (if parental sequence is 1, otherwise it is 0 by default), third line are the mutations.
            file.readline() # Fourth line is blank by design.
            x.write_sequence(i)
