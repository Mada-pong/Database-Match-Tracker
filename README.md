Resources:
Project docs: 
https://docs.google.com/document/d/1RVoDHEq723h7ekaB5ZLQuE3pM-vhqbLSoki4lT72p50/edit?tab=t.0

Er-diagram:
https://app.diagrams.net/#G1jyYc9VEoREAkPzUCpXBZ01jADWP0GGLM#%7B%22pageId%22%3A%22JRb11X1MwFA-jICFqmsR%22%7D

SQL Schema: 
https://app.diagrams.net/#G1MofRxAOzR1LIuTOSUC3N_v4ybhDWiaNf

Setup:

python -m venv .venv

source .venv/Scripts/activate

pip install -r requirements.txt

Setting up your user: 

create a file ".env"

DB_HOST=host ip 
DB_PORT=3306
DB_USER=user
DB_PASSWORD=password
DB_NAME=MatchDB
