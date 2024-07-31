import json
import logging
import time

ONG_JSON = 'ong_repo.json'
COMU_JSON = 'comunidade_repo.json'

def _get_registros(file_path):
    try:
        with open(file_path, 'r') as arquivo:
            try:
                registros = json.load(arquivo)
                return registros
            except json.JSONDecodeError:
                logging.warning(f'O arquivo {file_path} está vazio ou corrompido.')
                return []
    except FileNotFoundError:
        logging.error(f'Arquivo {file_path} não encontrado, verifique o caminho e tente novamente.')
        raise
    except Exception as e:
        logging.error(f'Erro ao ler o arquivo {file_path}: {e}')
        raise

def _post_registro(file_path, registro):
    try:
        registros = _get_registros(file_path)
        registros.append(registro)
        with open(file_path, 'w') as arquivo:
            json.dump(registros, arquivo, indent=4)
        return True
    except Exception as e:
        logging.error(f'Erro ao salvar registro em {file_path}: {e}')
        return False
    
def _save_full_registros(file_path, registros):
    try:
        with open(file_path, 'w') as arquivo:
            json.dump(registros, arquivo, indent=4)
        return True
    except Exception as e:
        logging.error(f'Erro ao atualizar registros em {file_path}: {e}')
        return False

def _generate_id(file_path):
    try:
        registros = _get_registros(file_path)
        if not registros:
            return 1
        else:
            return registros[-1]['id'] + 1
    except Exception as e:
        logging.error(f'Erro ao gerar ID no arquivo {file_path}: {e}')
        return 1

def create_registro(file_path, registro):
    try:
        registro['id'] = _generate_id(file_path)
        return _post_registro(file_path, registro)
    except Exception as e:
        logging.error(f'Erro ao criar registro: {e}')
        return False

def find_registro_by_id(file_path, id):
    try:
        registros = _get_registros(file_path)
        for registro in registros:
            if registro['id'] == id:
                return registro
        logging.error(f'Registro com ID {id} não encontrado.')
        return None
    except Exception as e:
        logging.error(f'Erro ao buscar registro por ID: {e}')
        return None

def list_registros(file_path):
    try:
        return _get_registros(file_path)
    except Exception as e:
        logging.error(f'Erro ao listar registros: {e}')
        return []

def update_registro(file_path, registro):
    try:
        registros = _get_registros(file_path)
        for idx, existing_registro in enumerate(registros):
            if existing_registro['id'] == registro['id']:
                registros[idx] = registro 
                _save_full_registros(file_path, registros)
            return True
        logging.error(f'Registro com ID {registro["id"]} não encontrado para atualização.')
        return False
    except Exception as e:
        logging.error(f'Erro ao atualizar registro: {e}')
        return False

def delete_registro(file_path, id):
    try:
        registros = _get_registros(file_path)
        new_registros = []
        for registro in registros:
            if registro['id'] != id:
                new_registros.append(registro)
        registros = new_registros
        _save_full_registros(file_path, registros)
        return True
        logging.error(f'Registro com ID {id} não encontrado para exclusão.')
        return False
    except Exception as e:
        logging.error(f'Erro ao deletar registro: {e}')
        return False

def list_comunidade_by_ong(id_ong):
    try:
        registros = list_registros(COMU_JSON)
        comunidades_ong = []
        for registro in registros:
            if registro['id_ong'] == id_ong:
                comunidades_ong.append(registro)
        return comunidades_ong
    except Exception as e:
        logging.error(f'Erro ao listar comunidades: {e}')

#-----------------------------------------------------------------------------

def listar_comunidade(id_ong):
    try:
        comunidades_ong = list_comunidade_by_ong(id_ong)
        if comunidades_ong:
            print("\n--- Comunidades da ONG selecionada ---")
            for comunidade in comunidades_ong:
                print(f"ID: {comunidade['id']}")
                print(f"Nome: {comunidade['nome']}")
                print(f"População: {comunidade['populacao']}")
                print(f"Região: {comunidade['regiao']}")
                print("--------------------------------------")
        else:
            print("Nenhuma comunidade encontrada para essa ONG.")
    except Exception as e:
        logging.error(f'Erro ao listar comunidades: {e}')

def selecionar_comunidade(id_ong):
    try:
        comunidades_ong = list_comunidade_by_ong(id_ong)
        id_comunidade = int(input("\nDigite o ID da comunidade que deseja selecionar: "))
        comunidade_selecionada = None
        for comunidade in comunidades_ong:
            if comunidade['id'] == id_comunidade:
                comunidade_selecionada = comunidade
                break
        if comunidade_selecionada:
            print("\n--- Comunidade selecionada ---")
            print(f"ID: {comunidade_selecionada['id']}")
            print(f"Nome: {comunidade_selecionada['nome']}")
            print(f"População: {comunidade_selecionada['populacao']}")
            print(f"Região: {comunidade_selecionada['regiao']}")
            print("------------------------")
        else:
            print("Comunidade não encontrada.")
    except Exception as e:
        logging.error(f'Erro ao selecionar comunidade: {e}')

