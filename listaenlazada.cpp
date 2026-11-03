#include <iostream>
using namespace std;
struct Nodo {
    int dato;
    Nodo* siguiente;
    Nodo(int valor) : dato(valor), siguiente(nullptr) {}
};
void insertarAlFinal(Nodo*&cabeza, int valor) {
    Nodo* nuevoNodo = new Nodo(valor);
    if (cabeza==nullptr){
        cabeza=nuevoNodo;
        return;
    }
    Nodo*actual=cabeza;
    while (actual->siguiente != nullptr) {
        actual=actual->siguiente;
    }
    actual->siguiente=nuevoNodo;
}
void imprimirLista(Nodo*cabeza){
    Nodo*actual=cabeza;
    bool primero=true;
    while(actual!=nullptr){
        if(!primero)cout<< " ";
        cout<<actual->dato;
        primero=false;
        actual=actual->siguiente;
    }
    cout<<endl;
}
int main(){
    Nodo*cabeza=nullptr;
    insertarAlFinal(cabeza, 10);
    insertarAlFinal(cabeza, 20);
    insertarAlFinal(cabeza, 30);
    insertarAlFinal(cabeza, 40);
    imprimirLista(cabeza);
    Nodo*actual=cabeza;
    while(actual!=nullptr) {
        Nodo*siguienteNodo=actual->siguiente;
        delete actual;
        actual=siguienteNodo;
    }
    return 0;
}