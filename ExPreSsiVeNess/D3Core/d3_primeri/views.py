from django.apps.registry import apps
from django.shortcuts import render, redirect
from d3_primeri.models import Attribute, Node, Link
import os

def index(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    plugini_viz = apps.get_app_config('d3_primeri').plugini_vizualizatori
    nodes=Node.objects.all()
    return render(request,"index.html",{"title":"Index","plugini_ucitavanje":plugini,"plugini_vizualizatori":plugini_viz,"node_data":nodes,"nodes_id":[]})

def ucitavanje_plugin(request,id):
    request.session['izabran_plugin_ucitavanje']=id
    plugini=apps.get_app_config('d3_primeri').plugini_ucitavanje
    Node.objects.all().delete()
    Attribute.objects.all().delete()
    Link.objects.all().delete()
    putanja_izvora=""
    if request.method == 'POST':
        print(request.POST)
        putanja_izvora = request.POST['putanja_izvora']
    apps.get_app_config('d3_primeri').stavi_aktivan_plugin_ucitavanje(id)
    plugin = apps.get_app_config('d3_primeri').aktivan_ucitavanje
    plugin.ucitati(putanja_izvora)
    print("ucitavanje_plugin(request,id,path) ", putanja_izvora)
    return redirect('index')

def viz_plugin(request,id):
    request.session['izabran_plugin_viz']=id
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    plugini_viz = apps.get_app_config('d3_primeri').plugini_vizualizatori
    all_nodes = Node.objects.all()
    root=all_nodes[0]#root je prvi node u bazi
    tree={}
    abspath = os.path.abspath("")
    root_path = abspath[:-14]
    content_path = root_path + "D3Core\\d3_primeri\\templates\\content.html"
    links_path=root_path + "D3Core\\d3_primeri\\templates\\links_template.html"
    nodes_path=root_path + "D3Core\\d3_primeri\\templates\\nodes_template.html"

    file_content = open(content_path, 'w')
    file_nodes = open(nodes_path, 'w')
    file_links = open(links_path, 'w')

    apps.get_app_config('d3_primeri').stavi_aktivan_plugin_viz(id)
    plugin = apps.get_app_config('d3_primeri').aktivan_viz
    tree=plugin.getTree()
    nodesHTML=plugin.getHTMLNodes()
    linksHTML=plugin.getHTMLLinks()
    contentHTML=plugin.getHTMLContent([])

    file_nodes.write(nodesHTML)
    file_nodes.close()
    file_links.write(linksHTML)
    file_links.close()
    file_content.write(contentHTML)
    file_content.close()

    return render(request, "content.html",
                  {"title": "Vizualizator", "plugini_ucitavanje": plugini,"plugini_vizualizatori":plugini_viz, "tree": tree, "root": root,
                   "nodes": tree[root],"node_data":all_nodes,"nodes_id":[]})


def create_dict_nodes(nodes):
    tree_child={}
    for node in nodes:
        children_links = Link.objects.filter(parent_node=node)
        children = []
        for child_link in children_links:
            children.append(child_link.child_node)
            print(child_link.child_node)
        tree_child[node]=create_dict_nodes(children)
    return tree_child


def refreshTree(search_text):
    nodes_id=[]
    if search_text != '':
        result_nodes = Node.objects.filter(label__contains=search_text)
        for node in result_nodes:
            nodes_id.append(node.id)
    return nodes_id

def getFilteredNodes(text):
    result_nodes=[]
    if text != '':
        result_nodes = Node.objects.filter(label__contains=text)
    else:
        result_nodes=Node.objects.all()
    return result_nodes


def search(request):
    id = request.session['izabran_plugin_viz']
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    plugini_viz = apps.get_app_config('d3_primeri').plugini_vizualizatori
    all_nodes = Node.objects.all()
    root = all_nodes[0]  # root je prvi node u bazi
    tree = {}
    abspath = os.path.abspath("")
    root_path = abspath[:-14]
    content_path = root_path + "D3Core\\d3_primeri\\templates\\content.html"
    links_path = root_path + "D3Core\\d3_primeri\\templates\\links_template.html"
    nodes_path = root_path + "D3Core\\d3_primeri\\templates\\nodes_template.html"

    file_content = open(content_path, 'w')
    file_nodes = open(nodes_path, 'w')
    file_links = open(links_path, 'w')

    nodes_id=[]
    if request.method == 'POST':
        search_text = request.POST['search_text']
        print(search_text)
        nodes_id=refreshTree(search_text)
        print(nodes_id)
        searchedNodes=getFilteredNodes(search_text)
        apps.get_app_config('d3_primeri').stavi_aktivan_plugin_viz(id)
        plugin = apps.get_app_config('d3_primeri').aktivan_viz
        tree = plugin.getTree()
        nodesHTML = plugin.getHTMLNodes()
        linksHTML = plugin.getHTMLLinks()
        contentHTML = plugin.getHTMLContent(searchedNodes)

        file_nodes.write(nodesHTML)
        file_nodes.close()
        file_links.write(linksHTML)
        file_links.close()
        file_content.write(contentHTML)
        file_content.close()

    return render(request, "content.html",
                  {"title": "Pretraga", "plugini_ucitavanje": plugini, "plugini_vizualizatori": plugini_viz,
                   "tree": tree, "root": root,
                   "nodes": tree[root], "node_data": all_nodes,"nodes_id":nodes_id, "tekst":search_text})

def filter(request):
    id=request.session['izabran_plugin_viz']
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    plugini_viz = apps.get_app_config('d3_primeri').plugini_vizualizatori
    all_nodes = Node.objects.all()
    root=all_nodes[0]#root je prvi node u bazi
    tree={}
    abspath = os.path.abspath("")
    root_path = abspath[:-14]
    content_path = root_path + "D3Core\\d3_primeri\\templates\\content.html"
    links_path=root_path + "D3Core\\d3_primeri\\templates\\links_template.html"
    nodes_path=root_path + "D3Core\\d3_primeri\\templates\\nodes_template.html"

    file_content = open(content_path, 'w')
    file_nodes = open(nodes_path, 'w')
    file_links = open(links_path, 'w')

    filter_text=""
    nodes_id=[]
    if request.method == 'POST':
        filter_text = request.POST['filter_text']
        print(filter_text)
        nodes_id=refreshTree(filter_text)
        print(nodes_id)
        filteredNodes= getFilteredNodes(filter_text)
        apps.get_app_config('d3_primeri').stavi_aktivan_plugin_viz(id)
        plugin = apps.get_app_config('d3_primeri').aktivan_viz
        tree = plugin.getTree()
        nodesHTML = plugin.getHTMLNodes()
        linksHTML = plugin.getHTMLLinks()
        contentHTML = plugin.getHTMLContent(filteredNodes)

        file_nodes.write(nodesHTML)
        file_nodes.close()
        file_links.write(linksHTML)
        file_links.close()
        file_content.write(contentHTML)
        file_content.close()

    return render(request, "content.html",
                  {"title": "Filter", "plugini_ucitavanje": plugini, "plugini_vizualizatori": plugini_viz,
                   "tree": None, "root": None,
                   "nodes": filteredNodes, "node_data": filteredNodes,"nodes_id":[]})


def zoom_pan():
    return ".call(d3.behavior.zoom().on(\"zoom\", function () { svg.attr(\"transform\", \"translate(\" + d3.event.translate + \")\" + \"scale(\" + d3.event.scale + \")\")}))"