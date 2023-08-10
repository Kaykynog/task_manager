import sqlite3
import argparse
import sys

# Conectar ao banco de dados
conexao = sqlite3.connect('tarefas.db')
cursor = conexao.cursor()

# Criar a tabela de tarefas (se não existir)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data_vencimento TEXT,
        concluida BOOLEAN
    )
''')
conexao.commit()

# Definir as funções para manipulação de tarefas
def adicionar_tarefa(titulo, descricao, data_vencimento):
    cursor.execute('INSERT INTO tarefas (titulo, descricao, data_vencimento, concluida) VALUES (?, ?, ?, ?)',
                   (titulo, descricao, data_vencimento, False))
    conexao.commit()


def listar_tarefas():
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()
    for tarefa in tarefas:
        print(f"ID: {tarefa[0]}, Título: {tarefa[1]}, Descrição: {tarefa[2]}, Data de Vencimento: {tarefa[3]}, Concluída: {'Sim' if tarefa[4] else 'Não'}")

def atualizar_tarefa(id_tarefa, titulo, descricao, data_vencimento):
    cursor.execute('UPDATE tarefas SET titulo=?, descricao=?, data_vencimento=? WHERE id=?',
                   (titulo, descricao, data_vencimento, id_tarefa))
    conexao.commit()

def marcar_como_concluida(id_tarefa):
    cursor.execute('UPDATE tarefas SET concluida=True WHERE id=?', (id_tarefa,))
    conexao.commit()

def excluir_tarefa(id_tarefa):
    cursor.execute('DELETE FROM tarefas WHERE id=?', (id_tarefa,))
    conexao.commit()

# Função principal
def main():
    parser = argparse.ArgumentParser(description='Gerenciador de Tarefas')
    parser.add_argument('-a', '--adicionar', nargs=3, metavar=('titulo', 'descricao', 'data_vencimento'), help='Adicionar uma nova tarefa')
    parser.add_argument('-l', '--listar', action='store_true', help='Listar todas as tarefas')
    parser.add_argument('-u', '--atualizar', nargs=4, metavar=('id_tarefa', 'titulo', 'descricao', 'data_vencimento'), help='Atualizar uma tarefa')
    parser.add_argument('-c', '--concluida', type=int, metavar='id_tarefa', help='Marcar uma tarefa como concluída')
    parser.add_argument('-d', '--excluir', type=int, metavar='id_tarefa', help='Excluir uma tarefa')

    args = parser.parse_args()

    if args.adicionar:
        adicionar_tarefa(*args.adicionar)
        print("Tarefa adicionada com sucesso.")
    elif args.listar:
        listar_tarefas()
    elif args.atualizar:
        atualizar_tarefa(*args.atualizar)
        print("Tarefa atualizada com sucesso.")
    elif args.concluida:
        marcar_como_concluida(args.concluida)
        print("Tarefa marcada como concluída.")
    elif args.excluir:
        excluir_tarefa(args.excluir)
        print("Tarefa excluída com sucesso.")
    else:
        parser.print_help()

    conexao.close()

if __name__ == '__main__':
    main()
