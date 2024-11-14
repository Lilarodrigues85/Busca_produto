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
driver.implicitly_wait(10)

# Função para buscar e extrair dados
def buscar_produtos_google_shopping(busca):
    driver.get(f"https://www.google.com/search?sca_esv=a0b6cc145a6c8085&hl=pt-BR&sxsrf=ADLYWIIk6nMp-BrVxWs1sulbKd-7_Wp4vg:1730941974229&q={busca}")

    # Espera até que o botão 'Shopping' esteja visível e clica nele
    try:
        botao_shopping = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Shopping"))
        )
        botao_shopping.click()
    except Exception as e:
        print(f"Erro ao clicar no botão Shopping: {e}")
        driver.quit()
        return

    # Espera até que os resultados da aba 'Shopping' sejam carregados
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sh-dgr__content"))
    )

    # Rola a página para garantir o carregamento dos produtos
    produtos = []
    max_produtos = 10
    produtos_encontrados = 0

    while produtos_encontrados < max_produtos:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Coleta os produtos
        items = driver.find_elements(By.CSS_SELECTOR, ".sh-dgr__content")
        for item in items:
            if produtos_encontrados >= max_produtos:
                break  # Limita a 10 produtos

            try:
                nome = item.find_element(By.XPATH, "/html/body/div[4]/div/div[4]/div[3]/div/div[3]/div[1]/g-scrolling-carousel/div[1]/div/div/div[1]/a/div[3]/div/p//text()").text
            except:
                nome = "Nome não encontrado"
                
            try:
                preco = item.find_element(By.XPATH, "/html/body/div[4]/div/div[4]/div[3]/div/div[3]/div[1]/g-scrolling-carousel/div[1]/div/div/div[1]/a/div[3]/div/div[1]/span/p//text()").text
            except:
                preco = "Preço não disponível"

            link = item.find_element(By.XPATH, "/html/body/div[4]/div/div[4]/div[3]/div/div[3]/div[1]/g-scrolling-carousel/div[1]/div/div/div[1]/a/p//text()")

            produto = {
                'nome': nome,
                'preco': preco,
                'link': link
            }
            produtos.append(produto)
            produtos_encontrados += 1

        if produtos_encontrados >= max_produtos:
            break

    # Salva os dados em JSON
    with open(f"produtos_{busca}.json", "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

    print(f"Busca completa para '{busca}'. {len(produtos)} produtos encontrados.")

# Entrada do usuário
busca = input("Digite o produto que você deseja buscar: ")

# Chama a função
buscar_produtos_google_shopping(busca)

# Fecha o navegador
driver.quit()