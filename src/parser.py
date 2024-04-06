import ast

class Entity:
    '''
    Entity class is used to store the information of the file.
    '''

    def __init__(self, path: str):
        self.path = path
        self.own_classes = []
        self.own_functions = []
        self.own_variables = []
        self.imports = []

    def parse(self):
        node = ast.parse(open(self.path).read())

        self.own_classes = [c for c in node.body if isinstance(c, ast.ClassDef)]
        self.own_functions = [f for f in node.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))]
        self.own_variables = [v for v in node.body if isinstance(v, (ast.Assign))]

        self.imports = [v for v in node.body if isinstance(v, (ast.ImportFrom, ast.Import))]

    def display(self):
        print(f"==============\nPath: {self.path}")
        print("\nClasses: ")
        for c in self.own_classes:
            print(c.name)

        print("\nFunctions: ")
        for f in self.own_functions:
            print(f.name)

        print("\nVariables: ")
        for v in self.own_variables:
            print(v.targets[0].id)

        print("\nImports: ")
        for c in self.imports:
            if isinstance(c, ast.ImportFrom):
                print(f"Module : {c.module}")
                for obj in c.names:
                    print(obj.name)
            elif isinstance(c, ast.Import):
                for obj in c.names:
                    print(f"Direct Import : {obj.name}")
        
        print("==============")