"""
Achilleas Thomas (Achi-lleas) 02/05/2025:
This is a script that generates JSON files of ONE protein scaffold along with ONE target that consists of one polypeptide chain (all in FASTA format). No PTM/cofactors are taken into account.
This script will be used to generate JSON files for the sequences identified by McConnell et al. (2023) for use in AlphaFold3.
Alternatively, one could use the json module.
"""

from Bio import SeqIO

from re import sub

def generate(name, target, scaffold):
    """
    This function generates a standard JSON template for the interaction between two different peptide chains.
    
    Args: the name of the job, the sequence of the target protein, the sequence of the binding scaffold.
    
    Returns: a JSON template in string format.
    """

    template = """
        {
        "name": "%s",
        "modelSeeds": [],
        "sequences": [
            {
            "proteinChain": {
                "sequence": "%s",
                "count": 1,
                "maxTemplateDate": "2023-01-20"
            }
            },
            {
            "proteinChain": {
                "sequence": "%s",
                "count": 1,
                "useStructureTemplate": false
            }
            }
                        ]
            ,
        "dialect": "alphafoldserver",
        "version": 1
        },
    """ % (name, target, scaffold)
    
    return template

if __name__ == "__main__":

    with open("./McConnell sequences.txt", "r") as scaffolds: #The names of the text files and other parameters can be modified for different applications.

        sequences_of_scaffolds = SeqIO.parse(scaffolds, "fasta")
        
        with open("./Target sequences.txt", "r") as targets:
            
            sequences_of_targets = SeqIO.to_dict(SeqIO.parse(targets, "fasta"))
            
            with open("./McConnell JSON.json", "w") as file:
                
                file.write("[")
                file.write("\n")
                
                for i in sequences_of_scaffolds:
                    
                    start, end, dic = 0, 0, {}

                    for index, character in enumerate(i.description):
                        
                        if character == "[":
                            start = index+1
                        
                        if character == "]":
                            end = index
                            dic[i.description[start:end].split("=")[0]] = i.description[start:end].split("=")[1]

                    for j in range(1,21): # For our project, we want to run the same job 20 times - this can change depending on the application.
                        
                        file.write(generate(i.id + "seed" + str(j), sequences_of_targets[dic["target"]].seq, i.seq)) # The FASTA sequence identifier line includes "[target=name of target]".
                        file.write("\n")
                
                file.write("]")

    with open("./McConnell JSON.json", "r+") as file:
        
        text = file.read()
        text = sub(pattern="        },\n\n]", repl="        }\n\t\n]", string=text)
        file.seek(0)
        file.write(text)
        file.truncate()
