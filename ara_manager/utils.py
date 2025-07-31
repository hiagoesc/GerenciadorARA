from qgis.core import QgsProject

def obter_camada_por_nome(nome_camada):
    for layer in QgsProject.instance().mapLayers().values():
        if layer.name() == nome_camada:
            return layer
    return None

def buscar_requerente_por_cpf(cpf):
    layer = obter_camada_por_nome("requerentes")
    if not layer:
        return None

    for feat in layer.getFeatures():
        if feat["cpf_requerente"] == cpf:
            return feat["nome_requerente"]
    return None