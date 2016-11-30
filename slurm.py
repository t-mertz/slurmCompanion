"""
Interface with SLURM by translating to text commands.
"""

def squeue(username=""):
    app = ""
    if username != "":
        app += " -u " + username
    
    return "squeue" + app

def sbatch(filename):
    return "sbatch " + filename

def sinfo():
    return "sinfo"