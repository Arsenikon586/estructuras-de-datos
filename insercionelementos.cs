using System;
class Nodo {
    public int dato;
    public Nodo siguiente;
    public Nodo(int valor) {
        dato = valor;
        siguiente = null;
    }
}
class ListaEnlazada {
    public static void InsertarEnPosicion(ref Nodo cabeza, int posicion, int valor) {
        if(posicion<0){
            Console.WriteLine("Error: Posición inválida.");
            return;
        }
        Nodo nuevoNodo=new Nodo(valor);

        if(posicion==0){
            nuevoNodo.siguiente=cabeza;
            cabeza=nuevoNodo;
            return;
        }
        Nodo actual=cabeza;
        int indiceActual=0;
        while(actual != null && indiceActual<posicion-1){
            actual=actual.siguiente;
            indiceActual++;
        }
        if(actual == null){
            Console.WriteLine("Error: Posición fuera de rango.");
            return;
        }
        nuevoNodo.siguiente=actual.siguiente;
        actual.siguiente=nuevoNodo;
    }
    public static void ImprimirLista(Nodo cabeza) {
        Nodo actual=cabeza;
        bool primero=true;
        while (actual != null) {
            if (!primero) Console.Write(" -> ");
            Console.Write(actual.dato);
            primero=false;
            actual=actual.siguiente;
        }
        Console.WriteLine();
    }
    static void Main() {
        Nodo cabeza = null;
        InsertarEnPosicion(ref cabeza, 0, 5);
        InsertarEnPosicion(ref cabeza, 1, 15);
        InsertarEnPosicion(ref cabeza, 2, 25);
        Console.WriteLine("Lista inicial:");
        ImprimirLista(cabeza);
        Console.Write("\nIngrese la posición donde desea insertar: ");
        if (int.TryParse(Console.ReadLine(), out int posicion)) {
            Console.Write("Ingrese el valor del nodo: ");
            if (int.TryParse(Console.ReadLine(), out int valor)) {
                InsertarEnPosicion(ref cabeza, posicion, valor);
                Console.WriteLine("\nResultado:");
                ImprimirLista(cabeza);
            } else {
                Console.WriteLine("Valor inválido.");
            }
        } else {
            Console.WriteLine("Posición inválida.");
        }
    }
}