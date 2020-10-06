import uast

parent = uast.UastNode()
parent.InternalType = "dvo:Test"
parent.Token = "Testing"
parent.AddRole(uast.Role.FILE)
parent.AddRole(uast.Role.BLOCK)
parent.AddProperty("PK", "True")
string = """InternalType: {0}, Token: {1} 
    Roles: {2} ID: {3}
    Properties: {4}""".format(parent.InternalType, parent.Token, parent.Roles, parent._ID, parent.Properties)
# print(string)
# print(parent.GetProperty("PK"))
# print(parent.ToString())
with open("Sample.json", "r") as r_in:
    jsonString = r_in.read()
tree = uast.UastNode.BuildAstTree(jsonString)
print(tree.ToString())
print(tree._ID)
print(tree.Name)
