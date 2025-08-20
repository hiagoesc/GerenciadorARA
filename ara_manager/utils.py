from qgis.core import QgsProject

def obter_camada_por_nome(nome_camada):
    for layer in QgsProject.instance().mapLayers().values():
        if layer.name() == nome_camada:
            return layer
    return None

def buscar_requerente_por_cpf_cnpj(cpf_cnpj):
    layer = obter_camada_por_nome("requerentes")
    if not layer:
        return None

    for feat in layer.getFeatures():
        if feat["cpf_cnpj_requerente"] == cpf_cnpj:
            return feat["nome_requerente"]
    return None

def buscar_tecnico_por_registro(registro):
    layer = obter_camada_por_nome("tecnicos")
    if not layer:
        return None

    for feat in layer.getFeatures():
        if feat["registro"] == registro:
            return {
                "nome": feat["nome"],
                "inscricao": feat["inscricao"],
                "email": feat["email"]
            }
    return None