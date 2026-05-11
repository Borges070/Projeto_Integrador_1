def safe_get(dictionary, *keys): #Basicamente uma função para acessar chaves aninhadas em um dicionário sem causar erros se alguma chave não existir.
    current = dictionary

    for key in keys:
        if not isinstance(current, dict):
            return None

        current = current.get(key)

        if current is None:
            return None

    return current


def transformar_deputado(dados): 
    redes = dados.get("redeSocial", []) # Obtém a lista de redes sociais do deputado. Se a chave "redeSocial" não existir, retorna uma lista vazia.

    if not isinstance(redes, list):
        redes = []

    return {
        "id": dados.get("id"),

        "nome_civil":
            dados.get("nomeCivil"),

        "nome_parlamentar":
            safe_get(dados, "ultimoStatus", "nome"),

        "partido":
            safe_get(
                dados,
                "ultimoStatus",
                "siglaPartido"
            ),

        "uf":
            safe_get(
                dados,
                "ultimoStatus",
                "siglaUf"
            ),

        "email":
            safe_get(
                dados,
                "ultimoStatus",
                "gabinete",
                "email"
            ),

        "telefone":
            safe_get(
                dados,
                "ultimoStatus",
                "gabinete",
                "telefone"
            ),

        "sexo":
            dados.get("sexo"),

        "data_nascimento":
            dados.get("dataNascimento"),

        "escolaridade":
            dados.get("escolaridade"),

        "website":
            dados.get("urlWebsite"),

        "redes_sociais":
            ", ".join(redes)
    }