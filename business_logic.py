
from models import PrediccionCuartos, PrediccionFinal, PrediccionRonda16, PrediccionSemifinal, Usuario
from flask import redirect, url_for
from sqlalchemy import text
import db

def get_partidos_R16(predicciones):
    """ Método que obtiene los partidos de la ronda de 16

    Returns:
        list: partidos de la ronda de 16
    """
    
    equipos_fase2 = {}
    
    for prediccion in predicciones:
        equipos_fase2['1ro {}'.format(prediccion.letra)] = {
            'id': prediccion.id_equipo_clasificado_1,
            'nombre': prediccion.equipo_clasificado_1
        }
        equipos_fase2['2do {}'.format(prediccion.letra)] = {
            'id': prediccion.id_equipo_clasificado_2,
            'nombre': prediccion.equipo_clasificado_2
        }
    
    partidos_fase2 = [
        {
            'id': 1,
            'equipo1': equipos_fase2['1ro A'],
            'equipo2': equipos_fase2['2do B']
        },
        {
            'id': 2,
            'equipo1': equipos_fase2['1ro B'],
            'equipo2': equipos_fase2['2do A']
        },
        {
            'id': 3,
            'equipo1': equipos_fase2['1ro C'],
            'equipo2': equipos_fase2['2do D']
        },
        {
            'id': 4,
            'equipo1': equipos_fase2['1ro D'],
            'equipo2': equipos_fase2['2do C']
        },
        {
            'id': 5,
            'equipo1': equipos_fase2['1ro E'],
            'equipo2': equipos_fase2['2do F']
        },
        {
            'id': 6,
            'equipo1': equipos_fase2['1ro F'],
            'equipo2': equipos_fase2['2do E']
        },
        {
            'id': 7,
            'equipo1': equipos_fase2['1ro G'],
            'equipo2': equipos_fase2['2do H']
        },
        {
            'id': 8,
            'equipo1': equipos_fase2['1ro H'],
            'equipo2': equipos_fase2['2do G']
        }
    ]
    return partidos_fase2

def guardar_prediccion(id_usuario, params):
    guardo_final = False
    # Se almacena la ronda de 16
    if 'partido_1' in params:
        for i in range(1, 9):
            db.session.add(PrediccionRonda16(
                i,
                params[f'partido_{i}'],
                id_usuario
            ))
    # Se almacena la ronda de cuartos
    elif 'partido_cuartos_1' in params:
        for i in range(1, 5):
            db.session.add(PrediccionCuartos(
                i,
                params[f'partido_cuartos_{i}'],
                id_usuario
            ))
    # Se almacena la ronda semifinal
    elif 'partido_semi_1' in params:
        for i in range(1, 3):
            db.session.add(PrediccionSemifinal(
                i,
                params[f'partido_semi_{i}'],
                id_usuario
            ))
    # Se almacena la ronda final
    elif 'partido_final_1' in params:
        for i in range(1, 2):
            db.session.add(PrediccionFinal(
                i,
                params[f'partido_final_{i}'],
                id_usuario
            ))    
        guardo_final = True    
    db.session.commit()
    return guardo_final

def get_partidos_cuartos(prediccionesR16):
    equipos_cuartos = {}
    for pred16 in prediccionesR16:
        equipos_cuartos[pred16.partido] = {
            'id_equipo': pred16.id_equipo,
            'nombre_equipo': pred16.nombre_equipo
        }
    partidos_cuartos = [
        {
            'id': 1,
            'id_1': 1,
            'id_2': 3,
            'equipo1': equipos_cuartos[1],
            'equipo2': equipos_cuartos[3]
        },
        {
            'id': 2,
            'id_1': 2,
            'id_2': 4,
            'equipo1': equipos_cuartos[2],
            'equipo2': equipos_cuartos[4]
        },
        {
            'id': 3,
            'id_1': 5,
            'id_2': 7,
            'equipo1': equipos_cuartos[5],
            'equipo2': equipos_cuartos[7]
        },
        {
            'id': 4,
            'id_1': 6,
            'id_2': 8,
            'equipo1': equipos_cuartos[6],
            'equipo2': equipos_cuartos[8]
        }
    ]
    return partidos_cuartos

