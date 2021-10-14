import ast

expr = 'fish & fish'

t = ast.parse(expr)
# t.parse(expr)
# print(ast.dump(t))
# for exp in t.body:
#     print(type(exp))
exprBody = t.body
# print(type(exprBody))
for body in exprBody:
    if (type(body) is ast.Expr):
        exprValue = body.value
        # print(exprValue)
        print(type(exprValue))
        if type(exprValue) is ast.Name:
            print(exprValue.id)
        elif type(exprValue) is ast.BinOp:
            left = exprValue.left
            right = exprValue.right
            op = exprValue.op
            print(left, right, op)
# for ep in ast.dump(t):
#     print(ep)