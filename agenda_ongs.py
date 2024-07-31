import json
from unittest import result
#MODELS-------------------

ong = {
    'id': 0,
    'cnpj': '',
    'nome': '',
    'territorio': ''
}

comunidade = {
    'id': 0,
    'ong_id': '',
    'nome': '',
    'populacao': 0 
}

#REPOSITORIES----------------
ONG_JSON = '/workspaces/fap_agenda_ongs/ong_repo.json'
COMU_JSON = '/workspaces/fap_agenda_ongs/comunidade_repo.json'

def create_ong(ong):   
    new_ong = ong
    new_ong['id'] = _generate_id(ONG_JSON)

    try:
        with open(ONG_JSON, 'r+') as arquivo:
            try: 
                ongs = json.load(arquivo)
            except json.JSONDecodeError: 
                print('Arquivo JSON em branco. Gerando primeira ong.')
                ongs = []
                
            ongs.append(new_ong)
            arquivo.seek(0)
            json.dump(ongs, arquivo, indent=4)
            arquivo.truncate()
            return True
    except Exception as e:
        print(f'Erro no repositorio: {e}')
        return False

def find_ong_by_id(id):
        try:
            with open(ONG_JSON, 'r') as arquivo:
                ongs = json.load(arquivo)
                for ong in ongs:
                    if ong['id'] == id:
                        return ong
    
                raise ValueError('Tarefa não encontrada.')
        except json.decoder.JSONDecodeError:
            print('Arquivo JSON em branco.')
        except Exception as e:
            print(f'Erro no repositorio: {e}')

def list_ongs():
        try:
            with open(ONG_JSON, 'r') as arquivo:
                ongs = json.load(arquivo)
                return ongs

        except json.decoder.JSONDecodeError:
            print('Arquivo JSON em branco.')
        except Exception as e:
            print(f'Erro no repositorio: {e}')   

def update_ong(ong):
    try:
        updated_ong = find_ong_by_id(ong['id'])
        if updated_ong:
            updated_ong['cnpj'] = ong['cnpj']
            updated_ong['nome'] = ong['nome']
            updated_ong['territorio'] = ong['territorio']

        else:
            return False

        with open(ONG_JSON, 'r+') as arquivo:
            ongs = json.load(arquivo)
            for o in ongs:
                if o['id'] == ong['id']:
                    o['cnpj'] = updated_ong['cnpj']
                    o['nome'] = updated_ong['nome']
                    o['territorio'] = updated_ong['territorio']
                    break

            arquivo.seek(0)
            json.dump(ongs, arquivo, indent=4)
            arquivo.truncate()
            return True
    except Exception as e:
        print(f'Erro no repositorio: {e}')
        return False

def delete_ong(id):
    try:
        with open(ONG_JSON, 'r+') as arquivo:
            ongs = json.load(arquivo)
            for ong in ongs:
                if ong['id'] == id:
                    ongs.remove(ong)
                    arquivo.seek(0)
                    json.dump(ongs, arquivo, indent=4)
                    arquivo.truncate()
                    print('Tarefa deletada com sucesso.')
                    return True
            return False
    except Exception as e:
        print(f'Erro no repositorio: {e}')
        return False

def create_comunidade(comunidade):   
    new_comunidade = comunidade
    new_comunidade['id'] = _generate_id(COMU_JSON)

    try:
        with open(COMU_JSON, 'r+') as arquivo:
            try: 
                comunidades = json.load(arquivo)
            except json.JSONDecodeError: 
                print('Arquivo JSON em branco. Gerando primeira comunidade.')
                comunidades = []
                
            comunidades.append(new_comunidade)
            arquivo.seek(0)
            json.dump(comunidades, arquivo, indent=4)
            arquivo.truncate()
            return True
    except Exception as e:
        print(f'Erro no repositorio: {e}')
        return False

def find_comunidade_by_id(id):
    try:
        with open(COMU_JSON, 'r') as arquivo:
            comunidades = json.load(arquivo)
            for comunidade in comunidades:
                if comunidade['id'] == id:
                    return comunidade
    
            raise ValueError('Comunidade não encontrada.')
    except json.decoder.JSONDecodeError:
        print('Arquivo JSON em branco.')
    except Exception as e:
        print(f'Erro no repositorio: {e}')

def list_comunidades():
    try:
        with open(COMU_JSON, 'r') as arquivo:
            comunidades = json.load(arquivo)
            return comunidades
    except json.decoder.JSONDecodeError:
        print('Arquivo JSON em branco.')
    except Exception as e:
        print(f'Erro no repositorio: {e}')   

