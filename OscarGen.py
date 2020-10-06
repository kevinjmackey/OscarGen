import argparse
from datetime import datetime
import logging as log
import json
import os
import pyratemp
import shutil
import sys
import uast

OSCAR_VERSION = "1.0"

class Datastore:
    _ID = ""
    _internalType = ""
    _properties = {}
    _token = ""
    _roles = []

    def __init__(self, id):
        self._ID = id
        self._internalType = "dvo:Datastore"
        self._properties = {}
        self._token = ""
        self._roles = []
        self._parent = None

    @property
    def ID(self):
        return self._ID

    @property
    def Properties(self):
        return self._properties

    def AddProperty(self, name, value):
        self._properties[name] = str(value).replace("\"","").replace("[","").replace("]","")

    @property
    def InternalType(self):
        return self._internalType

    @property
    def Name(self):
        return self._token if len(self._token) > 0 else ""
        
    @property
    def Token(self):
        return self._token if len(self._token) > 0 else ""
    @Token.setter
    def Token(self, value):
        self._token = value

    @property
    def DisplayName(self):
        return self.GetProperty("Display Name") if "Display Name" in self._properties else self.Name

    @property
    def Roles(self):
        return self._roles

    def AddRole(self, role):
        self._roles.append(role)

    def HasProperty(self, key):
        return True if key in self._properties else False
    def GetProperty(self, key):
        return self._properties[key] if key in self._properties else ""

class Item:
    _ID = ""
    _internalType = ""
    _properties = {}
    _associations = []
    _attributes = []
    _childItems = []
    _token = ""
    _roles = []
    _parent = None
    _datastore = None

    def __init__(self, id):
        self._ID = id
        self._internalType = "dvo:Item"
        self._properties = {}
        self._associations = []
        self._attributes = []
        self._childItems = []
        self._token = ""
        self._roles = []
        self._parent = None
        self._datastore = None

    @property
    def ID(self):
        return self._ID

    @property
    def Properties(self):
        return self._properties

    def AddProperty(self, name, value):
        self._properties[name] = str(value).replace("\"","").replace("[","").replace("]","")

    @property
    def InternalType(self):
        return self._internalType
    @InternalType.setter
    def InternalType(self, value):
        self._internalType = value

    @property
    def Name(self):
        return self._token if len(self._token) > 0 else ""
        
    @property
    def CapName(self):
        return self._token[0].upper() + self._token[1:].lower()

    @property
    def Token(self):
        return self._token if len(self._token) > 0 else ""
    @Token.setter
    def Token(self, value):
        self._token = value

    @property
    def Datastore(self):
        return self._datastore
    @Datastore.setter
    def Datastore(self, item):
        self._datastore = item

    @property
    def HasSchema(self):
        return "Schema" in self._properties
    @property
    def Schema(self):
        return self.GetProperty("Schema") if "Schema" in self._properties else None

    @property
    def DisplayName(self):
        return self.GetProperty("Display Name") if "Display Name" in self._properties else self.Name

    @property
    def Plural(self):
        return self.GetProperty("Plural") if "Plural" in self._properties else f"{self.Name}s"
    @property
    def CapPlural(self):
        return self.Plural[0].upper() + self.Plural[1:].lower()

    @property
    def Roles(self):
        return self._roles

    def AddRole(self, role):
        self._roles.append(role)

    @property
    def Attributes(self):
        return self._attributes

    @property
    def HasAssociations(self):
        return len(self._associations) > 0

    @property
    def Associations(self):
        return self._associations

    @property
    def PKattributes(self):
        pkAttributes = []
        for attrib in self._attributes:
            if attrib.GetProperty("PK") == "true":
                pkAttributes.append(attrib)
        return pkAttributes

    def AddAssociation(self, association):
        self._associations.append(association)

    def AddAttribute(self, attribute):
        self._attributes.append(attribute)

    def AddChildItem(self, item):
        self._childItems.append(item)

    @property
    def HasAttributes(self):
        return len(self._attributes) > 0
    @property
    def AttributeCount(self):
        return len(self._attributes)
    @property
    def FirstAttribute(self):
        return self._attributes[0] if self.HasAttributes() == True else None
    def HasRole(self, role):
        return True if role in self._roles else False
    def HasProperty(self, key):
        return True if key in self._properties else False
    def GetProperty(self, key):
        return self._properties[key] if key in self._properties else ""
    @property
    def HasParentItem(self):
        return True if self._parent != None and self._parent.InternalType == "dvo:Item" else False
    @property
    def Parent(self):
        return self._parent if self._parent != None else None
    @Parent.setter
    def Parent(self, item):
        self._parent = item
    @property
    def HasChildItems(self):
        return len(self._childItems) > 0
    @property
    def ChildItems(self):
        return self._childItems

