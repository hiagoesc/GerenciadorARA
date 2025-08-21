from qgis.core import QgsProject, QgsExpression, QgsFeatureRequest

def obter_dados_processo(numero_processo: str) -> dict:
    """
    Retorna todos os dados de um processo a partir do número do processo.
    Busca nas camadas: processos_ara, dados_localizacao, dados_projeto,
    requerentes, processo_requerente, tecnicos e processo_tecnicos.
    """
    projeto = QgsProject.instance()

    # Camadas principais
    camada_proc = projeto.mapLayersByName("processos_ara")[0]
    camada_local = projeto.mapLayersByName("dados_localizacao")[0]
    camada_proj = projeto.mapLayersByName("dados_projeto")[0]
    camada_reqs = projeto.mapLayersByName("requerentes")[0]
    camada_assoc = projeto.mapLayersByName("processo_requerente")[0]
    camada_tec = projeto.mapLayersByName("tecnicos")[0]
    camada_resps = projeto.mapLayersByName("processo_tecnicos")[0]

    dados = {"numero_processo": numero_processo}

    # 🔹 Processo
    expr = QgsExpression(f""""numero_processo" = '{numero_processo}'""")
    feat_proc = next(camada_proc.getFeatures(QgsFeatureRequest(expr)), None)
    if feat_proc:
        dados["processo"] = feat_proc.attributes()

    # 🔹 Localização
    feat_local = next(camada_local.getFeatures(QgsFeatureRequest(expr)), None)
    if feat_local:
        dados["localizacao"] = feat_local.attributes()

    # 🔹 Projeto
    feat_proj = next(camada_proj.getFeatures(QgsFeatureRequest(expr)), None)
    if feat_proj:
        dados["projeto"] = feat_proj.attributes()

    # 🔹 Requerente (único)
    feat_assoc = next(camada_assoc.getFeatures(QgsFeatureRequest(expr)), None)
    if feat_assoc:
        cpf_cnpj = feat_assoc["cpf_cnpj_requerente"]
        expr_req = QgsExpression(f""""cpf_cnpj_requerente" = '{cpf_cnpj}'""")
        feat_req = next(camada_reqs.getFeatures(QgsFeatureRequest(expr_req)), None)
        if feat_req:
            dados["requerente"] = feat_req.attributes()

    # 🔹 Técnicos
    feat_resp = next(camada_resps.getFeatures(QgsFeatureRequest(expr)), None)
    if feat_resp:
        dados["tecnicos"] = {}
        if feat_resp["registro_projeto"]:
            expr_tec = QgsExpression(f""""registro" = '{feat_resp["registro_projeto"]}'""")
            tec_proj = next(camada_tec.getFeatures(QgsFeatureRequest(expr_tec)), None)
            if tec_proj:
                dados["tecnicos"]["projeto"] = tec_proj.attributes()

        if feat_resp["registro_execucao"]:
            expr_tec = QgsExpression(f""""registro" = '{feat_resp["registro_execucao"]}'""")
            tec_exec = next(camada_tec.getFeatures(QgsFeatureRequest(expr_tec)), None)
            if tec_exec:
                dados["tecnicos"]["execucao"] = tec_exec.attributes()

    return dados



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