def get_partidos_semi(prediccionesCuartos):
    equipos_semi = {}
    for predCuartos in prediccionesCuartos:
        equipos_semi[predCuartos.partido_cuartos] = {
            'id_equipo' : predCuartos.id_equipo,
            'nombre_equipo' : predCuartos.nombre_equipo
        }
    partidos_semi = [
        {
            'id': 1,
            'id_1': 1,
            'id_2': 3,
            'equipo1': equipos_semi[1],
            'equipo2': equipos_semi[3]

        },
        {
            'id': 2,
            'id_1': 2,
            'id_2': 4,
            'equipo1': equipos_semi[2],
            'equipo2': equipos_semi[4]
        }
    ]
    return partidos_semi

def get_partido_final(prediccionesSemifinal):
    equipos_final = {}
    for predSemi in prediccionesSemifinal:
        equipos_final[predSemi.partido_semi] = {
            "id_equipo": predSemi.id_equipo,
            "nombre_equipo": predSemi.nombre_equipo
        }
    partidos_final = [
        {
            'id': 1,
            'id_1': 1,
            'id_2': 2,
            'equipo1': equipos_final[1],
            'equipo2': equipos_final[2]
        }
    ]
    return partidos_final

def obtener_puntaje_fase_grupos(id_usuario):
    resultados_grupos = [
        {
            'grupo':1,
            'equipo1':12,
            'equipo2':22
        },
        {
            'grupo':2,
            'equipo1':10,
            'equipo2':29
        },
        {
            'grupo':3,
            'equipo1':13,
            'equipo2':26
        },
        {
            'grupo':4,
            'equipo1':5,
            'equipo2':31
        },
        {
            'grupo':5,
            'equipo1':16,
            'equipo2':8
        },
        {
            'grupo':6,
            'equipo1':23,
            'equipo2':7
        },
        {
            'grupo':7,
            'equipo1':4,
            'equipo2':11
        },
        {
            'grupo':8,
            'equipo1':25,
            'equipo2':15
        }
    ]
    predicados = []
    for res in resultados_grupos:
        grupo = res['grupo']
        equipo1 = res['equipo1']
        equipo2 = res['equipo2']
        predicados.append(f'''
                          (
                              (id_grupo = {grupo} and equipo_clasificado_1 = {equipo1} and equipo_clasificado_2 = {equipo2}) OR
                              (id_grupo = {grupo} and equipo_clasificado_1 = {equipo2} and equipo_clasificado_2 = {equipo1})
                            )''')
    
    query = """
            SELECT id_prediccion FROM predicciones
            WHERE 
            id_usuario = {}
            AND
            ({})
            """.format(id_usuario, ' or '.join(predicados))
    
    with db.engine.connect() as con:
        predicciones_acertadas = con.execute(query).all()
        puntaje_fase_grupos = len(predicciones_acertadas)
    return puntaje_fase_grupos

def obtener_puntaje_R16(id_usuario):
    '''
    TAREA 1:
    1) Lista con puntajes reales.
    2) Armar los predicados (equipo).
    3) Sentencia SQL adicionando el filtro por id_usuario.
        Teniendo cuidado con la relevancia de los operadores AND y OR
    4) Contar el número de aciertos para asignar 1 punto por cada acierto.
    '''

    resultados_R16 = [
        {'partido': 1,
         'equipo1': 12
         },
        {'partido': 2,
         'equipo1': 10
         },
        {'partido': 3,
         'equipo1': 13
        },
        {'partido': 4,
         'equipo1': 5
         },
        {'partido': 5,
         'equipo1': 7
         },
        {'partido': 6,
         'equipo1': 23
         },
        {'partido': 7,
         'equipo1': 4
         },
        {'partido': 8,
         'equipo1': 25
         }
    ]
    predicados = []
    for res in resultados_R16:
        equipo1 = res['equipo1']
        predicados.append(f'id_equipo = {equipo1}')

    query = """
                SELECT id_prediccionRonda16 FROM predicciones_R16
                WHERE 
                id_usuario = {}
                AND
                ({})
                """.format(id_usuario, ' or '.join(predicados))

    with db.engine.connect() as con:
        predicciones_acertadas = con.execute(query).all()
        puntaje_R16 = len(predicciones_acertadas)
    return puntaje_R16

