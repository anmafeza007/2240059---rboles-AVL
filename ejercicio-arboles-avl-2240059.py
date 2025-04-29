# Clase que representa un nodo en el árbol AVL
class Node:
    def __init__(self, value):
        self.value = value  
        self.left = None   
        self.right = None   
        self.height = 1  

# Obtiene la altura de un nodo; si es None, retorna 0
def getHeight(node):
    return node.height if node else 0

# Calcula el factor de balance de un nodo
def getBalance(node):
    return getHeight(node.left) - getHeight(node.right) if node else 0

# Actualiza la altura de un nodo según la altura de sus hijos
def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

# ------------------- ROTACIONES -------------------

# Rotación simple a la derecha
def rotate_right(y):
    x = y.left          
    T2 = x.right       

    x.right = y
    y.left = T2

    updateHeight(y)
    updateHeight(x)

    return x  

# Rotación simple a la izquierda
def rotate_left(x):
    y = x.right         
    T2 = y.left         

    y.left = x
    x.right = T2

    updateHeight(x)
    updateHeight(y)

    return y


class AVLTree:
    def __init__(self):
        self.root = None  # Inicializa el árbol vacío

    # Inserta un valor en el árbol
    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    # Función recursiva para insertar y reequilibrar
    def _insert_recursive(self, node, value):
        # Caso base: inserta el nuevo nodo
        if not node:
            return Node(value)

        # Navega el árbol según propiedad BST
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node  # No permite duplicados

        # Actualiza altura y calcula balance
        updateHeight(node)
        balance = getBalance(node)

        # Rebalanceo según los 4 casos posibles

        # Caso Izquierda-Izquierda
        if balance > 1 and value < node.left.value:
            return rotate_right(node)

        # Caso Izquierda-Derecha
        if balance > 1 and value > node.left.value:
            node.left = rotate_left(node.left)
            return rotate_right(node)

        # Caso Derecha-Derecha
        if balance < -1 and value > node.right.value:
            return rotate_left(node)

        # Caso Derecha-Izquierda
        if balance < -1 and value < node.right.value:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node  # Retorna el nodo balanceado

    # Elimina un valor del árbol
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    # Función recursiva para eliminar un nodo
    def _delete_recursive(self, node, value):
        if not node:
            return node  # Valor no encontrado

        # Buscar el nodo a eliminar
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Caso 1: nodo sin hijos o con un hijo
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Caso 2: nodo con dos hijos
            temp = self._get_min_value_node(node.right)  # Nodo más pequeño en subárbol derecho
            node.value = temp.value  # Copia el valor
            node.right = self._delete_recursive(node.right, temp.value)  # Elimina duplicado

        # Actualizar altura y rebalancear
        updateHeight(node)
        balance = getBalance(node)

        # Rebalanceo después de eliminación

        # Izquierda-Izquierda
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)

        # Izquierda-Derecha
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)

        # Derecha-Derecha
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)

        # Derecha-Izquierda
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node  # Retorna nodo balanceado

    # Obtiene el nodo con valor mínimo (para eliminación)
    def _get_min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    # Realiza recorrido in-order del árbol y devuelve los valores en lista
    def inorder_traversal(self):
        return self._inorder_recursive(self.root)

    def _inorder_recursive(self, node):
        if not node:
            return []
        return self._inorder_recursive(node.left) + [node.value] + self._inorder_recursive(node.right)

    # Imprime la estructura del árbol de forma visual
    def print_tree(self, node=None, level=0, label="Root"):
        if node is None:
            node = self.root
        if node.right:
            self.print_tree(node.right, level + 1, "R")
        print("   " * level + f"{label}: ({node.value}, h={node.height})")
        if node.left:
            self.print_tree(node.left, level + 1, "L")