from d3_primeri.models import Attribute, Node, Link
from d3_primeri.services.ucitati import UcitatiService
import os
# instaliraj u virtualno okruzenja sa: pip install lxml
import lxml.html as htmlParser


class UcitatiHTMLIzvor(UcitatiService):
    def naziv(self):
        return "Ucitati html izvor"

    def identifier(self):
        return "ucitati_html_izvor"

    def ucitati(self, path):
        self.parseHTML(path)

    def addAttributes(self, node, n):
        if node.attrib != {}:
            for key in node.attrib.keys():
                a = Attribute(name=key, value=node.attrib[key])
                a.save()
                n.attributes.add(a)
            n.save()
        return n

    def findNode(self, node):
        if (node.tag == "head"):
            allNodes = Node.objects.all();

            for nodeDB in allNodes:
                if nodeDB.label == "head":
                    n = nodeDB
        else:
            n = Node(code=node, label=node.tag)
            if node.text != None and "\n" not in node.text:
                n.text = node.text
            else:
                n.text = ""
            n.save()
        return n;

    def addLink(self, node, child, n):
        label = node.tag + "->" + child.tag
        l = Link(label=label)
        l.parent_node = n
        child_node = Node(code=child, label=child.tag)
        # print("C-  ", child_node)
        if child.text != None and "\n" not in child.text:
            child_node.text = child.text
            print(child.text)
        else:
            child_node.text = ""
        child_node.save()
        l.child_node = child_node
        l.save()

    def parseHTML(self, path):
        print("parseHTML")
        # ako je apsolutna putanja onda na osnovu nje parsira
        if "\\" in path:
            full_file_path = path
            print("full_file_path ", full_file_path)
        # ako je relativna onda trazi taj fajl u static fajlovima
        else:
            abspath = os.path.abspath("")
            root_path = abspath[:-14]
            print("root_path", root_path)
            full_file_path = root_path + "D3Core\\d3_primeri\\static\\" + path
            print("full_file_path ", full_file_path)
        tree = htmlParser.parse(full_file_path)
        root = tree.getroot()
        print(root.tag)
        print(root.attrib)
        # kreiranje cvora i linkova za korijenski element

        n = Node(code=root, label=root.tag)
        n.save()
        n = self.addAttributes(root, n)
        if len(root) > 0:
            # print("Node2  ", node)
            for child in root:
                self.addLink(root, child, n)
        # kreiranje cvorova i linkova za ostale elemente
        nodes = root
        results = []
        while 1:
            newNodes = []
            if len(nodes) == 0:
                break
            for node in nodes:
                results.append(node)
                try:
                    n = Node.objects.get(code=node)
                except Node.DoesNotExist:
                    n = self.findNode(node)
                n = self.addAttributes(node, n)
                if len(node) > 0:
                    for child in node:
                        self.addLink(node, child, n)
                        newNodes.append(child)
            nodes = newNodes


