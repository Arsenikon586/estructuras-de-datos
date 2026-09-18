
tablero = [[' ' for _ in range(8)] for _ in range(8)]
movimientos = []
jugadorActual = 'X'
def inicializar_tablero():
    global tablero
    tablero = [[' ' for _ in range(8)] for _ in range(8)]
    for fila in range(3):
        for columna in range(8):
            if (fila + columna) % 2 == 1:
                tablero[fila][columna] = 'O'
    for fila in range(5, 8):
        for columna in range(8):
            if (fila + columna) % 2 == 1:
                tablero[fila][columna] = 'X'
def mostrar_tablero():
    print()
    print("       1   2   3   4   5   6   7   8")
    print("     #---#---#---#---#---#---#---#---#")
    for fila in range(8):
        print(f" {fila + 1}   |", end="")
        for columna in range(8):
            print(f" {tablero[fila][columna]} |", end="")
        print()
        print("     #---#---#---#---#---#---#---#---#")
    print()
def posicion_valida(fila, columna):
    return 0 <= fila < 8 and 0 <= columna < 8
def es_ficha_contraria(ficha):
    if jugadorActual == 'X':
        return ficha in ('O', 'o')
    if jugadorActual == 'O':
        return ficha in ('X', 'x')
    return False
def es_movimiento_normal(fila_origen, columna_origen, fila_destino, columna_destino):
    diferencia_fila = fila_destino - fila_origen
    diferencia_columna = columna_destino - columna_origen
    if abs(diferencia_fila) != 1 or abs(diferencia_columna) != 1:
        return False
    ficha = tablero[fila_origen][columna_origen]
    if ficha == 'X' and diferencia_fila != -1:
        return False
    if ficha == 'O' and diferencia_fila != 1:
        return False
    return True
def es_movimiento_de_captura(fila_origen, columna_origen, fila_destino, columna_destino):
    diferencia_fila = fila_destino - fila_origen
    diferencia_columna = columna_destino - columna_origen
    if abs(diferencia_fila) != 2 or abs(diferencia_columna) != 2:
        return False
    fila_media = (fila_origen + fila_destino) // 2
    columna_media = (columna_origen + columna_destino) // 2
    ficha_en_medio = tablero[fila_media][columna_media]
    if not es_ficha_contraria(ficha_en_medio):
        return False
    ficha = tablero[fila_origen][columna_origen]
    if ficha == 'X' and diferencia_fila != -2:
        return False
    if ficha == 'O' and diferencia_fila != 2:
        return False
    return True
def coronar_ficha(fila, columna):
    if tablero[fila][columna] == 'X' and fila == 0:
        tablero[fila][columna] = 'x'
        print("La ficha X se ha convertido en dama.")
    if tablero[fila][columna] == 'O' and fila == 7:
        tablero[fila][columna] = 'o'
        print("La ficha O se ha convertido en dama.")
def guardar_movimiento(fila_origen, columna_origen, fila_destino, columna_destino, captura):
    tipo = "[CAPTURA]" if captura else "[MOVIMIENTO]"
    movimiento = (
        f"Jugador {jugadorActual}: "
        f"({fila_origen + 1},{columna_origen + 1}) -> "
        f"({fila_destino + 1},{columna_destino + 1}) {tipo}"
    )
    movimientos.append(movimiento)
def puede_capturar_desde(fila, columna):
    movimientos_fila = [-2, -2, 2, 2]
    movimientos_columna = [-2, 2, -2, 2]
    for i in range(4):
        nueva_fila = fila + movimientos_fila[i]
        nueva_columna = columna + movimientos_columna[i]
        if posicion_valida(nueva_fila, nueva_columna):
            if tablero[nueva_fila][nueva_columna] == ' ':
                if es_movimiento_de_captura(fila, columna, nueva_fila, nueva_columna):
                    return True
    return False
def continuar_captura(fila, columna):
    puede_capturar = puede_capturar_desde(fila, columna)
    while puede_capturar:
        print()
        print("Puedes realizar otra captura.")
        mostrar_tablero()
        try:
            nueva_fila = int(input("Nueva fila destino: ")) - 1
            nueva_columna = int(input("Nueva columna destino: ")) - 1
        except ValueError:
            print("Posicion invalida.")
            continue
        if not posicion_valida(nueva_fila, nueva_columna):
            print("Posicion invalida.")
            continue
        if tablero[nueva_fila][nueva_columna] != ' ':
            print("La posicion esta ocupada.")
            continue
        if not es_movimiento_de_captura(fila, columna, nueva_fila, nueva_columna):
            print("Debes realizar una captura valida.")
            continue
        fila_media = (fila + nueva_fila) // 2
        columna_media = (columna + nueva_columna) // 2
        tablero[fila_media][columna_media] = ' '
        tablero[nueva_fila][nueva_columna] = tablero[fila][columna]
        tablero[fila][columna] = ' '
        coronar_ficha(nueva_fila, nueva_columna)
        guardar_movimiento(fila, columna, nueva_fila, nueva_columna, True)
        fila = nueva_fila
        columna = nueva_columna
        puede_capturar = puede_capturar_desde(fila, columna)
