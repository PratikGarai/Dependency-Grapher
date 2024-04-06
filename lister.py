import ast
import os
import glob

files  = glob.glob("sample/**/*.py", recursive=True)
print(files)

entry = os.path.join("sample", "main.py")

if __name__ == "__main__" :
    node = ast.parse(open(entry).read())

    print(type(node))

    classes = [c for c in node.body if isinstance(c, ast.ClassDef)]
    print("\nClasses: ")
    for c in classes:
        print(c.name)

    functions = [f for f in node.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))]
    print("\nFunctions: ")
    for f in functions:
        print(f.name)

    imported_classes = [c for c in node.body if isinstance(c, (ast.ImportFrom))]
    print("\nImported classes: ")
    for c in imported_classes:
        print(c.module)
        for obj in c.names:
            print(obj.name)