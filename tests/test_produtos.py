import pytest

# Teste 1: Pegar lista com banco limpo [cite: 37]
def test_deve_retornar_lista_vazia_no_inicio(client):
    resposta = client.get("/produtos")
    assert resposta.status_code == 200
    assert resposta.json() == [] # Espera uma lista vazia no começo [cite: 37]

# Teste 2: Testar se o cadastro grava no banco [cite: 38]
def test_deve_cadastrar_produto_com_sucesso(client):
    dados = {"nome": "Teclado", "preco": 120.0, "estoque": 10, "ativo": True}
    resposta = client.post("/produtos", json=dados)
    
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] is not None
    assert corpo["nome"] == "Teclado"

# Teste 3: Cadastrar e ver se ele aparece na listagem geral [cite: 39]
def test_deve_aparecer_na_lista_depois_de_criar(client):
    dados = {"nome": "Caderno", "preco": 25.50, "estoque": 5, "ativo": True}
    client.post("/produtos", json=dados) # Cadastra [cite: 39]
    
    resposta_lista = client.get("/produtos") # Lista [cite: 39]
    assert resposta_lista.status_code == 200
    assert len(resposta_lista.json()) == 1 # Tem que ter 1 item lá dentro [cite: 39]

# Teste 4: Buscar um id que existe [cite: 40]
def test_deve_buscar_produto_por_id_correto(client, produto_existente):
    id_do_produto = produto_existente["id"] # Puxa o ID gerado na fixture [cite: 49]
    
    resposta = client.get(f"/produtos/{id_do_produto}")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == produto_existente["nome"]

# Teste 5: Buscar um id que não foi criado [cite: 41]
def test_deve_dar_404_ao_buscar_id_invalido(client):
    resposta = client.get("/produtos/9999") # ID absurdo para dar erro [cite: 41]
    assert resposta.status_code == 404

# Teste 6: Apagar um produto [cite: 42]
def test_deve_deletar_um_produto_existente(client, produto_existente):
    id_alvo = produto_existente["id"]
    resposta = client.delete(f"/produtos/{id_alvo}")
    assert resposta.status_code == 204 # Código de sem conteúdo [cite: 22, 42]

# Teste 7: Apagar e depois tentar achar ele para confirmar [cite: 43]
def test_deve_deletar_e_dar_404_no_get_depois(client, produto_existente):
    id_alvo = produto_existente["id"]
    
    # Deleta primeiro [cite: 43]
    resultado_delete = client.delete(f"/produtos/{id_alvo}")
    assert resultado_delete.status_code == 204
    
    # Tenta buscar em seguida [cite: 43]
    resultado_get = client.get(f"/produtos/{id_alvo}")
    assert resultado_get.status_code == 404 # Sumiu do banco! [cite: 43]

# Teste 8: Tentar apagar algo que não existe [cite: 44]
def test_deve_dar_404_ao_deletar_produto_inexistente(client):
    resposta = client.delete("/produtos/8888")
    assert resposta.status_code == 404

# Teste 9: Testando dados inválidos com parametrização [cite: 45]
@pytest.mark.parametrize(
    "corpo_errado",
    [
        {"nome": "", "preco": 50.0},        # Nome em branco fere min_length
        {"nome": "Mouse", "preco": 0},       # Preço zero não pode
        {"nome": "Mouse", "preco": -10.0},   # Preço negativo não pode
        {"preco": 30.0}                      # Sem o campo nome
    ]
)
def test_validacao_erros_payload(client, corpo_errado):
    resposta = client.post("/produtos", json=corpo_errado)
    assert resposta.status_code == 422 # Erro de validação do Pydantic [cite: 45]

# Teste 10: Validar o isolamento do banco (Dividido em duas funções separadas) [cite: 46]
def test_verificar_isolamento_banco_parte1(client):
    dados = {"nome": "Item Teste Isolado", "preco": 5.0}
    client.post("/produtos", json=dados)
    
    # Conferindo que salvou nesta execução [cite: 46]
    resposta = client.get("/produtos")
    assert len(resposta.json()) == 1

def test_verificar_isolamento_banco_parte2(client):
    # Como a fixture limpa o banco entre os testes, o "Item Teste Isolado" não pode estar aqui [cite: 46, 48]
    resposta = client.get("/produtos")
    assert len(resposta.json()) == 0 # Banco precisa iniciar zerado novamente [cite: 46]