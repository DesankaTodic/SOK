from d3_primeri.models import Attribute, Node, Link
from d3_primeri.services.vizualizator import VizualizatorService
from d3_primeri.views import zoom_pan
import  os
import json
import os


class TreeLayout(VizualizatorService):
    def naziv(self):
        return "Tree layout"

    def identifier(self):
        return "tree_layout"

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
            fill: #fff;
            stroke: steelblue;
            stroke-width: 3px;
        }

        .node text { font: 12px sans-serif; }

        .link {
            fill: none;
            stroke: #ccc;
            stroke-width: 2px;
        }

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

                ///birdview radi tako sto imam 2xnodes i 2xlinks, koje prosledjujem jednom d3 layout-u
                //sve je u funkciji update(source)

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
                           {%include "nodes_template.html" %}
                ]
                {% endif %}
             }
            {%if forloop.counter < nodes|length %}
            ,
            {% endif %}
        {% endfor %}
    ]
    }
    {%else%}//dodat lazni root za filter posto d3 tree layout zahtjeva pocetni cvor od koga iscrtava
    {%if nodes%}
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
    {% endif %}
    {% endif %}];

        // ************** Generate the tree diagram  *****************

        var i = 0,
        duration = 400;

        var tree = d3.layout.tree()
            .size([400, 400]);

        var diagonal = d3.svg.diagonal()
            .projection(function(d) { return [d.y, d.x]; });


        var svg = d3.select("#tree")
            .attr("width", 500)
            .attr("height", 500)
            """+zoom_pan()+"""
            .append("g")
            .attr("transform", "translate(0,0)");

         var svg2 = d3.select("#bird")
            .append("g")
            .attr("transform", "translate(0,0)");

        var diagonal = d3.svg.diagonal()
            .projection(function(d) { return [d.y, d.x]; });
        var diagonal2 = d3.svg.diagonal()
            .projection(function(d) { return [d.y, d.x]; });

        {

        root = treeData[0];
        root.x0 = 400 / 2;
        root.y0 = 200;

        function collapse(d) {
            if (d.children) {
                d._children = d.children;
                d._children.forEach(collapse);
                d.children = null;
            }
        }

        update(root);
        }

        d3.select(self.frameElement).style("height", "800px");

        function update(source) {

            // Compute the new tree layout.
            var nodes = tree.nodes(root).reverse(),
                         links = tree.links(nodes);

            // Normalize for fixed-depth.
            nodes.forEach(function(d) { d.y = d.depth * 90; });

            // Declare the nodesâ€¦
            var node = svg.selectAll("g.node")
                .data(nodes, function(d) { return d.id || (d.id = ++i); });

            // Enter the nodes.
            var nodeEnter = node.enter().append("g")
                .attr("class", "node")
                .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
                .on("click", click);

            nodeEnter.append("circle")
                .attr("r", 1e-6)
                .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

            nodeEnter.append("text")
                .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
                .attr("dy", ".35em")
                .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
                .text(function(d) { return d.naziv; })
                .style("fill-opacity", 1e-6)
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
                    update(d);
                });

            // Transition nodes to their new position.
            var nodeUpdate = node.transition()
                .duration(duration)
                .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

            nodeUpdate.select("circle")
                .attr("r", 4.5)
                .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

            nodeUpdate.select("text")
                .style("fill-opacity", 1);


            // Transition exiting nodes to the parent's new position.
            var nodeExit = node.exit().transition()
                .duration(duration)
                .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
                .remove();

            nodeExit.select("circle")
                .attr("r", 1e-6);

            nodeExit.select("text")
                .style("fill-opacity", 1e-6);

            // Declare the linksâ€¦
            var link = svg.selectAll("path.link")
                .data(links, function(d) { return d.target.id; });

            // Enter the links.
            link.enter().insert("path", "g")
                .attr("class", "link")
                .attr("d", function(d) {
                    var o = {x: source.x0, y: source.y0};
                    return diagonal({source: o, target: o});
                });

            // Transition links to their new position.
            link.transition()
                .duration(duration)
                .attr("d", diagonal);

            // Transition exiting nodes to the parent's new position.
            link.exit().transition()
                .duration(duration)
                .attr("d", function(d) {
                    var o = {x: source.x, y: source.y};
                    return diagonal({source: o, target: o});
                })
                .remove();

            // Stash the old positions for transition.
            nodes.forEach(function(d) {
                d.x0 = d.x;
                d.y0 = d.y;
            });
            // Compute the tree layout for birdview.
            var nodes2 = tree.nodes(root).reverse(),
                         links2 = tree.links(nodes2);

            // Normalize for fixed-depth.
            nodes2.forEach(function(d) { d.y = d.depth * 90; });

            // Declare the nodesâ€¦
            var node2 = svg2.selectAll("g.node")
                .data(nodes2, function(d) { return d.id || (d.id = ++i); });

            // Enter the nodes.
            var nodeEnter2 = node2.enter().append("g")
                .attr("class", "node")
                .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; });

            nodeEnter2.append("circle")
                .attr("r", 1e-6)
                .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

            nodeEnter2.append("text")
                .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
                .attr("dy", ".35em")
                .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
                .text(function(d) { return d.naziv; })
                .style("fill-opacity", 1e-6)
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
                    update(d);
                });


            // Transition nodes to their new position.
            var nodeUpdate2 = node2.transition()
                .duration(duration)
                .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

            nodeUpdate2.select("circle")
                .attr("r", 4.5)
                .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

            nodeUpdate2.select("text")
                .style("fill-opacity", 1);

            // Transition exiting nodes to the parent's new position.
            var nodeExit2 = node2.exit().transition()
                .duration(duration)
                .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
                .remove();

            nodeExit2.select("circle")
                .attr("r", 1e-6);

            nodeExit2.select("text")
                .style("fill-opacity", 1e-6);

            // Declare the linksâ€¦
            var link2 = svg2.selectAll("path.link")
                .data(links2, function(d) { return d.target.id; });

            // Enter the links.
            link2.enter().insert("path", "g")
                .attr("class", "link")
                .attr("d", function(d) {
                    var o = {x: source.x0, y: source.y0};
                    return diagonal2({source: o, target: o});
                });

            // Transition links to their new position.
            link2.transition()
                .duration(duration)
                .attr("d", diagonal2);

            // Transition exiting nodes to the parent's new position.
            link2.exit().transition()
                .duration(duration)
                .attr("d", function(d) {
                    var o = {x: source.x, y: source.y};
                    return diagonal2({source: o, target: o});
                })
                .remove();

            // Stash the old positions for transition.
            nodes2.forEach(function(d) {
                d.x0 = d.x;
                d.y0 = d.y;
            });
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

        function click(d) {
            if (d.children) {
                d._children = d.children;
                d.children = null;
            } else {
                d.children = d._children;
                d._children = null;
            }
            update(d);
            nodeClick(d);
        }


        </script>
        {% endblock %}
                """
        return message

    def getHTMLLinks(self):
        return """ """

    def getHTMLNodes(self):
        nodes = """
         {% for n2,values2 in values.items %}
        {name:"node_{{n2.id}}",
           tekst:"{{n2.text}}",
         naziv:"{{n2}}",
            atributi:[
                {% for a in n2.attributes.all %}
                {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                {% endfor %}
                ],
         {% if values2 %}
          children:[
                {%with values=values2 template_name="tree_layout_template.html" %}
                    {%include template_name%}
                {%endwith%}
            ]
            {% endif %}
            }
            {%if forloop.counter < values|length %}
            ,
            {% endif %}
            {% endfor %}
        """

        return nodes
