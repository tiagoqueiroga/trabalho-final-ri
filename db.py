import sqlite3

def cria_conexao_sqlite(db_file):
    print("Criando 'banco de dados SQLite")
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def cria_tabela_reports(conn):
	cursor = conn.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS ufo_reports (
                        id int PRIMARY KEY,
                        tags text,
                        address text,
                        addressResolution text,
                        altitude text ,
                        city text,
                        country text,
                        county text,
                        midia text,
                        created text,
                        description text,
                        detailedDescription text,
                        distance text,
                        duration text,
                        features text,
                        flightPath text,
                        latitude double,
                        location text,
                        logNumber text,
                        longitude double,
                        occurred double,
                        region text,
                        shape text,
                        source text,
                        submitted double,
                        summary text,
                        locationName text,
                        type text
                        )
				   ''')

def grava_reports(conn,reports):
    conn.executemany('INSERT OR REPLACE INTO ufo_reports VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', reports)
    conn.commit()

def coleta_reports(conteudo):
    reports = []
    for elemento in conteudo:
        # Só busca reports com algum tipo de midia(Fotos ou vídeos)
        if(len(elemento['urls']) > 0):
            reports.append(
                tuple((
                    elemento['id'],
                    ",".join(elemento['tags']),
                    elemento['address'],
                    elemento['addressResolution'],
                    elemento['altitude'],
                    elemento['city'],
                    elemento['country'],
                    elemento['county'],
                    ",".join(elemento['urls']),
                    elemento['created'],
                    elemento['description'],
                    elemento['detailedDescription'],
                    elemento['distance'],
                    elemento['duration'],
                    elemento['features'],
                    elemento['flightPath'],
                    elemento['latitude'],
                    elemento['location'],
                    elemento['logNumber'],
                    elemento['longitude'],
                    elemento['occurred'],
                    elemento['region'],
                    elemento['shape'],
                    elemento['source'],
                    elemento['submitted'],
                    elemento['summary'],
                    elemento['locationName'],
                    elemento['type'],
                ))
    )
    return reports
