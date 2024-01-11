from neo4j import GraphDatabase
try:
    uri = 'bolt+s://dd77fa45.databases.neo4j.io'

    user = 'neo4j'
    pwd = 'PWZJs7q3meMtgeUQobxKOcMYuvFs9P36n2FNhi25gDs'
    driver = GraphDatabase.driver(uri, auth=(user, pwd)) # uri, username, pwd
    session = driver.session()
    print('successo')
except:
    print('errore')