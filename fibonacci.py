import ast
import inspect

# a biblioteca ast vai ser necessaria para permitir analisar o código-fonte Python 
# e a inspect vai  fornecer varias ferramentas para  inspecionar objetos como módulos e funçoes.


def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def identificarRecursaoManual(func, n):
    # Função para identificar recursão manualmente.
    if n == 0:
        return [func(n)]
    else:
        serie = identificarRecursaoManual(func, n - 1)  #aqui vai criar uma lista contendo as chamadas recursivas 
        serie.append(func(n)) #aqui com o append vai adicionar a func para lista serie 
        return serie    

def identificarRecursaoEstatica(func):
    # Função para identificar chamadas recursivas usando análise estática.
    codigoFonte = inspect.getsource(func)
    arvore = ast.parse(codigoFonte)   #converte o código-fonte em uma árvore de análise sintática usando o módulo ast.

    chamadasRecursivas = []  #Uma lista é inicializada para armazenar as chamadas recursivas identificadas.

    # Este visitante percorre a árvore de análise sintática da função.
    class Visitante(ast.NodeVisitor):
        def visit_Call(self, node): #O método visit_Call é chamado sempre que um nó de chamada de função é encontrado.
           
            if isinstance(node.func, ast.Name) and node.func.id == func.__name__:
                chamadasRecursivas.append(ast.get_source_segment(codigoFonte, node))

    Visitante().visit(arvore) #instância de Visitante é criada e aplicada a árvore de análise sintática 

    return chamadasRecursivas

def identificarRecursaoPersonalizada(func, n, chamadas=[]):
    # Função para identificar chamadas recursivas personalizadamente.
    
    if n == 0:
        return chamadas
    else:
        chamadas.append(func(n)) #Antes de fazer a chamada recursiva, a função atual (func(n)) é adicionada à lista de chamadas.
        return identificarRecursaoPersonalizada(func, n - 1, chamadas)

def resultado(func, n):
    # Exibe o resultado da identificação de recursão manual.
    
    print("Identificando recursão na função", func.__name__, "para n =", n, ":")
    resultadoRecursao = identificarRecursaoManual(func, n)
    for i, valor in enumerate(resultadoRecursao):
        print("Passo", i + 1, ":", valor)

def aplicando(func, n):
    
    resultado(func, n)

    chamadasRecursivasEstaticas = identificarRecursaoEstatica(func)
    print("\nIdentificando estaticamente chamadas recursivas:")
    for chamada in chamadasRecursivasEstaticas:
        print(chamada)

    chamadaRecursivaPersonalizada = identificarRecursaoPersonalizada(func, n)
    print("\nIdentificando personalizadamente chamadas recursivas:")
    for i, chamada in enumerate(chamadaRecursivaPersonalizada):
        print("Passo", i + 1, ":", chamada)


aplicando(fibonacci, 5)
