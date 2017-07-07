import pkg_resources
from django.apps import AppConfig


class D3PrimeriConfig(AppConfig):
    name = 'd3_primeri'
    plugini_ucitavanje=[]
    plugini_vizualizatori=[]
    aktivan_viz=None
    aktivan_ucitavanje=None


    def stavi_aktivan_plugin_viz(self,id):
        for i in self.plugini_vizualizatori:
            if i.identifier() == id:
                self.aktivan_viz=i

    def stavi_aktivan_plugin_ucitavanje(self,id):
        for i in self.plugini_ucitavanje:
            if i.identifier() == id:
                self.aktivan_ucitavanje=i

    def ready(self):
        self.plugini_ucitavanje = load_plugins("kod.ucitati")
        self.plugini_vizualizatori = load_plugins("kod.vizualizator")


def load_plugins(oznaka):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=oznaka):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins
