'''
Created on Mar 3, 2014

@author: Jing
'''

import xml.etree.ElementTree as xmlElementTree
from xml.etree.ElementTree import Element, SubElement #, ElementTree, dump, tostring
import xml.dom.minidom as MiniDom
import types as Types

def saveXML(root, pzFile):
    """
    Method: SaveXML(Element root, string pzFile)
    Description: format xml to a pretty-printed string and write it out
    """
    doc = MiniDom.parseString(xmlElementTree.tostring(root))
    prettyxml = doc.toprettyxml(indent="\t", newl="\r\n") #  encoding='utf-8'
    #file_object = open(pzFile, "w")
    #file_object.write(prettyxml)
    #file_object.close()
    return prettyxml

def loadXML(pzFile):
    tree = xmlElementTree.parse(pzFile)
    root = tree.getroot()
    return root


class CSimpleXMLSerializer:
    def __init__(self):
        self.buildInTypes = [Types.BooleanType, Types.FloatType, Types.IntType, Types.LongType, Types.StringType]
        self.buildInCreators = {Types.BooleanType.__name__:bool,
                                Types.FloatType.__name__:float,
                                Types.IntType.__name__:int,
                                Types.LongType.__name__:long,
                                Types.StringType.__name__:str}


    def serialize(self, obj, pzFile, rootName=None):
        if rootName==None:
            rootName = obj.__class__.__name__
        root = Element(rootName)
        self.toXML(obj, root)
        return saveXML(root, pzFile)
         
    def deserialize(self, pzFile, obj):
        root = loadXML(pzFile)
        self.fromXML(root, obj)
    
    def toXML(self, obj, root):
        self.simpleAttrs2XmlElem(obj, root)
        self.specialAttrs2XmlElem(obj, root)
        
    
    def fromXML(self, root, obj):
        self.xmlElem2SimpleAttrs(root, obj)
        self.xmlElem2SpecialAttrs(root, obj)
        
    
    def getAttrs(self, obj):
        return dir(obj)
    
    def specialAttrs2XmlElem(self, obj, root):
        pass
    
    def xmlElem2SpecialAttrs(self, root, obj):
        pass
    
    def simpleAttrs2XmlElem(self, obj, root):
        attributes = self.getSimpleAttrs(obj)
        for attrName in attributes:
            value = getattr(obj, attrName)
            subElem  = SubElement(root, attrName)
            subElem.attrib["typeName"] = type(value).__name__
            subElem.text = str(value)
      
    
    def xmlElem2SimpleAttrs(self, root, obj):
        attributes = self.getSimpleAttrs(obj)
        for attrName in attributes:
            elem = root.find(attrName)
            if elem == None:
                print("no element for attribute: " + attrName)

            attTypeName = elem.attrib['typeName']
            value = self.buildInCreators[attTypeName](elem.text)
            setattr(obj, attrName, value)
    
    def getSimpleAttrs(self, obj):
        simpleAttributes = []
        attributes = self.getAttrs(obj)
        for attrName in attributes:
            value = getattr(self, attrName)
            if type(value) in self.buildInTypes:
                simpleAttributes.append(attrName)
                
        return simpleAttributes
    
    
    

    
class CTestClass():
    def __init__(self):
        attrI = 1
        attrS = "str"
        attrF = 1.0
        

obj = CTestClass()
xmlS = CSimpleXMLSerializer()
print xmlS.serialize(obj, "test", "test_class")
