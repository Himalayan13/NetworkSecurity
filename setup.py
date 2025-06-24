from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    requirements_lst:List[str] = []

    try:
        with open('requirements.txt','r') as file:
            #Reading lines from the files 
            lines = file.readlines()
            #Processing each line
            for line in lines:
                requirement = line.strip()
                if requirement and requirement!='-e .':
                    requirements_lst.append(requirement)
    
    except FileNotFoundError:

        print("Requirement.txt file not found")

    return requirements_lst

setup(
    name = "NetworkSecurity",
    version="0.0.1",
    author = "Himnish A",
    author_email = "himnisha11@gmail.com",
    packages= find_packages(),
    install_requires = get_requirements()

)