'''
TAREA 2:
    Replicar la TAREA 1 para todas las demás fases.
'''

def obtener_puntaje_cuartos(id_usuario):
    resultados_cuartos = [
        {'partido': 1,
         'equipo1': 13
         },
        {'partido': 2,
         'equipo1': 5
         },
        {'partido': 3,
         'equipo1': 7
         },
        {'partido': 4,
         'equipo1': 23
         }
    ]
    predicados = []
    for res in resultados_cuartos:
        equipo1 = res['equipo1']
        predicados.append(f'id_equipo = {equipo1}')

    query = """
                    SELECT id_prediccionCuartos FROM predicciones_cuartos
                    WHERE 
                    id_usuario = {}
                    AND
                    ({})
                    """.format(id_usuario, ' or '.join(predicados))

    with db.engine.connect() as con:
        predicciones_acertadas = con.execute(query).all()
        puntaje_cuartos = len(predicciones_acertadas)
    return puntaje_cuartos


def obtener_puntaje_semi(id_usuario):
    resultados_semi = [
        {'partido': 1,
         'equipo1': 13
         },
        {'partido': 2,
         'equipo1': 5
         }
    ]
    predicados = []
    for res in resultados_semi:
        equipo1 = res['equipo1']
        predicados.append(f'id_equipo = {equipo1}')

    query = """
                        SELECT id_prediccionSemi FROM predicciones_semifinal
                        WHERE 
                        id_usuario = {}
                        AND
                        ({})
                        """.format(id_usuario, ' or '.join(predicados))

    with db.engine.connect() as con:
        predicciones_acertadas = con.execute(query).all()
        puntaje_semi = len(predicciones_acertadas)
    return puntaje_semi

def obtener_puntaje_final(id_usuario):
    '''
    NOTA TAREA 2:
        No es necesario tener en 1) una lista, solamente el id del equipo ganador.
    '''
    equipo = 13

    query = """
                        SELECT id_prediccionFinal FROM predicciones_final
                        WHERE 
                        id_usuario = {}
                        AND
                        (id_equipo = {})
                        """.format(id_usuario, equipo)

    with db.engine.connect() as con:
        predicciones_acertadas = con.execute(query).all()
        puntaje_final = len(predicciones_acertadas)
    return puntaje_final

def obtener_puntaje(id_usuario):
    puntaje_fase_grupos = obtener_puntaje_fase_grupos(id_usuario)
    puntaje_R16 = obtener_puntaje_R16(id_usuario)
    puntaje_cuartos = obtener_puntaje_cuartos(id_usuario)
    puntaje_semi = obtener_puntaje_semi(id_usuario)
    puntaje_final = obtener_puntaje_final(id_usuario)

    return (puntaje_fase_grupos + puntaje_R16 + puntaje_cuartos + puntaje_semi + puntaje_final)

def guardar_puntaje(id_usuario, puntaje):
    db.session.query(Usuario).\
        filter(Usuario.id_usuario == id_usuario).\
        update({'puntaje': puntaje})
    db.session.commit()

def calcular_puntaje_usuario(id_usuario):
    puntaje = obtener_puntaje(id_usuario)
    guardar_puntaje(id_usuario, puntaje)