def realizar_movimiento():
    try:
        fila_origen = int(input("Fila de la ficha: ")) - 1
        columna_origen = int(input("Columna de la ficha: ")) - 1
    except ValueError:
        print("Posicion fuera del tablero.")
        return False
    if not posicion_valida(fila_origen, columna_origen):
        print("Posicion fuera del tablero.")
        return False
    if (
        tablero[fila_origen][columna_origen] != jugadorActual
        and tablero[fila_origen][columna_origen] != jugadorActual.lower()
    ):
        print("No hay una ficha tuya en esa posicion.")
        return False
    try:
        fila_destino = int(input("Fila destino: ")) - 1
        columna_destino = int(input("Columna destino: ")) - 1
    except ValueError:
        print("Posicion fuera del tablero.")
        return False
    if not posicion_valida(fila_destino, columna_destino):
        print("Posicion fuera del tablero.")
        return False
    if tablero[fila_destino][columna_destino] != ' ':
        print("La posicion destino esta ocupada.")
        return False
    es_captura = es_movimiento_de_captura(
        fila_origen, columna_origen, fila_destino, columna_destino
    )
    movimiento_normal = es_movimiento_normal(
        fila_origen, columna_origen, fila_destino, columna_destino
    )
    if not es_captura and not movimiento_normal:
        print("Movimiento no valido.")
        return False
    if es_captura:
        fila_media = (fila_origen + fila_destino) // 2
        columna_media = (columna_origen + columna_destino) // 2
        tablero[fila_media][columna_media] = ' '
    tablero[fila_destino][columna_destino] = tablero[fila_origen][columna_origen]
    tablero[fila_origen][columna_origen] = ' '
    coronar_ficha(fila_destino, columna_destino)
    guardar_movimiento(
        fila_origen, columna_origen, fila_destino, columna_destino, es_captura
    )
    if es_captura:
        continuar_captura(fila_destino, columna_destino)
    return True
def puede_mover_normalmente(fila, columna):
    ficha = tablero[fila][columna]
    direcciones_columna = [-1, 1]
    for dir_col in direcciones_columna:
        nueva_columna = columna + dir_col
        if ficha == 'X':
            nueva_fila = fila - 1
            if posicion_valida(nueva_fila, nueva_columna):
                if tablero[nueva_fila][nueva_columna] == ' ':
                    return True
        if ficha == 'O':
            nueva_fila = fila + 1
            if posicion_valida(nueva_fila, nueva_columna):
                if tablero[nueva_fila][nueva_columna] == ' ':
                    return True
        if ficha in ('x', 'o'):
            for dir_fila in [-1, 1]:
                nueva_fila = fila + dir_fila
                if posicion_valida(nueva_fila, nueva_columna):
                    if tablero[nueva_fila][nueva_columna] == ' ':
                        return True
    return False
def puede_capturar_con_jugador(fila, columna, jugador):
    cambios_fila = [-2, -2, 2, 2]
    cambios_columna = [-2, 2, -2, 2]
    ficha = tablero[fila][columna]
    for i in range(4):
        nueva_fila = fila + cambios_fila[i]
        nueva_columna = columna + cambios_columna[i]
        if posicion_valida(nueva_fila, nueva_columna):
            if tablero[nueva_fila][nueva_columna] == ' ':
                fila_media = (fila + nueva_fila) // 2
                columna_media = (columna + nueva_columna) // 2
                ficha_media = tablero[fila_media][columna_media]
                if jugador == 'X':
                    if ficha_media in ('O', 'o'):
                        if ficha == 'x' or cambios_fila[i] == -2:
                            return True
                if jugador == 'O':
                    if ficha_media in ('X', 'x'):
                        if ficha == 'o' or cambios_fila[i] == 2:
                            return True
    return False
def hay_movimientos_disponibles(jugador):
    for fila in range(8):
        for columna in range(8):
            if (
                tablero[fila][columna] == jugador
                or tablero[fila][columna] == jugador.lower()
            ):
                if puede_mover_normalmente(fila, columna):
                    return True
                if puede_capturar_con_jugador(fila, columna, jugador):
                    return True
    return False
def cambiar_jugador(jugador):
    return 'O' if jugador == 'X' else 'X'
def mostrar_registro():
    print()
    print("====================================")
    print("        REGISTRO DE MOVIMIENTOS")
    print("====================================")
    if not movimientos:
        print("No hubo movimientos.")
    for i, mov in enumerate(movimientos):
        print(f"{i + 1}. {mov}")
    print("====================================")
def preguntar_guardar_partida():
    respuesta = input("Quieres guardar la partida? (S/N): ").strip()
    if respuesta.upper() == "S":
        mostrar_registro()
    else:
        print("El registro no se guardara.")
def main():
    global jugadorActual
    inicializar_tablero()
    partida_terminada = False
    print("====================================")
    print("         DAMAS INGLESAS")
    print("====================================")
    print("Jugador X: fichas X")
    print("Jugador O: fichas O")
    print()
    while not partida_terminada:
        mostrar_tablero()
        print()
        print(f"Turno del jugador: {jugadorActual}")
        print()
        movimiento_realizado = realizar_movimiento()
        if movimiento_realizado:
            siguiente_jugador = cambiar_jugador(jugadorActual)
            if not hay_movimientos_disponibles(siguiente_jugador):
                mostrar_tablero()
                print()
                print("====================================")
                print("          FIN DE LA PARTIDA")
                print("====================================")
                print(f"Ganador: jugador {jugadorActual}")
                print()
                partida_terminada = True
            else:
                jugadorActual = siguiente_jugador
    preguntar_guardar_partida()
    print()
    print("Programa terminado.")
if __name__ == "__main__":
    main()

