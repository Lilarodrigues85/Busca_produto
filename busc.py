import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configurações do Selenium
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Função para buscar produtos no Mercado Livre com base na entrada do usuário e rolamento da página
def buscar_produtos(tipo_produto):
    # Acesse a página principal do Mercado Livre
    driver.get("https://www.mercadolivre.com.br/")

    # Encontrar a caixa de pesquisa e digitar o termo fornecido
    search_box = driver.find_element(By.NAME, "as_word")
    search_box.send_keys(tipo_produto)
    search_box.send_keys(Keys.RETURN)

    # Esperar até que os resultados carreguem completamente
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-search-results"))
        )
    except Exception as e:
        print("Erro ao carregar resultados:", e)
        return

    # Rolagem da página para carregar mais produtos
    for _ in range(3):  # Rola a página 3 vezes
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Aguardar mais tempo para garantir o carregamento completo dos resultados

    # Listar os produtos encontrados
    produtos = []
    try:
        # Aguardar até que a lista de resultados esteja disponível
        items = driver.find_elements(By.CSS_SELECTOR, ".ui-search-result")

        if not items:
            print("Nenhum produto encontrado.")
            return

        print(f"Total de {len(items)} itens encontrados.")

        for item in items:
            try:
                # Extrair o nome do produto
                nome_item = WebDriverWait(nome, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "title_next"))).text
                nome = nome_item
                
                # Esperar explicitamente até que o preço esteja visível
                preco_element = WebDriverWait(item, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".price__symbol"))
                )
                preco = preco_element.text

                # Extrair o link do produto
                link_item = WebDriverWait(link,10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-search-item__link"))).get_attribute('href')
                link = link_item

                # Adicionar os dados ao produto
                produto = {
                    'nome': nome,
                    'preco': preco,
                    'link': link
                }
                produtos.append(produto)
            except Exception as e:
                print(f"Erro ao extrair um produto: {e}")
    except Exception as e:
        print(f"Erro ao localizar produtos na página: {e}")

    # Salvar os dados em um arquivo JSON
    with open(f"{tipo_produto}_produtos.json", "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

    print(f"Busca concluída para '{tipo_produto}', {len(produtos)} produtos encontrados.")

# Solicitar ao usuário o tipo de celular ou produto para busca
tipo_produto = input("Digite o tipo de celular ou produto para buscar: ")

# Exibir uma mensagem indicando que a busca está começando
print(f"Iniciando busca para '{tipo_produto}'...")

# Executando a busca
buscar_produtos(tipo_produto)

# Fechar o navegador
driver.quit()