from neo4j import GraphDatabase


def difficolta_piste():
    result = session.run("MATCH (p:pista) RETURN p.name, p.diff ORDER BY CASE p.diff WHEN 'blu' THEN 1 WHEN 'rossa' THEN 2 WHEN 'nera' THEN 3 ELSE 4 END")
    return [(r["p.name"], r["p.diff"]) for r in result]

def piste_aperte():
    result = session.run("MATCH (p:pista)-[r:CONDUCE_A]->() WHERE r.stato = 1 RETURN p.name")
    return [r["p.name"] for r in result]

def percorso_breve(pista1, pista2):
    result = session.run("MATCH (p1:pista), (p2:pista) WHERE p1.name = $p1 AND p2.name = $p2 "
                         "CALL apoc.shortestPath(p1, p2, {relationship: 'CONDUCE_A'}) "
                         "YIELD path, weight RETURN length(path) as length, weight")
    for r in result:
        return r["length"], r["weight"]


if __name__ == '__main__':
    try:
        uri = 'bolt+s://dd77fa45.databases.neo4j.io'
        user = 'neo4j'
        pwd = 'PWZJs7q3meMtgeUQobxKOcMYuvFs9P36n2FNhi25gDs'
        driver = GraphDatabase.driver(uri, auth=(user, pwd))
        session = driver.session()
        print('successo')
    except Exception as e:
        print(f'errore: {e}')

    while True:
        scelta = int(input(('Inserisci: \n1 per visualizzare la difficoltà delle piste'
                            '\n2 per visualizzare le piste aperte'
                            '\n3 per visualizzare il percorso più breve tra due piste'
                            '\n4 per uscire\n')))
        if scelta == 1:
            result = difficolta_piste()
            for elem in result:
                print(f'la pista {elem[0]} ha difficoltà: {elem[1]}')
        elif scelta == 2:
            for elem in piste_aperte():
                if elem[-1] ==' ':
                    elem = elem[:-1]
                    print(f'la pista {elem} è aperta')
                else:
                    print(f'la pista {elem} è aperta')
        elif scelta == 3:
            pista1 = input("Inserisci il nome della prima pista: ")
            pista2 = input("Inserisci il nome della seconda pista: ")
            print(percorso_breve(pista1, pista2))
        elif scelta == 4:
            print('grazie per scelto il nostro servizio, alla prossima...')
            break
        else:
            print('Scelta non valida')
