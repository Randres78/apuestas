
from models import PrediccionCuartos, PrediccionFinal, PrediccionRonda16, PrediccionSemifinal
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
    db.session.commit()

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