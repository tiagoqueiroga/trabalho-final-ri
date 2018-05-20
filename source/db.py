import sqlite3
import os
import requests

def cria_conexao_sqlite(db_file):
    print("Criando 'banco de dados SQLite")
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def cria_tabelas(conn):
    cria_tabela_reports(conn)
    cria_tabela_midias(conn)

def cria_tabela_reports(conn):
	cursor = conn.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS ufo_reports (
                        id int PRIMARY KEY,
                        tags text,
                        address text,
                        altitude text ,
                        city text,
                        country text,
                        county text,
                        created text,
                        description text,
                        detailedDescription text,
                        distance text,
                        duration text,
                        flightPath text,
                        latitude double,
                        location text,
                        longitude double,
                        region text,
                        shape text,
                        summary text,
                        locationName text,
                        type text
                        )
				   ''')


def cria_tabela_midias(conn):
	cursor = conn.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS ufo_midias (
                        url text PRIMARY KEY,
                        report_id int,
                        type text
                        )
				   ''')

def grava_reports(conn,reports):
    conn.executemany('INSERT OR REPLACE INTO ufo_reports VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', reports)
    conn.commit()


def coleta_dados(conteudo):
    reports = []
    for elemento in conteudo:
        # Só busca reports com algum tipo de midia(Fotos ou vídeos)
        if(len(elemento['urls']) > 0):
            reports.append(
                tuple((
                    elemento['id'],
                    ",".join(elemento['tags']),
                    elemento['address'],
                    elemento['altitude'],
                    elemento['city'],
                    elemento['country'],
                    elemento['county'],
                    elemento['created'],
                    elemento['description'],
                    elemento['detailedDescription'],
                    elemento['distance'],
                    elemento['duration'],
                    elemento['flightPath'],
                    elemento['latitude'],
                    elemento['location'],
                    elemento['longitude'],
                    elemento['region'],
                    elemento['shape'],
                    elemento['summary'],
                    elemento['locationName'],
                    elemento['type'],
                ))
            )
        # Grava midias na tabela ufo_midias
        midias = coleta_midias(elemento['id'],elemento['urls'])   
    
    return {"reports":reports,"midias":midias}

def coleta_midias(id_report,midias):
    listaMidias = []
    for midia in midias:
        listaMidias.append(
            tuple((
                midia,
                id_report,
                define_tipo_midia(midia)
            ))
        )

    return listaMidias    

def define_tipo_midia(midia):
    nome_arquivo, extensao = os.path.splitext(midia)
    if is_image(extensao.replace('.','')):
        import uuid

        # Salva images na pasta /midia/images
        """
        with open('../midia/images/' + str(uuid.uuid1()) + extensao, 'wb') as handle:
            response = requests.get(midia, stream=True)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        """

        return 'image'
    else:
        return 'video'      

def grava_midias(conn,midias):
    conn.executemany('INSERT OR REPLACE INTO ufo_midias VALUES (?,?,?)', midias)
    conn.commit()  

def is_image(extensao):
    images = [
        "bmp","cut","dds","dib","djvu","egt","exif","gif","gpl","pam","pcx","tga"
        "grf","icns","ico","iff","jng","jpeg","jpg","jfif","jp2","jps","pcf","pcx","pdn","pgm",
        "PI1","PI2","PI3","pict","pct","pnm","pns","ppm","psb","psd","pdd",
        "psp","px","pxm","pxr","qfx","raw","rle","sct","sgi","rgb","int",
        "bw","tga","tiff","tif","vtf","xbm","xcf","xpm","3dv","amf","ai",
        "awg","cgm","cdr","cmx","dxf","e2d","egt","eps","fs","gbr","odg",
        "svg","stl","vrml","x3d","sxd","v2d","vnd","wmf","emf","art","xar",
        "png","webp","jxr","hdp","wdp","cur","ecw","iff","lbm","liff","nrrd"
    ]

    if extensao in images:
        return True
    else:
        return False