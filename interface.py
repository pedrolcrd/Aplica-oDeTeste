import requests
import os

def main():
    base = os.getenv("API_URL", "http://localhost:8000")
    while True:
        print("\n1. Listar itens\n2. Criar item\n0. Sair")
        opt = input("Escolha uma opção: ")
        if opt == "0":
            break
        elif opt == "1":
            resp = requests.get(f"{base}/items")
            for item in resp.json():
                print(f"[{item['id']}] {item['name']}")
        elif opt == "2":
            name = input("Nome do item: ")
            resp = requests.post(f"{base}/items", json={"name": name})
            print(resp.json())
        else:
            print("Opção inválida")

if __name__ == "__main__":
    main()
