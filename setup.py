from setuptools import find_packages,setup
from typing import List



def get_requirements()->List[str]:
    #this function will list list of requirements
    requirement_lst: List[str] = []
    try:
        with open("requirements.txt","r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip() # ignore extra spaces
                #ignore empty lines and -e.
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirement file not Found")
    return  requirement_lst

setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    author="Adarsh Kumar",
    author_email="adarsh2022ji@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)