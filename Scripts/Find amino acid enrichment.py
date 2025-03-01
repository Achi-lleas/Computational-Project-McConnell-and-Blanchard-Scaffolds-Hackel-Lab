"""
Achilleas Thomas (Achi-lleas) 02/16/2025:
This is a script that generates a bar graph of the frequency of each amino acid in the paratopes of the designed scaffolds.
It also employs a two-tailed p-test to check if the enrichment in each one of the amino acids is statistically significant or not.
"""

from Bio import SeqIO

from matplotlib import pyplot

from scipy.stats import binom

one_letter_amino_acids = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "Y"]

def main(name):
    
    with open(f"./Amino acids participating in binding {name}.txt", "r") as file: # The name of the text files and other parameters can change for different applications of this script.
        
        total_amino_acids = 0
        enrichments, sequences = {}, []
        
        for sequence in SeqIO.parse(file, "fasta"):
            
            sequences.append(sequence.seq)

        for amino_acid in one_letter_amino_acids:
            
            current_total = 0 

            for i in sequences:

                current_total += i.count(amino_acid)
            
            enrichments[amino_acid] = current_total
            
            total_amino_acids += current_total

    help_list = sorted(enrichments.items(), key=lambda i: (i[1], i[0]))
    enrichments = {}

    for i in help_list:

        enrichments[i[0]] = i[1]  

    significance = []

    with open(f"Amino acid frequencies in initial {name} libraries.txt", "r") as file:

        probabilities = {}

        for line in file: # Each line is of the form [amino acid one letter code] [frequency of the amino acid in the library].

            probabilities[line.split(" ")[0]] = line.split(" ")[1]
    
    for i, j in enrichments.items(): # A binomial distribution is used to check for enrichment in amino acids. The null hypothesis is that the amino acid being tested has a frequency equal to its frequency in all of the libraries in all paratopes.

        if 0.025 < binom.cdf(j, total_amino_acids, float(probabilities[i])) < 0.975:
            significance.append(False)
        else:
            significance.append(True)

    for key, value in enrichments.items():

        enrichments[key] = value / total_amino_acids  

    plot_of_enrichments = pyplot.bar(enrichments.keys(), enrichments.values(), color = "red", width=0.5)
    
    pyplot.xlabel("Amino acids")
    pyplot.ylabel("Enrichment")
    pyplot.title("Amino acid enrichment of the Blanchard/McConnell scaffold paratopes")
    
    for index, bar in enumerate(plot_of_enrichments):
        
        if significance[index]:
            pyplot.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), '*', ha='center', va='bottom', fontsize=14)
    
    pyplot.show()
    
if __name__ == "__main__":    

    main("Blanchard")
    main("McConnell")