def cadastrar_comunidade(id_ong):
    try:
        nome = input("\nDigite o nome da comunidade: ")
        populacao = input("Digite a população da comunidade: ")
        regiao = input("Digite a região da comunidade: ")
        registro = {
            'id': None,
            'id_ong': id_ong,
            'nome': nome,
            'populacao': populacao,
            'regiao': regiao
        }
        if create_registro(COMU_JSON, registro):
            print("Comunidade cadastrada com sucesso.")
        else:
            print("Erro ao cadastrar comunidade.")
    except Exception as e:
        logging.error(f'Erro ao cadastrar comunidade: {e}')

def atualizar_comunidade(id_ong):
    try:
        comunidades_ong = list_comunidade_by_ong(id_ong)

        id_comunidade = int(input("\nDigite o ID da comunidade que deseja atualizar: "))
        comunidade_selecionada = None
        for comunidade in comunidades_ong:
            if comunidade['id'] == id_comunidade:
                comunidade_selecionada = comunidade
                break
        if comunidade_selecionada:
            for key, value in comunidade_selecionada.items():
                if key == 'nome':
                    print(f"\nNome da comunidade selecionada: {value}")
                    novo_nome = input("Digite o novo nome da comunidade (ou deixe em branco para manter o mesmo): ")
                    if novo_nome:
                        comunidade_selecionada[key] = novo_nome
                elif key == 'populacao':
                    print(f"\nPopulação da comunidade selecionada: {value}")
                    novo_populacao = input("Digite a nova população da comunidade (ou deixe em branco para manter a mesma): ")
                    if novo_populacao:
                        comunidade_selecionada[key] = novo_populacao
                elif key == 'regiao':
                    print(f"\nRegião da comunidade selecionada: {value}")
                    novo_regiao = input("Digite a nova região da comunidade (ou deixe em branco para manter a mesma): ")
                    if novo_regiao:
                        comunidade_selecionada[key] = novo_regiao
            if update_registro(COMU_JSON, comunidade_selecionada):
                print("Comunidade atualizada com sucesso.")
            else:
                print("Erro ao atualizar comunidade.")
        else:
            print("Comunidade não encontrada.")
    except Exception as e:
        logging.error(f'Erro ao atualizar comunidade: {e}')

def deletar_comunidade(id_ong):
    try:
        comunidades_ong = list_comunidade_by_ong(id_ong)
        if comunidades_ong:
            print("--- Comunidades da ONG ---")
            for comunidade in comunidades_ong:
                print(f"ID: {comunidade['id']}")
                print(f"Nome: {comunidade['nome']}")
                print(f"População: {comunidade['populacao']}")
                print(f"Região: {comunidade['regiao']}")
                print("------------------------")
            id_comunidade = int(input("\nDigite o ID da comunidade que deseja deletar: "))
            comunidade_selecionada = None
            for comunidade in comunidades_ong:
                if comunidade['id'] == id_comunidade:
                    comunidade_selecionada = comunidade
                    break
            if comunidade_selecionada:
                if delete_registro(COMU_JSON, id_comunidade):
                    print("Comunidade deletada com sucesso.")
                else:
                    print("Erro ao deletar comunidade.")
            else:
                print("Comunidade não encontrada.")
        else:
            print("Nenhuma comunidade encontrada para essa ONG.")
    except Exception as e:
        logging.error(f'Erro ao deletar comunidade: {e}')

def listar_ong():
    try:
        registros = list_registros(ONG_JSON)
        if registros:
            print("\n--- ONGs Cadastradas ---")
            for registro in registros:
                print(f"ID: {registro['id']}")
                print(f"Nome: {registro['nome']}")
                print(f"CNPJ: {registro['cnpj']}")
                print(f"Área de Atuação: {registro['area_atuacao']}")
                print("------------------------")
        else:
            print("Nenhuma ONG cadastrada.")
    except Exception as e:
        logging.error(f'Erro ao listar ONGs: {e}')

def selecionar_ong():
    try:
        registros = list_registros(ONG_JSON)
        id_ong = int(input("\nDigite o ID da ONG que deseja selecionar: "))
        ong_selecionada = None
        for registro in registros:
            if registro['id'] == id_ong:
                ong_selecionada = registro
                break
        if ong_selecionada:
            print("\n--- ONG Selecionada ---")
            print(f"ID: {ong_selecionada['id']}")
            print(f"Nome: {ong_selecionada['nome']}")
            print(f"CNPJ: {ong_selecionada['cnpj']}")
            print(f"Área de Atuação: {ong_selecionada['area_atuacao']}")
            print("------------------------")
        else:
            print("ONG não encontrada.")
    except Exception as e:
        logging.error(f'Erro ao selecionar ONG: {e}')

