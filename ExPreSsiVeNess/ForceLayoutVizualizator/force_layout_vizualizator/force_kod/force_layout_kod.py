from d3_primeri.models import Attribute, Node, Link
from d3_primeri.services.vizualizator import VizualizatorService
from d3_primeri.views import zoom_pan
import json
import os

class ForceLayout(VizualizatorService):
    def naziv(self):
        return "Force layout"
    def identifier(self):
        return "force_layout"

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

    def create_dict_nodes(self,nodes):
        tree_child = {}
        for node in nodes:
            children_links = Link.objects.filter(parent_node=node)
            children = []
            for child_link in children_links:
                children.append(child_link.child_node)
                print(child_link.child_node)
            tree_child[node] = self.create_dict_nodes(children)
        return tree_child

    def convertListOfSearchedNodesToString(self,result_nodes):
        search_nodes = []
        if result_nodes:
            for node in result_nodes:
                search_nodes.append('node_' + str(node.id))
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

    def getHTMLContent(self,result_nodes):
        #result_nodes = rezultati search-a
        print("force_layout")
        search = self.convertListOfSearchedNodesToString(result_nodes)
        print ("search " + search)

        message = """
       {% extends "base.html" %}
        {% block head_sadrzaj %}
        <style>
           .node2 {
           cursor: pointer;
            color: #3182bd;
            }

        .link2 {
          fill: none;
          stroke: #9ecae1;
          stroke-width: 1.5px;
        }

        .line2 {
          fill: green;
          stroke: black;
          stroke-width: 1.5px;
          opacity:0.5;

        }
        .node {
          cursor: pointer;
          color: #3182bd;

        }

        .link {
          fill: none;
          stroke: #9ecae1;
          stroke-width: 1.5px;
        }

        .line1 {
          fill: green;
          stroke: black;
          stroke-width: 1.5px;
          opacity:0.5;

        }
        </style>

        {% endblock %}
        {% block content %}
        <div id="birdview" class="center">
                    <svg id="bird" width="500" height="500">

                    </svg>
                </div>
        <div class="center">
            <svg id="force" width="500" height="500">

            </svg>
        </div>

        <script>
            var search_nodes="""+search+"""
            var nodes={
            {%if nodes.items%}
            "node_{{root.id}}":{name:"node_{{root.id}}",naziv:"{{root.label}}",text:"{{root.text}}",
            kategorije:[
                {% for a in root.attributes.all %}
                       {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                    {% endfor %}
            ]},
            {% for n,values in nodes.items %}
               "node_{{n.id}}":{name:"node_{{n.id}}",naziv:"{{n.label}}",text:"{{n.text}}",

                   kategorije:[
                    {% for a in n.attributes.all %}
                       {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                    {% endfor %}
                    ]
                },
               {%include "nodes_template.html" %}

            {% endfor %}
            {%else%}//poredjenje za filter ako dobije listu(a ne stablo) znaci da treba filtrirati
                {% for n in nodes %}
               "node_{{n.id}}":{name:"node_{{n.id}}",naziv:"{{n.label}}",text:"{{n.text}}",

                   kategorije:[
                    {% for a in n.attributes.all %}
                       {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                    {% endfor %}
                    ]
                },


            {% endfor %}
             {% endif %}

        {%if nodes.items%}
            "node_{{root.id}}":{name:"node_{{root.id}}",naziv:"{{root.label}}",text:"{{root.text}}",
            kategorije:[
                {% for a in root.attributes.all %}
                       {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                    {% endfor %}
            ]},
            {% for n,values in nodes.items %}
               "node_{{n.id}}":{name:"node_{{n.id}}",naziv:"{{n.label}}",text:"{{n.text}}",

                   kategorije:[
                    {% for a in n.attributes.all %}
                       {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                    {% endfor %}
                    ]
                },
               {%include "nodes_template.html" %}
            {% endfor %}
            {%else%}
                {% for n in nodes %}
               "node_{{n.id}}":{name:"node_{{n.id}}",naziv:"{{n.label}}",text:"{{n.text}}",

                   kategorije:[
                    {% for a in n.attributes.all %}
                       {name:"attribute_{{a.id}}",naziv:"{{a.name}}",vrednost:"{{a.value}}" },
                    {% endfor %}
                    ]
                },

            {% endfor %}
             {% endif %}


            };

            var links=[
                {% for n,values in nodes.items %}
                      {source:"node_{{root.id}}",target:"node_{{n.id}}"},
                       {%include "links_template.html" %}
                {% endfor %}
                {% for n,values in nodes.items %}
                              {source:"node_{{root.id}}",target:"node_{{n.id}}"},
                              {%include "links_template.html" %}
                        {% endfor %}
            ];

             links.forEach(function(link) {
                link.source = nodes[link.source];
                link.target = nodes[link.target];
            });

            var force = d3.layout.force() //kreiranje force layout-a
                .size([500, 500]) //raspoloziv prostor za iscrtavanje
                .nodes(d3.values(nodes)) //dodaj nodove
                .links(links) //dodaj linkove
                .on("tick", tick) //sta treba da se desi kada su izracunate nove pozicija elemenata
                .linkDistance(300) //razmak izmedju elemenata
                .charge(-100)//koliko da se elementi odbijaju
                .start(); //pokreni izracunavanje pozicija


            var ln1 = [];
            var ln2 = [];
            var i;
            for(i=0;i<links.length/2;i++){
                ln1.push(links[i]);
            }
            for(i;i<links.length;i++){
                ln2.push(links[i]);
            }
            var svg=d3.select('#force')
            """+zoom_pan()+"""
            .append("g")
            .attr("transform", "translate(0,0)");


            // add the links
            var link = svg.selectAll('.link')
                .data(ln1)
                .enter().append('line')
                .attr('class', 'link');

                var svg2=d3.select('#bird');
            // add the links
            var link2 = svg2.selectAll('.link2')
                .data(ln2)
                .enter().append('line')
                .attr('class', 'link2');

            function nodeClick(el){
                if(el.attributes.tekst.value==""){
                   alert("ID: "+el.id);
                   }else{
                   alert("ID: "+el.id+" text: "+el.attributes.tekst.value);
                   }
                }
            // add the nodes
            var node = svg.selectAll('.node')
                .data(force.nodes()) //add
                .enter().append('g')
                .attr('class', 'node')
                .attr('id', function(d){return d.name;})
                .attr('tekst', function(d){return d.text;})
                .on('click',function(){
                   nodeClick(this);
                });

         var node2 = svg2.selectAll('.node2')
                .data(force.nodes()) //add
                .enter().append('g')
                .attr('class', 'node2')
                .attr('id', function(d){return d.name+"2";})//da bi id bio jedinstven dodato je +2
                .attr('tekst', function(d){return d.text;});

            d3.selectAll('.node').each(function(d){slozenPrikaz(d);});
            d3.selectAll('.node2').each(function(d){slozenPrikaz2(d);});

            function slozenPrikaz(d){
              var duzina=100;
              var brKategorija=d.kategorije.length;

              var textSize=10;
              var visina=(brKategorija==0)?textSize:brKategorija*textSize;
              visina+=textSize;

              //Ubacivanje pravougaonika
              d3.select("g#"+d.name).append('rect').
              attr('x',0).attr('y',0).attr('width',duzina).attr('height',visina)
              .attr('fill','yellow');
              //Ubacivanje naziva cvora
              d3.select("g#"+d.name).append('text').attr('x',duzina/2).attr('y',10)
              .attr('text-anchor','middle')
              .attr('font-size',textSize).attr('font-family','sans-serif')
              .attr('fill','green').text(d.naziv);


              //Ubacivanje razdelnika
              d3.select("g#"+d.name).append('line').
              attr('x1',0).attr('y1',textSize).attr('x2',duzina).attr('y2',textSize)
              .attr('stroke','gray').attr('stroke-width',2);

              //Ubacivanje teksta za atribute
                for(var i=0;i<brKategorija;i++)
                {
                   //Ubacivanje naziva atributa=vrednost
                  d3.select("g#"+d.name).append('text').attr('x',0).attr('y',20+i*textSize)
                  .attr('text-anchor','start')
                  .attr('font-size',textSize).attr('font-family','sans-serif')
                  .attr('fill','green').text(d.kategorije[i].naziv+" = "+d.kategorije[i].vrednost);

                }

            }
        function slozenPrikaz2(d){
              var duzina=100;
              var brKategorija=d.kategorije.length;

              var textSize=10;
              var visina=(brKategorija==0)?textSize:brKategorija*textSize;
              visina+=textSize;

              //Ubacivanje pravougaonika
              d3.select("g#"+d.name+"2").append('rect').
              attr('x',0).attr('y',0).attr('width',duzina).attr('height',visina)
              .attr('fill','yellow');
              //Ubacivanje naziva cvora
              d3.select("g#"+d.name+"2").append('text').attr('x',duzina/2).attr('y',10)
              .attr('text-anchor','middle')
              .attr('font-size',textSize).attr('font-family','sans-serif')
              .attr('fill','green').text(d.naziv);


              //Ubacivanje razdelnika
              d3.select("g#"+d.name+"2").append('line').
              attr('x1',0).attr('y1',textSize).attr('x2',duzina).attr('y2',textSize)
              .attr('stroke','gray').attr('stroke-width',2);

              //Ubacivanje teksta za atribute
                for(var i=0;i<brKategorija;i++)
                {
                   //Ubacivanje naziva atributa=vrednost
                  d3.select("g#"+d.name+"2").append('text').attr('x',0).attr('y',20+i*textSize)
                  .attr('text-anchor','start')
                  .attr('font-size',textSize).attr('font-family','sans-serif')
                  .attr('fill','green').text(d.kategorije[i].naziv+" = "+d.kategorije[i].vrednost);

                }

            }
            d3.selectAll('.node').each(function(d){search(d);});
                function search(d){
                    for(var i=0;i<search_nodes.length;i++)
                    {
                        if(d.name==search_nodes[i]){
                          var duzina=100+2;
                          var brKategorija=d.kategorije.length;
                          var textSize=10;
                          var visina=(brKategorija==0)?textSize:brKategorija*textSize+2
                          visina+=textSize;

                            d3.select('g#'+d.name).append("rect")
                                              .style("stroke", "red")
                                               .style("stroke-width", 2)
                                              .style("fill", "none")
                                             .attr("x", 0)
                                            .attr("y", 0)
                                           .attr("width", duzina)
                                          .attr("height", visina);
                            d3.select('g#'+d.name+"2").append("rect")
                                              .style("stroke", "red")
                                               .style("stroke-width", 2)
                                              .style("fill", "none")
                                             .attr("x", 0)
                                            .attr("y", 0)
                                           .attr("width", duzina)
                                          .attr("height", visina);
                            }
                        }
                   }
            function tick(e) {

                node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
                    .call(force.drag);
                node2.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
                    .call(force.drag);

                link.attr('x1', function(d) { return d.source.x; })
                    .attr('y1', function(d) { return d.source.y; })
                    .attr('x2', function(d) { return d.target.x; })
                    .attr('y2', function(d) { return d.target.y; })
                link2.attr('x1', function(d) { return d.source.x; })
                    .attr('y1', function(d) { return d.source.y; })
                    .attr('x2', function(d) { return d.target.x; })
                    .attr('y2', function(d) { return d.target.y; });

            }


        </script>
        {% endblock %}
                """
        return message

    def getHTMLLinks(self):
        links="""
        {%for n2,values2 in values.items %}
          {source:"node_{{n.id}}",target:"node_{{n2.id}}"},
          {%with values=values2 n=n2 template_name="links_template.html" %}
               {%include template_name%}
          {%endwith%}
        {%endfor%}
        """
        return links

    def getHTMLNodes(self):
        nodes="""
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

    def getHTMLContentBirdView(self, result_nodes):
       pass

    def getHTMLLinksBirdView(self):
       pass

    def getHTMLNodesBirdView(self):
        pass








