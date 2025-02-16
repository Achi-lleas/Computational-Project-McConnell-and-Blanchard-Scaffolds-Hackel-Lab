"""
Achilleas Thomas (Achi-lleas) 02/06/2025:
This is a script that generates JSON files of ONE protein scaffold along with multiple targets that might consist of more than one chains (all in FASTA format). No PTM/cofactors are taken into account.
This script will be used to generate JSON files for the sequences identified by Blanchard et al. (2023) for use in AlphaFold3.
"""

from Bio import SeqIO

from re import sub

def generate_target_for_JSON(target, number):
    """
    This function generates the standard template of a protein chain that can be used inside a JSON file.
    
    Args: the sequence of the protein chain (target), the number of copies of the chain.

    Returns: a standard template to represent a protein sequence in JSON format.
    """

    template =""",
            {
            "proteinChain": {
                "sequence": "%s",
                "count": %s,
                "maxTemplateDate": "2023-01-20"
            }
            }""" % (target, number)
    
    return template

def generate_JSON(name, scaffold, targets):
    """
    This function generates a standard JSON template for the interaction between several different proteins.
    
    Args: the name of the job, the sequence of the binding scaffold, the sequence of the target protein(s).
    
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
                "useStructureTemplate": false
            }
            }""" % (name, scaffold)
    
    for sequence, number_of_copies in targets.items():
        
        template += generate_target_for_JSON(sequence, number_of_copies)
        
    template += """
                    ]
        ,
    "dialect": "alphafoldserver",
    "version": 1
        },
""" 
    
    return template

if __name__ == "__main__":

    with open("./Blanchard sequences.txt", "r") as scaffolds: #The names of the text files and other parameters can be modified for different applications.

        sequences_of_scaffolds = SeqIO.parse(scaffolds, "fasta")
        
        with open("./Target sequences.txt", "r") as targets:
            
            sequences_of_targets_initial_dictionary = SeqIO.to_dict(SeqIO.parse(targets, "fasta"))
            
            dictionary_of_targets = {}

            for j in sequences_of_targets_initial_dictionary.values():
                
                helper = {}

                for index, character in enumerate(j.description):
                        
                        if character == "[":
                            start = index+1
                        
                        if character == "]":
                            end = index
                            helper[j.description[start:end].split("=")[0]] = j.description[start:end].split("=")[1]

                dictionary_of_targets[j.id] = helper

            with open("./Blanchard JSON.json", "w") as file:
                
                file.write("[")
                file.write("\n")
                
                for i in sequences_of_scaffolds:
                    
                    start, end, dictionary_scaffold = 0, 0, {}

                    for index, character in enumerate(i.description):
                        
                        if character == "[":
                            start = index+1
                        
                        if character == "]":
                            end = index
                            dictionary_scaffold[i.description[start:end].split("=")[0]] = i.description[start:end].split("=")[1]
                        
                    for j in range(1,21): # For our project, we want to run the same job 20 times - this can change depending on the application.

                        file.write(generate_JSON(i.id + "seed" + str(j), i.seq, {sequences_of_targets_initial_dictionary[i].seq: dictionary_of_targets[i]["copies"] for i in dictionary_scaffold["target"].split(", ")})) # The FASTA sequence identifier line includes "[target=name of target1, name of target2, ...]".
                        file.write("\n")
                
                file.write("]")

    with open("./Blanchard JSON.json", "r+") as file:
        
        text = file.read()
        text = sub(pattern="        },\n\n]", repl="        }\n\t\n]", string=text)
        file.seek(0)
        file.write(text)
        file.truncate()
