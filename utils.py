import platform
import pathlib
import string
import random
import subprocess
import os
import json
from getpass import getpass
import psycopg2 as psy
from psycopg2 import extensions
from time import sleep


CURRENT_OS = platform.system()
MODULE_DIR = pathlib.Path(__file__).parent.absolute()

def generate_password():
    valid_chars = string.ascii_letters + string.digits + string.punctuation

    # Supprimer les caractères indésirables
    valid_chars = valid_chars.replace("'", "").replace(":", "").replace("\"", "")

    password = ''.join(random.choices(valid_chars, k=random.randint(15, 20)))
    return password

def string_to_hex(string):
    result = ""
    for char in string:
        result += hex(ord(char))[2:]
    return result

def hex_to_string(hex_string):
    result = ""
    for i in range(0, len(hex_string), 2):
        result += chr(int(hex_string[i:i+2], 16))
    return result

def check_psql_installed() -> bool:

    match CURRENT_OS:

        case "Linux":
            return subprocess.call("which psql", shell=True) == 0

        case "Windows":
            # find if C:\Program Files\PostgreSQL\15 exists
            print(os.path.exists("C:"))
            return os.path.exists("C:\Program Files\PostgreSQL")

        case "Darwin":
            return subprocess.call("which psql", shell=True) == 0

def Ask_Option(Option : str, Answers : list) -> bool:
    Confirm = input(Option)
    return Confirm.upper() in Answers

def install_psql(win_include_pgadmin: bool = False):

    match CURRENT_OS:
        case "Linux":
            subprocess.Popen(
                "sudo apt-get install postgresql -y", shell=True).wait()

        case "Windows":
                # download the file
                subprocess.Popen(
                    "powershell Invoke-WebRequest -Uri https://get.enterprisedb.com/postgresql/postgresql-15.2-1-windows-x64.exe -OutFile postgresql-15.2-1-windows-x64.exe",
                    shell=True).wait()

                if win_include_pgadmin:
                    disabled_components = "stackbuilder"
                else:
                    disabled_components = "stackbuilder,pgAdmin"

                subprocess.Popen(
                    f"cd.. | postgresql-15.2-1-windows-x64.exe --disable-components {disabled_components} --mode unattended --superpassword postgres",
                    shell=True).wait()

        case "Darwin":
            subprocess.Popen("brew install postgresql")

        case _:
            raise NotImplementedError("This OS is not supported yet.")
        
def Init():

    mdp_postgres = None

    # Installation du SGBDR
    if not check_psql_installed():
        print("Pour fonctionner, ce programme à besoin que PostgreSQL soit installé sur votre machine.")

        if Ask_Option("Voulez-vous installer PostgreSQL ? [O/n]", ["OUI", "YES", "O"]):
            print("Début de l'installation")
            install_psql()
            mdp_postgres = "postgres"
            print(
                "Installation terminée. Le mot de passe par défaut de l'utilisateur postgres est 'postgres'.")
        else:
            print(
                "L'installation de PostgreSQL est requise pour que le programme fonctionne.")
            
            sleep(15)
            exit()

    if CURRENT_OS == "Linux":
        subprocess.Popen(f"sudo su postgres -c 'psql -c \"CREATE DATABASE sae_aeroport WITH OWNER sae_aeroport_USER\"")

    if mdp_postgres is None:
        # Vérification du mdp postgres
        while mdp_postgres is None:
            print("Merci d'entrer le mot de passe de l'utilisateur postgresql (pour des raisons de sécurité, le mot de passe ne sera pas affiché)\n\
                  Ce mot de passe ne sera enregistré ni réutilisé après la création de la base de donnée")
            mdp_postgres = getpass()

            try:
                conn = psy.connect(
                    str("dbname = postgres user=postgres password=") + mdp_postgres)
            except psy.OperationalError:
                print("Le mot de passe semble incorrect")
                mdp_postgres = None
    else:
        conn = psy.connect(
            str("dbname = postgres user=postgres password=") + mdp_postgres)

    conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    db = conn.cursor()

    # Mise en place de l'utilisateur / de la database
    db.execute("CREATE USER sae_aeroport_USER LOGIN")
    random_pass = generate_password()
    print(random_pass)
    db.execute(f"ALTER ROLE sae_aeroport_USER WITH ENCRYPTED PASSWORD '{random_pass}'")
    db.execute("CREATE DATABASE sae_aeroport WITH OWNER sae_aeroport_USER")
    print(1)
    db.close()
    conn.close()
    print(2)
    # Création des tables
    conn = psy.connect(database="sae_aeroport", user="sae_aeroport_user", password=random_pass)
    print(3)
    db = conn.cursor()
    sql_path = MODULE_DIR.joinpath("SQL/sqlfile.sql")
    print(4)
    with open(sql_path, "r", encoding="utf-8") as file:
        db.execute(file.read().encode('utf-8'))
    conn.commit()
    db.close()
    conn.close()

    # Sauvegarde des mots de passe
    pass_dic = {"BPASS": string_to_hex(random_pass)}
    with open('Data.json', 'w') as Data:
        json.dump(pass_dic, Data)

    return random_pass