class Association:
    _ID = ""
    _internalType = ""
    _token = ""
    _properties = {}
    _roles = []

    def __init__(self, id):
        self._ID = id
        self._internalType = "dvo:Association"
        self._properties = {}
        self._token = ""
        self._roles = []
    @property
    def InternalType(self):
        return self._internalType
    @InternalType.setter
    def InternalType(self, value):
        self._internalType = value

    @property
    def Name(self):
        return self._token if len(self._token) > 0 else ""
        
    @property
    def Token(self):
        return self._token if len(self._token) > 0 else ""
    @Token.setter
    def Token(self, value):
        self._token = value

    @property
    def Cardinality(self):
        return self.GetProperty("Cardinality")

    @property
    def Item(self):
        return self.GetProperty("Item")

    @property
    def FromKey(self):
        return self.GetProperty("FromKey")

    @property
    def ToKey(self):
        return self.GetProperty("ToKey")

    @property
    def Roles(self):
        return self._roles

    def AddProperty(self, name, value):
        self._properties[name] = str(value).replace("\"","").replace("[","").replace("]","")

    def AddRole(self, role):
        self._roles.append(role)
    def HasRole(self, role):
        return True if role in self._roles else False

    def HasProperty(self, key):
        return True if key in self._properties else False
    def GetProperty(self, key):
        return self._properties[key] if key in self._properties else ""

class Attribute:
    _ID = ""
    _internalType = ""
    _properties = {}
    _token = ""
    _roles = []

    def __init__(self, id):
        self._ID = id
        self._internalType = "dvo:Attribute"
        self._properties = {}
        self._token = ""
        self._roles = []

    @property
    def ID(self):
        return self._ID

    @property
    def Properties(self):
        return self._properties

    def AddProperty(self, name, value):
        self._properties[name] = str(value).replace("\"","").replace("[","").replace("]","")

    @property
    def InternalType(self):
        return self._internalType
    @InternalType.setter
    def InternalType(self, value):
        self._internalType = value

    @property
    def Name(self):
        return self._token if len(self._token) > 0 else ""
        
    @property
    def Token(self):
        return self._token if len(self._token) > 0 else ""
    @Token.setter
    def Token(self, value):
        self._token = value

    @property
    def Datatype(self):
        return self.GetProperty("Datatype")

    @property
    def Default(self):
        self.GetProperty("Default")

    @property
    def DisplayName(self):
        return self.GetProperty("Display Name") if "Display Name" in self._properties else self.Name

    @property
    def Roles(self):
        return self._roles

    def AddRole(self, role):
        self._roles.append(role)

    def HasRole(self, role):
        return True if role in self._roles else False
    def HasProperty(self, key):
        return True if key in self._properties else False
    def GetProperty(self, key):
        return self._properties[key] if key in self._properties else ""

datastoreIDs = []
parentIDs = []
itemIDs = []
datastores = []
parentItems = []
items = []
tree = None

def GetParentByID(_ID):
    node = None
    for parent in parentItems:
        if parent._ID == _ID:
            node = parent
            break
    return node

def GetParentDatastore(_node):
    datastore = None
    datastore = _node.Parent if _node.Parent.RawInternalType == "dvo:Datastore" else GetParentDatastore(_node.Parent)
    return datastore

def MakeAnAttribute(node):
    anAttribute = Attribute(node.ID)
    anAttribute.Token = node.RawToken
    if node.HasProperties:
        for k,v in node._properties.items():
            anAttribute.AddProperty(k,v)
    if node.HasRoles:
        for role in node._roles:
             anAttribute.AddRole(role.name)

    return anAttribute