def update_comunidade(comunidade):
    try:
        updated_comunidade = find_comunidade_by_id(comunidade['id'])
        if updated_comunidade:
            updated_comunidade['ong_id'] = comunidade['ong_id']
            updated_comunidade['nome'] = comunidade['nome']
            updated_comunidade['populacao'] = comunidade['populacao']
        else:
            return False

        with open(COMU_JSON, 'r+') as arquivo:
            comunidades = json.load(arquivo)
            for c in comunidades:
                if c['id'] == comunidade['id']:
                    c['ong_id'] = updated_comunidade['ong_id']
                    c['nome'] = updated_comunidade['nome']
                    c['populacao'] = updated_comunidade['populacao']
                    break

            arquivo.seek(0)
            json.dump(comunidades, arquivo, indent=4)
            arquivo.truncate()
            return True
    except Exception as e:
        print(f'Erro no repositorio: {e}')
        return False

def delete_comunidade(id):
    try:
        with open(COMU_JSON, 'r+') as arquivo:
            comunidades = json.load(arquivo)
            for comunidade in comunidades:
                if comunidade['id'] == id:
                    comunidades.remove(comunidade)
                    arquivo.seek(0)
                    json.dump(comunidades, arquivo, indent=4)
                    arquivo.truncate()
                    print('Comunidade deletada com sucesso.')
                    return True
            return False
    except Exception as e:
        print(f'Erro no repositorio: {e}')
        return False

def _generate_id(file_path):
    try:
        with open(file_path, 'r') as arquivo:
            entidades = json.load(arquivo)
            if len(entidades) == 0:
                return 1
            else:
                return entidades[-1]['id'] + 1
    except json.decoder.JSONDecodeError:
        return 1
    except Exception as e:
        print(f'Erro no repositorio: {e}')
        return None

#CONTROLLER-------------------

def criar_ong(ong_cnpj, ong_nome, ong_territorio):
    ong = {
        'id': None,
        'cnpj': ong_cnpj,
        'nome': ong_nome,
        'territorio': ong_territorio
    }
    
    try: 
        create_ong(ong)
        return True  
    except Exception as e:
        print('Erro ao cadastrar tarefa, tente novamente.', e)
        return False

def buscar_ong(id):
    try:
        ong = find_ong_by_id(id)
        return ong
    except Exception as e:
        print('Erro ao buscar tarefa, tente novamente.', e)
        return None

def listar_ongs():
    try:
        ongs = list_ongs()
        return ongs
    except Exception as e:
        print('Erro ao listar tarefas, tente novamente.', e)
        return None

def atualizar_ong(ong_id, ong_cnpj, ong_nome, ong_territorio):
    ong = {
        'id': ong_id,
        'cnpj': ong_cnpj,
        'nome': ong_nome,
        'territorio': ong_territorio
    }
    
    try:
        update_ong(ong)
        return True
    except Exception as e:
        print('Erro ao atualizar tarefa, tente novamente.', e)
        return False

def deletar_ong(id):
    try:
        delete_ong(id)
        return True
    except Exception as e:
        print('Erro ao deletar tarefa, tente novamente.', e)
        return False

def criar_comunidade(comunidade_cnpj, comunidade_nome, comunidade_territorio):
    comunidade = {
        'id': None,
        'cnpj': comunidade_cnpj,
        'nome': comunidade_nome,
        'territorio': comunidade_territorio
    }
    
    try: 
        create_comunidade(comunidade)
        return True  
    except Exception as e:
        print('Erro ao cadastrar tarefa, tente novamente.', e)
        return False

def buscar_comunidade(id):
    try:
        comunidade = find_comunidade_by_id(id)
        return comunidade
    except Exception as e:
        print('Erro ao buscar tarefa, tente novamente.', e)
        return None

def listar_comunidades():
    try:
        comunidades = list_comunidades()
        return comunidades
    except Exception as e:
        print('Erro ao listar tarefas, tente novamente.', e)
        return None

def atualizar_comunidade(comunidade_id, comunidade_cnpj, comunidade_nome, comunidade_territorio):
    comunidade = {
        'id': comunidade_id,
        'cnpj': comunidade_cnpj,
        'nome': comunidade_nome,
        'territorio': comunidade_territorio
    }
    
    try:
        update_comunidade(comunidade)
        return True
    except Exception as e:
        print('Erro ao atualizar tarefa, tente novamente.', e)
        return False

def deletar_comunidade(id):
    try:
        delete_comunidade(id)
        return True
    except Exception as e:
        print('Erro ao deletar tarefa, tente novamente.', e)
        return False


#VIEW-------------------

def menu():
    while True:
        print('1 - ONGs')
        print('2 - Comunidades')
        print('0 - Sair')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            menu_ongs()
        elif opcao == '2':
            menu_comunidades()
        elif opcao == '0':
            break
        else:
            print('Opção inválida.')

def menu_ongs():
    while True:
        print('1 - Cadastrar ONG')
        print('2 - Encontrar ONG')
        print('3 - Listar ONGs')
        print('4 - Atualizar ONG')
        print('5 - Deletar ONG')
        print('0 - Voltar')

        opcao = input('Escolha uma opção: ')
        if opcao == 1:

    