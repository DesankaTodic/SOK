from d3_primeri.models import Attribute, Node, Link
from d3_primeri.services.vizualizator import VizualizatorService
from d3_primeri.views import zoom_pan
import  os
import json
import os


class CollapsLayout(VizualizatorService):
    def naziv(self):
        return "Collapsible force layout"

    def identifier(self):
        return "collaps_layout"

    def getTree(self):
        root = Node.objects.all()
        print("root ", root[0])
        tree = {}
        children_links = Link.objects.filter(parent_node=root[0])
        children = []
        for child_link in children_links:
            children.append(child_link.child_node)
            print(child_link.child_node)
        tree[root[0]] = self.create_dict_nodes(children)
        return tree

    def create_dict_nodes(self, nodes):
        tree_child = {}
        for node in nodes:
            children_links = Link.objects.filter(parent_node=node)
            children = []
            for child_link in children_links:
                children.append(child_link.child_node)
                print(child_link.child_node)
            tree_child[node] = self.create_dict_nodes(children)
        return tree_child

    def convertListOfSearchedNodesToString(self, result_nodes):
        search_nodes = []
        if result_nodes:
            for node in result_nodes:
                search_nodes.append(node.label)
        search = ""
        if search_nodes:
            search = "['"
            for id in search_nodes:
                search = search + id + "','"
            search = search[0:len(search) - 3]
            search += "'];"
        else:
            search = "[];"
        return search


    def getHTMLContent(self, result_nodes):
        # result_nodes = rezultati search-a
        print("tree_layout")
        search = self.convertListOfSearchedNodesToString(result_nodes)
        print("search " + search)

        message = """
        {% extends "base.html" %}
        {% block head_sadrzaj %}
        <style>

        .node circle {
          cursor: pointer;
          stroke: #3182bd;
          stroke-width: 1.5px;
        }

        .node text {
          font: 10px sans-serif;
          pointer-events: none;
          text-anchor: middle;
        }

        .node2 circle {
          cursor: pointer;
          stroke: #3182bd;
          stroke-width: 1.5px;
        }

        .node2 text {
          font: 10px sans-serif;
          pointer-events: none;
          text-anchor: middle;
        }

        line.link {
          fill: none;
          stroke: #9ecae1;
          stroke-width: 1.5px;
        }

        line.link2 {
          fill: none;
          stroke: #9ecae1;
          stroke-width: 1.5px;
        }

        </style>

        {% endblock %}
        {% block content %}
        <div class="center">
            <svg id="bird" width="500" height="500"></svg>
        </div>
        <div class="center">
            <svg id="tree" width="500" height="500"></svg>
        </div>


        <script>

         var search_nodes="""+search+"""

         var treeData=[
           {%if nodes.items%}
                {name:"node_{{root.id}}",
                naziv:"{{root}}",
               tekst:"{{root.text}}",
               atributi:[
                    {% for a in root.attributes.all %}
                            {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                            {% endfor %}
                    ],
                children:[
                {% for n,values in nodes.items %}
                   {name:"node_{{n.id}}",
                    tekst:"{{n.text}}",
                    atributi:[
                    {% for a in n.attributes.all %}
                            {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                            {% endfor %}
                    ],
                    naziv:"{{n}}",
                    {% if values %}
                        children:[
                               {%include "collaps_layout_template.html" %}
                    ]
                    {% endif %}
                 }
                {%if forloop.counter < nodes|length %}
                ,
                {% endif %}
            {% endfor %}
        ]
        }
        {%else%}
            {name:"lazni",
                naziv:"lazni",
               tekst:"",
               atributi:[],
                children:[
                {% for n in nodes %}
                   {name:"node_{{n.id}}",
                    tekst:"{{n.text}}",
                    atributi:[
                    {% for a in n.attributes.all %}
                            {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                            {% endfor %}
                    ],
                    naziv:"{{n}}",
                    children:[]

                 }
                {%if forloop.counter < nodes|length %}
                ,
                {% endif %}
            {% endfor %}
        ]
        }
        {% endif %}];


        var force = d3.layout.force()
            .linkDistance(20)
            .charge(-120)
            .gravity(.05)
            .size([300, 300])
            .on("tick", tick);

        var svg = d3.select("#tree")
             .attr("width", 500)
            .attr("height", 500)
            """+zoom_pan()+"""
            .append("g");

        var svg2 = d3.select("#bird")
            .append("g")
            .attr("transform", "translate(0,0)");

        var link = svg.selectAll(".link"),
            node = svg.selectAll(".node");

        var link2 = svg2.selectAll(".link"),
            node2 = svg2.selectAll(".node");




        root = treeData[0];
        treeData[0].x = 250;
        treeData[0].y = 250;
        treeData[0].fixed = true;
        update();


        function update() {
              var nodes = flatten(root),
                  links = d3.layout.tree().links(nodes);

              // Restart the force layout.
              force
                  .nodes(nodes)
                  .links(links)
                  .start();

              // Update links.
              link = link.data(links, function(d) { return d.target.id; });

              link.exit().remove();

              link.enter().insert("line", ".node")
                  .attr("class", "link");

              // Update nodes.
              node = node.data(nodes, function(d) { return d.id; });

              node.exit().remove();

              var nodeEnter = node.enter().append("g")
                  .attr("class", "node")
                  .on("click", click)
                  .call(force.drag);

              nodeEnter.append("circle")
                  .attr("r", function(d) { return Math.sqrt(d.size) / 10 || 4.5; });

              nodeEnter.append("text")
                  .attr("dy", ".35em")
                  .text(function(d) { return d.naziv; })
                  .attr("fill", function(d){
                        if(!search_nodes){
                            return "black";
                        } else {
                            for(var i=0;i<search_nodes.length;i++){
                                if(d.naziv === search_nodes[i]) {
                                    return "red";
                                }
                            }

                        }
                        update();
                  });

              node.select("circle")
                  .style("fill", color);







            //za birdview
            // Update links.
              link2 = link2.data(links, function(d) { return d.target.id; });

              link2.exit().remove();

              link2.enter().insert("line", ".node")
                  .attr("class", "link");

              // Update nodes.
              node2 = node2.data(nodes, function(d) { return d.id; });

              node2.exit().remove();

              var nodeEnter2 = node2.enter().append("g")
                  .attr("class", "node2")
                  .call(force.drag);

              nodeEnter2.append("circle")
                  .attr("r", function(d) { return Math.sqrt(d.size) / 10 || 4.5; });

              nodeEnter2.append("text")
                  .attr("dy", ".35em")
                  .text(function(d) { return d.naziv; })
                  .attr("fill", function(d){
                        if(!search_nodes){
                            return "black";
                        } else {
                            for(var i=0;i<search_nodes.length;i++){
                                if(d.naziv === search_nodes[i]) {
                                    return "red";
                                }
                            }

                        }
                        update();
                  });

              node2.select("circle")
                  .style("fill", color);
        }

            function tick() {


              link.attr("x1", function(d) { return d.source.x; })
                  .attr("y1", function(d) { return d.source.y; })
                  .attr("x2", function(d) { return d.target.x; })
                  .attr("y2", function(d) { return d.target.y; });

              node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });


              node2.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
                       .call(force.drag);

               link2.attr('x1', function(d) { return d.source.x; })
                   .attr('y1', function(d) { return d.source.y; })
                   .attr('x2', function(d) { return d.target.x; })
                   .attr('y2', function(d) { return d.target.y; });
            }

            function color(d) {
              return d._children ? "#3182bd" // collapsed package
                  : d.children ? "#c6dbef" // expanded package
                  : "#fd8d3c"; // leaf node
            }

            function createStringOfAttributes(atributi){
                message = "atributi: {";
                    for(var i=0;i<atributi.length;i++){
                          message+=  atributi[i].naziv+" : "+atributi[i].vrednost+",";
                     }
                     message=message.substring(0, message.length-1);
                     message+="}";
                return message;
            }

            function nodeClick(el) {
                if (el.tekst == "") {
                        if (el.atributi.length == 0) {
                            alert("ID: " + el.name);
                        } else {
                            message = createStringOfAttributes(el.atributi);
                            alert("ID: " + el.name+", "+message)
                        }
                } else {
                    if (el.atributi.length == 0) {
                            alert("ID: " + el.name+", text: "+el.tekst);
                        } else {
                            message = createStringOfAttributes(el.atributi);
                            alert("ID: " + el.name+", text: "+el.tekst+", "+message);
                        }
                }
            }

            // Toggle children on click.
            function click(d) {
              if (d3.event.defaultPrevented) return; // ignore drag
              if (d.children) {
                d._children = d.children;
                d.children = null;
              } else {
                d.children = d._children;
                d._children = null;
              }
              update();
              nodeClick(d);
            }


            // Returns a list of all nodes under the root.
            function flatten(root) {
              var nodes = [], i = 0;

              function recurse(node) {
                if (node.children) node.children.forEach(recurse);
                if (!node.id) node.id = ++i;
                nodes.push(node);
              }

              recurse(root);
              return nodes;
            }

        </script>

        {% endblock %}
                """
        return message

    def getHTMLLinks(self):
        links = """
        {%for n2,values2 in values.items %}
          {source:"node_{{n.id}}",target:"node_{{n2.id}}"},
          {%with values=values2 n=n2 template_name="links_template.html" %}
               {%include template_name%}
          {%endwith%}
        {%endfor%}
        """
        return links

    def getHTMLNodes(self):
        nodes = """
         {% if values %}
        {%for n,values2 in values.items %}
                "node_{{n.id}}":{name:"node_{{n.id}}",naziv:"{{n.label}}",text:"{{n.text}}",

               kategorije:[
                {% for a in n.attributes.all %}
                   {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                {% endfor %}
                ]
                },
              {%with values=values2 template_name="nodes_template.html" %}
                   {%include template_name%}
              {%endwith%}
         {%endfor%}
        {% endif %}
        """

        return nodes
