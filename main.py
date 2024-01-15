from neo4j import GraphDatabase


def difficolta_piste():
    result = session.run("MATCH (p:pista) RETURN p.name, p.diff ORDER BY CASE p.diff WHEN 'blu' THEN 1 WHEN 'rossa' THEN 2 WHEN 'nera' THEN 3 ELSE 4 END")
    return [(r["p.name"], r["p.diff"]) for r in result]

def piste_aperte():
    result = session.run("MATCH (p:pista)-[r:CONDUCE_A]->() WHERE r.stato = 1 RETURN p.name")
    return [r["p.name"] for r in result]

def percorso_breve(pista1, pista2):
    result = session.run(
        "MATCH path = (startNode:pista {name: $p1})-[:CONDUCE_A*]->(endNode:pista {name: $p2})\n"
        "WITH path, REDUCE(totalDuration = 0, rel IN relationships(path) | totalDuration + rel.durata_minuti) AS totalDuration\n"
        "ORDER BY totalDuration ASC\n"
        "LIMIT 1\n"
        "RETURN nodes(path) as nodes, relationships(path) as rels, totalDuration;", p1=pista1, p2=pista2
    )
    
    record = result.single()
    
    if record:
        nodes = record["nodes"]
        rels = record["rels"]
        total_duration = record["totalDuration"]
        print('--------------------------------------------------------------------------------------------------------------------------\n')
        print("per raggiungere la tua destinazione nel minor tempo possibile, ti suggeriamo di seguire questo percorso:")
        for node in nodes:
            if node == nodes[-1]:
                print(f"infine  {node['name']} ({node['diff']})")
            elif node == nodes[0]:
                print(f"per cominciare {node['name']} ({node['diff']})")
            else:
                print(f"successivamente  {node['name']} ({node['diff']})")
        print(f'il tempo totale di percorrenza è di circa {total_duration} minuti')

        return None
    else:
        return None

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
            pista1 = input("Inserisci il nome del punto di partenza: ")
            pista2 = input("Inserisci il nome del punto di arrivo: ")
            percorso_breve(pista1, pista2)
        elif scelta == 4:
            print('grazie per scelto il nostro servizio, alla prossima...')
            break
        else:
            print('Scelta non valida')