def MakeAnAssociation(node):
    anAssociation = Association(node.ID)
    anAssociation.Token = node.RawToken
    if node.HasProperties:
        for k,v in node._properties.items():
            anAssociation.AddProperty(k,v)
    if node.HasRoles:
        for role in node._roles:
             anAssociation.AddRole(role.name)

    return anAssociation

def MakeAnItem(node):
    anItem = Item(node.ID)
    anItem.Token = node.RawToken
    if node.HasProperties:
        for k,v in node._properties.items():
            anItem.AddProperty(k,v)
    if node.HasRoles:
        for role in node._roles:
             anItem.AddRole(role.name)
    for child in node.Children:
        if child.RawInternalType == "dvo:Association":
            anItem.AddAssociation(MakeAnAssociation(child))
        if child.RawInternalType == "dvo:Attribute":
            anItem.AddAttribute(MakeAnAttribute(child))
        if child.RawInternalType == "dvo:Item":
            anItem.AddChildItem(MakeAnItem(child))
    if node.Parent.RawInternalType == "dvo:Item":
        anItem.Parent = GetParentByID(node.Parent._ID)
    if node.Parent.RawInternalType == "dvo:Datastore":
        anItem.Parent = MakeADatastore(node.Parent)
    anItem.Datastore = GetParentDatastore(node)
    return anItem

def MakeADatastore(node):
    aDatastore = Datastore(node.ID)
    aDatastore.Token = node.RawToken
    if node.HasProperties:
        for k,v in node._properties.items():
            aDatastore.AddProperty(k,v)
    if node.HasRoles:
        for role in node._roles:
             aDatastore.AddRole(role.name)

    return aDatastore

def WalkTheTree(_node):
    if _node.RawInternalType == "dvo:Datastore":
        datastoreIDs.append(_node.ID)
    if _node.RawInternalType == "dvo:Item":
        if _node.ID not in itemIDs:
            itemIDs.append(_node.ID)
        if _node._parent.RawInternalType == "dvo:Item":
            if _node.Parent.ID not in parentIDs:
                parentIDs.append(_node.Parent.ID)
    for child in _node.Children:
        WalkTheTree(child)

def PopulateArrays(astTree):
    if astTree.RawInternalType == "dvo:Item":
        itemIDs.append(astTree.ID)
    for child in astTree.Children:
        WalkTheTree(child)
    for datastoreID in datastoreIDs:
        datastores.append(MakeADatastore(astTree.GetNodeByID(datastoreID)))
    for parentID in parentIDs:
        parentItems.append(MakeAnItem(astTree.GetNodeByID(parentID)))
    for itemID in itemIDs:
        items.append(MakeAnItem(astTree.GetNodeByID(itemID)))

class AppFile:
    label = ""
    outputFile = ""
    outputFolder = ""
    fileName = ""
    skipChildItems = False
    action = ""
    include = []
    exclude = []

datastores = []
items = []

def ApplyTemplate(_dict, _templateString):
    localDict = _dict
    t = pyratemp.Template(_templateString)
    return str(t(**localDict))

def ParseAppConfig(jsonString):
    appConfig = {}
    appFiles = []
    jsonObject = json.loads(jsonString)
    appConfig = jsonObject["Application"]

    files = jsonObject["Files"]
    for fileElement in files:
        appFile = AppFile()
        appFile.label = fileElement["Label"]
        appFile.outputFile = fileElement["OutputFile"]
        appFile.outputFolder = fileElement["OutputFolder"]
        appFile.fileName = fileElement["FileName"]
        appFile.action = str(fileElement["Action"]).upper()
        appFile.skipChildItems = True if "SkipChildItems" in fileElement else False
        appFile.include = fileElement["Include"] if "Include" in fileElement else None
        appFile.exclude = fileElement["Exclude"] if "Exclude" in fileElement else None
        appFiles.append(appFile)

    return appConfig, appFiles

def ProcessStaticFile(appConfig, appFile):
    folder = ApplyTemplate(appConfig, appFile.outputFolder)
    os.makedirs(folder, exist_ok=True)
    shutil.copyfile(appFile.fileName, folder + ApplyTemplate(appConfig, appFile.outputFile))
    
