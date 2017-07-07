from d3_primeri.models import Attribute, Node, Link
from d3_primeri.services.ucitati import UcitatiService
import json
from pprint import pprint
import os
import uuid


class UcitatiJSONIzvor(UcitatiService):
    def naziv(self):
        return "Ucitati json izvor"
    def identifier(self):
        return "ucitati_json_izvor"

    def ucitati(self, path):
        self.parseJSON(path)

    def recursive(self,values,parent):
        for list_values in values:#rjecnik ima listu rjecnika

            child = Node(code=uuid.uuid4(), label="childNode")
            child.save()
            label = parent.label + "->" + child.label
            link = Link(label=label)
            link.parent_node = parent
            link.child_node = child
            link.save()

            #print("list_values ",list_values)
            for key,values in list_values.items():

                #print("key2 ",key)
                if isinstance(values, list):
                    child2 = Node(code=uuid.uuid4(), label=key)
                    child2.save()
                    label = child.label + "->" + child2.label
                    link = Link(label=label)
                    link.parent_node = child
                    link.child_node = child2
                    link.save()

                    self.recursive(values,child2)
                else:
                    #child = Node(code=uuid.uuid4(), label=key)
                    #child.save()
                    a = Attribute(name=key, value=values)
                    a.save()
                    child.attributes.add(a)
                    child.save()

    def parseJSON(self, path):
        print("parseJSON")
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
        json_file = open(full_file_path)
        json_str = json_file.read()
        json_data = json.loads(json_str)
        parent = Node(code=uuid.uuid4(), label="root")
        parent.save()
        for key,values in json_data.items():

            if isinstance(values, list):
                child = Node(code=uuid.uuid4(), label=key)
                child.save()
                label = parent.label + "->" + child.label
                link = Link(label=label)
                link.parent_node = parent
                link.child_node = child
                link.save()

                self.recursive(values,child)
            elif isinstance(values, dict):

                jsonObjekat = Node(code=uuid.uuid4(), label=key)
                jsonObjekat.save()

                label = parent.label + "->" + jsonObjekat.label
                link = Link(label=label)
                link.parent_node = parent
                link.child_node = jsonObjekat
                link.save()

                for key, values in values.items():
                    print(key)
                    print(values)

                    a = Attribute(name=key, value=values)
                    a.save()
                    jsonObjekat.attributes.add(a)
                    jsonObjekat.save()
            else:
                a = Attribute(name=key, value=values)
                a.save()
                parent.attributes.add(a)
                parent.save()
        pprint(json_data)
