from .plugin import MujPlugin


# vytvoření pluginu a předání iface
def classFactory(iface):
    return MujPlugin(iface)