def ProcessOnceFiles(appConfig, appFile):
    localDict = {}
    itemsToProcess = [i for i in items if i.Name in appFile.include] if appFile.include != None else items
    itemsToProcess = itemsToProcess if appFile.exclude == None else [i for i in itemsToProcess if i.Name not in appFile.exclude]
    itemsToProcess = itemsToProcess if appFile.skipChildItems == False else [i for i in itemsToProcess if i.HasChildItems == True]
    for k,v in appConfig.items():
        localDict[k] = v
    folder = ApplyTemplate(appConfig, appFile.outputFolder)
    outputFile = folder + ApplyTemplate(appConfig, appFile.outputFile)
    os.makedirs(folder, exist_ok=True)
    localDict["oscar_version"] = OSCAR_VERSION
    localDict["date"] = str(datetime.now())
    localDict["items"] = itemsToProcess
    if len(datastores) > 0:
        localDict["datastores"] = datastores
    t = pyratemp.Template(filename=appFile.fileName)
    with open(outputFile, "w") as fout:
        fout.write(t(**localDict))

def ProcessEachFiles(appConfig, appFile):
    localDict = {}
    itemsToProcess = [i for i in items if i.Name in appFile.include] if appFile.include != None else items
    itemsToProcess = itemsToProcess if appFile.exclude == None else [i for i in itemsToProcess if i.Name not in appFile.exclude]
    itemsToProcess = itemsToProcess if appFile.skipChildItems == False else [i for i in itemsToProcess if i.HasParentItem == False]
    localDict["oscar_version"] = OSCAR_VERSION
    for k,v in appConfig.items():
        localDict[k] = v
    localDict["date"] = str(datetime.now())
    if len(datastores) > 0:
        localDict["datastores"] = datastores
    t = pyratemp.Template(filename=appFile.fileName)
    for item in itemsToProcess:
        localDict["item"] = item
        folder = ApplyTemplate(localDict, appFile.outputFolder)
        os.makedirs(folder, exist_ok=True)
        outputFile = folder + ApplyTemplate(localDict, appFile.outputFile)
        with open(outputFile, "w") as fout:
            fout.write(t(**localDict))

def ProcessAppFiles(appConfig, appFiles):
    log.info("Beginning application files processing...")
    for appFile in appFiles:
        log.info(f"Processing file: {appFile.label}")
        if appFile.action == "COPY":
            ProcessStaticFile(appConfig, appFile)
        if appFile.action == "ONCE":
            ProcessOnceFiles(appConfig, appFile)
        if appFile.action == "EACH":
            ProcessEachFiles(appConfig, appFile)

def initLogging():
    log.basicConfig(level=log.INFO,
                    format="[%(levelname)s] %(funcName)s:: %(message)s",
                    filename=os.path.join(os.getcwd(), "OscarGen.log")
                    )

def Main(_argv):
    #Script starts here
    version = "1.0"
    initLogging()
    log.info(f"Run started at {datetime.now()}")
    argsparser = argparse.ArgumentParser(prog="OscarGen")
    argsparser.add_argument("-c", "--config", dest="config", default="AppGenConfig.json", type=argparse.FileType(), help="This file lists the templates and how they should be used.")
    argsparser.add_argument("-m", "--metadata", dest="metadata", type=argparse.FileType(), help="This file declares the Items (entities) for which code should be generated.")
    args = argsparser.parse_args()

    appConfig = {}
    appFiles = []
    with args.config as c:
        appConfig, appFiles = ParseAppConfig(c.read())

    log.info(f"Loading Oscar metadata...Generator Version {version}")
    with args.metadata as m:
        jsonString = m.read()

    tree = uast.UastNode.BuildAstTree(jsonString)

    PopulateArrays(tree)

    log.info(f"Starting Oscar code generation...Generator Version {version}")
    ProcessAppFiles(appConfig, appFiles)

    log.info(f"Finishing Oscar code generation...Generator Version {version}")
    log.info(f"Run ended at {datetime.now()}")

if __name__ == "__main__":
    Main(sys.argv)
