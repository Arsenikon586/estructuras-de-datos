import curses
import time
# 1:estado global y configuracion
tablero = [[' ' for _ in range(8)] for _ in range(8)]
movimientos = []
jugadorActual = 'X'
cursor_fila = 5
cursor_columna = 0
seleccion = None
TIEMPO_LIMITE = 15
# 2:logica y reglas
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
    if tablero[fila][columna] == 'O' and fila == 7:
        tablero[fila][columna] = 'o'
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
        print("No hubo movimientos")
    for i, mov in enumerate(movimientos):
        print(f"{i + 1}. {mov}")
    print("====================================")
def preguntar_guardar_partida():
    respuesta = input("Quieres guardar la partida? (S/N): ").strip()
    if respuesta.upper() == "S":
        mostrar_registro()
    else:
        print("El registro no se guardara")
# 3:interfaz de renderizado
def mostrar_tablero_curses(stdscr, tiempo_restante, mensaje=""):
    stdscr.erase()
    stdscr.addstr(0, 0, "====================================")
    stdscr.addstr(1, 0, f"         DAMAS INGLESAS (Turno: {jugadorActual})")
    stdscr.addstr(2, 0, f"         Tiempo restante: {tiempo_restante:02d}s", curses.A_REVERSE if tiempo_restante <= 5 else 0)
    stdscr.addstr(3, 0, "====================================")
    stdscr.addstr(4, 0, " Controles: Flechas (Mover), Enter/Espacio (Seleccionar), Q (Salir)")
    stdscr.addstr(6, 0, "       1   2   3   4   5   6   7   8")
    stdscr.addstr(7, 0, "     #---#---#---#---#---#---#---#---#")
    for fila in range(8):
        stdscr.addstr(8 + (fila * 2), 0, f" {fila + 1}   |")
        for columna in range(8):
            attr = curses.A_NORMAL
            if fila == cursor_fila and columna == cursor_columna:
                attr = curses.A_REVERSE
            elif seleccion == (fila, columna):
                attr = curses.A_BOLD
            val = tablero[fila][columna]
            stdscr.addstr(8 + (fila * 2), 7 + (columna * 4), f" {val} ", attr)
            stdscr.addstr(8 + (fila * 2), 10 + (columna * 4), "|")
        stdscr.addstr(9 + (fila * 2), 0, "     #---#---#---#---#---#---#---#---#")
    if mensaje:
        stdscr.addstr(25, 0, f"Info: {mensaje}")
    stdscr.refresh()
# 4:adicion de entrada por teclado y temporizador
def main_curses(stdscr):
    global jugadorActual, cursor_fila, cursor_columna, seleccion
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    inicializar_tablero()
    tiempo_inicio = time.time()
    mensaje = "Selecciona una ficha"
    while True:
        tiempo_transcurrido = time.time() - tiempo_inicio
        tiempo_restante = max(0, int(TIEMPO_LIMITE - tiempo_transcurrido))
        if tiempo_restante == 0:
            jugadorActual = cambiar_jugador(jugadorActual)
            seleccion = None
            tiempo_inicio = time.time()
            mensaje = "Tiempo agotado, cambiando turno..."
            continue
        mostrar_tablero_curses(stdscr, tiempo_restante, mensaje)
        try:
            key = stdscr.getch()
        except Exception:
            key = -1
        if key == -1:
            time.sleep(0.05)
            continue
        if key == curses.KEY_UP and cursor_fila > 0:
            cursor_fila -= 1
        elif key == curses.KEY_DOWN and cursor_fila < 7:
            cursor_fila += 1
        elif key == curses.KEY_LEFT and cursor_columna > 0:
            cursor_columna -= 1
        elif key == curses.KEY_RIGHT and cursor_columna < 7:
            cursor_columna += 1
        elif key in (10, 13, 32):  # Enter o Espacio
            if seleccion is None:
                if tablero[cursor_fila][cursor_columna] in (jugadorActual, jugadorActual.lower()):
                    seleccion = (cursor_fila, cursor_columna)
                    mensaje = f"Ficha ({cursor_fila + 1},{cursor_columna + 1}) seleccionada"
                else:
                    mensaje = "Posicion invalida o ficha ajena"
            else:
                f_orig, c_orig = seleccion
                f_dest, c_dest = cursor_fila, cursor_columna
                if (f_orig, c_orig) == (f_dest, c_dest):
                    seleccion = None
                    mensaje = "Selección cancelada"
                    continue
                if tablero[f_dest][c_dest] != ' ':
                    mensaje = "La posicion destino esta ocupada"
                    continue
                es_captura = es_movimiento_de_captura(f_orig, c_orig, f_dest, c_dest)
                movimiento_normal = es_movimiento_normal(f_orig, c_orig, f_dest, c_dest)
                if not es_captura and not movimiento_normal:
                    mensaje = "Movimiento no valido"
                    continue
                if es_captura:
                    fila_media = (f_orig + f_dest) // 2
                    columna_media = (c_orig + c_dest) // 2
                    tablero[fila_media][columna_media] = ' '
                tablero[f_dest][c_dest] = tablero[f_orig][c_orig]
                tablero[f_orig][c_orig] = ' '
                coronar_ficha(f_dest, c_dest)
                guardar_movimiento(f_orig, c_orig, f_dest, c_dest, es_captura)
                if es_captura and puede_capturar_desde(f_dest, c_dest):
                    seleccion = (f_dest, c_dest)
                    mensaje = "Puedes realizar otra captura"
                else:
                    seleccion = None
                    siguiente_jugador = cambiar_jugador(jugadorActual)
                    if not hay_movimientos_disponibles(siguiente_jugador):
                        mostrar_tablero_curses(stdscr, 0, f"FIN DE LA PARTIDA Ganador: {jugadorActual}")
                        time.sleep(3)
                        break
                    jugadorActual = siguiente_jugador
                    tiempo_inicio = time.time()
                    mensaje = f"Turno del jugador {jugadorActual}"
        elif key in (ord('q'), ord('Q')):
            break
def main():
    curses.wrapper(main_curses)
    preguntar_guardar_partida()
    print()
    print("Programa terminado")
if __name__ == "__main__":
    main()