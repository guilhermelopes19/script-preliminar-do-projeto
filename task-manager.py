#Alunos
#Guilherme Souza Lopes - 072320015
#Sara Stephanie Costa - 072320039

# !!! Necessario instalar a biblioteca pandas e openpyxl(utilizada pelo pandas para criar tabelas excel) !!!

import pandas as pd # utilizado para gerenciar os dados e tabelas
from os import system # utilizado para limpar o terminal com os metodos system("cls") e system("clear") 
import platform # utilizado para verificar o sistema operacional e deste modo utilizar o comando respectivo do sistema para limpar o terminal utilizando a funcao system do modulo os
import sys # Utilizado para fechar o programa

# O seguinte programa é um gerenciador de tarefas que pode adicionar, remover e visualizar as tarefas, e salva os dados em uma tabela excel 

# Classe utilizada para gerenciar as tarefas
class TaskManager:
    # funcao construtora da classe que verifica se ja existe uma tabela com dados, se nao cria uma tabela para salvar os dados
    def __init__(self):
        try:
            self.__dfTask = pd.read_excel("tasks_table.xlsx")
            print("Lendo dados...")
        except FileNotFoundError:
            print("Criando tabela...")
            self.__dfTask = pd.DataFrame({
                "nomeTarefa": [],
                "equipe": [],
                "equipamentos": [],
                "materiais": [],
            })
            self.updateTable()
    
    # Atualiza a tabela(excel) com os dados presentes na tabela __dfTask(DataFrame do pandas) 
    def updateTable(self):
        self.__dfTask.to_excel("tasks_table.xlsx", index=False)
        print("Atualizando tabela...")

    # Adiciona uma nova tarefa a tabela
    def addTask(self, nomeTarefa: str, membrosEquipe: list, equipamentos: list, materiais: list):
        newLine = {
            "nomeTarefa": nomeTarefa,
            "equipe": ', '.join(membrosEquipe),
            "equipamentos": ', '.join(equipamentos),
            "materiais": ', '.join(materiais)
        }
        self.__dfTask = pd.concat([self.__dfTask, pd.DataFrame([newLine])], ignore_index=True)
        self.updateTable()
    
    # Remove uma tarefa da tabela
    def removeTask(self, index):
        try:
            self.__dfTask.drop(index, inplace=True)
            self.__dfTask.reset_index(drop=True, inplace=True)
            self.updateTable()
            print('Removido com sucesso!')
        except KeyError:
            print('Index não encontrado!')

    # Retorna a tabela __dfTask
    def getTableTasks(self):
        return self.__dfTask

# Instacia de um objeto TaskManager
taskManager = TaskManager()

# Metodo que imprimi o menu principal da aplicacao e permiti escolher outras acoes no sistema
def main():
    cleanTerminal()

    print('-'*10, 'Gerenciador de Tarefas', '-'*10)
    print('0 - Adicionar Tarefa')
    print("1 - Remover Tarefa")
    print('2 - Visualizar tarefas')
    print('3 - Sair')

    numMenu = int(input('Digite o número do que deseja fazer: '))

    if numMenu == 0:
        optionAdd()
    elif numMenu == 1:
        optionRemove()
    elif numMenu == 2:
        print('visulizar tarefas...')
        optionView()
    elif numMenu == 3:
        sys.exit()

# Imprimi no terminal a area de adicionar novas tarefas ao objeto taskManager
def optionAdd():
    cleanTerminal()
    print('-'*10, 'Adicionar Tarefa', '-'*10)
    
    nomeTarefa = input('Digite o nome da tarefa: ')
    membrosEquipe = []
    equipamentos = []
    materiais = []

    while True:
        nomeMembro = input("Digite o nome do membro(Pressione Enter duas vezes quando terminar): ").strip()
        
        if nomeMembro != "":
            membrosEquipe.append(nomeMembro)
        else:
            break
    
    while True:
        equipamento = input("Digite o nome do equipamento(Pressione Enter duas vezes quando terminar): ").strip()

        if equipamento != "":
            equipamentos.append(equipamento)
        else:
            break
    
    while True:
        material = input("Digite o nome do material(Pressione Enter duas vezes quando terminar): ").strip()

        if material != "":
            materiais.append(material)
        else:
            break
    
    taskManager.addTask(nomeTarefa, membrosEquipe, equipamentos, materiais)

    print('Tarefa adionada com sucesso!')
    input('(Pressione Enter para voltar ao menu)')

# Imprimi a area para remover tarefas cadastradas no sistema
def optionRemove():
    cleanTerminal()
    print('-'*10, 'Remover Tarefa', '-'*10)
    if len(taskManager.getTableTasks()) != 0:
        i = 0
        while i < len(taskManager.getTableTasks()):
            print('Indice:',i, ' ', 'Tarefa',taskManager.getTableTasks().loc[i, 'nomeTarefa'])
            i += 1
        indexLine = input("Digite o indice da tarefa que sera removida(Deixe vazio para cancelar): ").strip()

        if indexLine != "":
            taskManager.removeTask(int(indexLine))
        else:
            print('Remocao cancelada!')
    else:
        print("Sem tarefas cadastradas!")
    input('(Pressione Enter para voltar ao menu)')

#Imprimi as tarefas cadastradas no sistema
def optionView():
    cleanTerminal()

    print('-'*10, 'Visualizar Tarefas', '-'*10)

    tb = taskManager.getTableTasks()
    i = 0

    if len(tb) > 0:
        while i < len(tb):
            print((i + 1), '- Nome Tarefa:', tb.loc[i, "nomeTarefa"])
            print('    Membros:', tb.loc[i, 'equipe'])
            print('    Equipamentos:', tb.loc[i, 'equipamentos'])
            print('    Material:', tb.loc[i, 'materiais'])
            i += 1
    else:
        print("Nenhuma tarefa cadastrada!")
    input('(Pressione Enter para voltar ao menu)')

# Limpa o terminal para manter as informacoes organizadas
def cleanTerminal():
    operatingSystem = platform.system()
    if operatingSystem == 'Windows':
        system('cls')
    else:
        system('clear')

# Loop que repetirar de forma infinita chamando o metodo main(). Este loop so acabara se o metodo sys.exit() for chamado dentro da logica da funcao main()
while True:
    main()