def cadastrar_ong():
    try:
        nome = input("\nDigite o nome da ONG: ")
        cnpj = input("Digite o CNPJ da ONG: ")
        area_atuacao = input("Digite a área de atuação da ONG: ")
        registro = {
            'id': None,
            'nome': nome,
            'cnpj': cnpj,
            'area_atuacao': area_atuacao
        }
        if create_registro(ONG_JSON, registro):
            print("ONG cadastrada com sucesso.")
        else:
            print("Erro ao cadastrar ONG.")
    except Exception as e:
        logging.error(f'Erro ao cadastrar ONG: {e}')

def atualizar_ong():
    try:
        registros = list_registros(ONG_JSON)
        id_ong = int(input("\nDigite o ID da ONG que deseja atualizar: "))
        ong_selecionada = None
        for registro in registros:
            if registro['id'] == id_ong:
                ong_selecionada = registro
                break
        if ong_selecionada:
            for key, value in ong_selecionada.items():
                if key == 'nome':
                    print(f"\nNome da ONG selecionada: {value}")
                    novo_nome = input("Digite o novo nome da ONG (ou deixe em branco para manter o mesmo): ")
                    if novo_nome:
                        ong_selecionada[key] = novo_nome
                elif key == 'cnpj':
                    print(f"\nCNPJ da ONG selecionada: {value}")
                    novo_cnpj = input("Digite o novo CNPJ da ONG (ou deixe em branco para manter o mesmo): ")
                    if novo_cnpj:
                        ong_selecionada[key] = novo_cnpj
                elif key == 'area_atuacao':
                    print(f"\nÁrea de Atuação da ONG selecionada: {value}")
                    nova_area_atuacao = input("Digite a nova área de atuação da ONG (ou deixe em branco para manter a mesma): ")
                    if nova_area_atuacao:
                        ong_selecionada[key] = nova_area_atuacao
            if update_registro(ONG_JSON, ong_selecionada):
                print("ONG atualizada com sucesso.")
            else:
                print("Erro ao atualizar ONG.")
        else:
            print("ONG não encontrada.")
    except Exception as e:
        logging.error(f'Erro ao atualizar ONG: {e}')

def deletar_ong():
    try:
        registros = list_registros(ONG_JSON)
        if registros:
            print("--- ONGs Cadastradas ---")
            for registro in registros:
                print(f"ID: {registro['id']}")
                print(f"Nome: {registro['nome']}")
                print(f"CNPJ: {registro['cnpj']}")
                print(f"Área de Atuação: {registro['area_atuacao']}")
                print("------------------------")
            id_ong = int(input("\nDigite o ID da ONG que deseja deletar: "))
            ong_selecionada = None
            for registro in registros:
                if registro['id'] == id_ong:
                    ong_selecionada = registro
                    break
            if ong_selecionada:
                if delete_registro(ONG_JSON, id_ong):
                    print("ONG deletada com sucesso.")
                else:
                    print("Erro ao deletar ONG.")
            else:
                print("ONG não encontrada.")
        else:
            print("Nenhuma ONG cadastrada.")
    except Exception as e:
        logging.error(f'Erro ao deletar ONG: {e}')

def gerenciar_ongs():
    id_ong = int(input("\nDigite o ID da ONG que deseja gerenciar: "))
    ong_selecionada = find_registro_by_id(ONG_JSON, int(id_ong))
    if ong_selecionada:
        menu_comunidades(int(id_ong))
    else:
        print("ONG não encontrada.")

#-----------------------------------------------------------------------------

def menu_comunidades(id_ong):
    while True:
        print(f"\n--- Gerenciamento de Comunidades: ONG ID {id_ong} ---")
        print("1. Listar Comunidades")
        print("2. Selecionar Comunidade")
        print("3. Cadastrar Comunidade")
        print("4. Atualizar Comunidade")
        print("5. Deletar Comunidade")
        print("6. Voltar ao Menu Principal")
        print("--------------------------------------------")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listar_comunidade(id_ong)
        elif opcao == '2':
            selecionar_comunidade(id_ong)
        elif opcao == '3':
            cadastrar_comunidade(id_ong)
        elif opcao == '4':
            atualizar_comunidade(id_ong)
        elif opcao == '5':
            deletar_comunidade(id_ong)
        elif opcao == '6':
            break
        else:
            print("Opção inválida, tente novamente.")

def menu_ongs():
    while True:
        print("\n--- Menu Principal ---")
        print("1. Listar ONGs")
        print("2. Selecionar ONG")
        print("3. Cadastrar ONG")
        print("4. Atualizar ONG")
        print("5. Deletar ONG")
        print("6. Gerenciar ONG")
        print("7. Sair")
        print("----------------------")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            listar_ong()
        elif opcao == '2':
            selecionar_ong()
        elif opcao == '3':
            cadastrar_ong()
        elif opcao == '4':
            atualizar_ong()
        elif opcao == '5':
            deletar_ong()
        elif opcao == '6':
            gerenciar_ongs()
        elif opcao == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

# Execução do menu principal
menu_ongs()
