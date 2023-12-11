from ast import NodeVisitor
from ast import iter_fields, AST, If, arguments
from queue import Queue

# Clase para contar el numero de declaraciones if anidadas en un codigo
class ASTNestedIfCounter(NodeVisitor):

    count : int      # registro del numero total de declaraciones if encontradas 
    nested_if : int  # contador del numero de declaraciones if anidadas 

    # Constructor de la clase 
    def __init__(self) -> None:
        self.count = 0
        self.nested_if = 0

    # Devuelve el maximo nivel de anidamiento de expresiones if a partir de un nodo del AST "node" 
    def generic_visit(self, node):
        '''
        Generic visit of the code
        '''
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.visit(item)
                    elif isinstance(value, AST):
                        self.visit(value)

        return self.nested_if
    
    # Cada vez que se encuentra un if, se aumenta el contador de declaraciones if encontradas
    def visit_If(self, node):
        '''
        If is visited in this function
        '''
        # +1 por que se encontro un if anidado
        self.count+=1

        # explora el if
        for _, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    # si encuentra otro if, explora el if 
                    if isinstance(item, If):
                        self.visit(item)
        
        # si el if actual tiene mas anidamiento que el anterior, se actualiza 
        if self.count > self.nested_if:
            self.nested_if = self.count
        
        self.count = 0

# Clase para generar un grafo .dot a partir de un nodo del AST
class ASTDotVisitor(NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.state_count = 0
        self.depth = 0

    def generic_visit(self, node: AST):
        self.depth += 1

        string, node_id = self.dot_state(node)
        interior = ""
        comma_counter = 0
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    s_id, s_string = self.visit(item)

                    # Añadimos la transición a la lista + descripción del subárbol
                    string += "\n" + node_id + " -> " + s_id + \
                        "[label=\"%s\"]\n" % (field) + s_string
            elif isinstance(value, AST):
                s_id, s_string = self.visit(value)

                # Añadimos la transición a la lista + descripción del subárbol
                string += "\n" + node_id + " -> " + s_id + \
                    "[label=\"%s\"]\n" % (field) + s_string
            else:
                if comma_counter == 0:
                    interior += "%s=%s" % (field, value)
                else:
                    interior += ", %s=%s" % (field, value)
                comma_counter += 1

        # Rellenamos el interior del nodo y decrementamos la profundidad
        string = string % interior
        self.depth -= 1

        # Caso final: Todos los subárboles han devuelto su descripción
        if self.depth == 0:
            string = "digraph {\n" + string + "\n}"
            print(string)
        else:
            return node_id, string

    def dot_state(self, node: AST):
        """
        Método auxiliar para poner en formato .dot un nodo AST
        """
        x = str(type(node).__name__) + "(%s)"
        node_id = "s%d" % (self.state_count)
        string = 's%d[label="%s", shape=box]' % (self.state_count, x)
        self.state_count += 1
        return string, node_id
    