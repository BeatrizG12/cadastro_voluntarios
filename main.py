cad# Importa os módulos necessários do Kivy (para a interface gráfica)
from kivy.app import App  # Responsável por rodar o aplicativo
from kivy.uix.boxlayout import BoxLayout  # Layout em forma de caixa (coluna ou linha)
from kivy.uix.label import Label  # Rótulo de texto
from kivy.uix.button import Button  # Botão clicável
from kivy.uix.textinput import TextInput  # Campo para digitar texto

# Importa o módulo para lidar com banco de dados, neste usamos o banco de dados sqlite3
import sqlite3

# Criação da classe principal do aplicativo, herdando de App (do Kivy)
class CadastroVoluntario(App):
    
    # Função principal que monta a interface do aplicativo
    def build(self):
        # Conecta ao banco de dados (ou cria um)
        self.conectar_banco()
        
        # Cria um layout vertical com espaço interno e entre os elementos
        self.box = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Cria os campos onde o usuário vai digitar o nome, telefone e e-mail para se cadastrar
        self.nome_input = TextInput(hint_text='Nome', multiline=False)
        self.telefone_input = TextInput(hint_text='Telefone', multiline=False)
        self.email_input = TextInput(hint_text='E-mail', multiline=False)

        # Adiciona os campos de entrada ao layout
        self.box.add_widget(self.nome_input)
        self.box.add_widget(self.telefone_input)
        self.box.add_widget(self.email_input)

        # Cria o botão "Cadastrar" e define o que acontece quando ele é clicado
        botao = Button(text='Cadastrar')
        botao.bind(on_press=self.cadastrar)  # Quando clicar, chama a função cadastrar
        self.box.add_widget(botao)

        # Cria uma área de texto para exibir mensagens de resposta
        self.resposta = Label(text='')
        self.box.add_widget(self.resposta)

        # Retorna a interface construída
        return self.box

    # Função que conecta o banco de dados
    def conectar_banco(self):
        # Conecta ao arquivo "voluntarios.db" (será criado se não existir)
        self.conexao = sqlite3.connect("voluntarios.db")
        self.cursor = self.conexao.cursor()
        
        # Cria uma tabela chamada "voluntarios", se ainda não existir
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS voluntarios ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "  # ID automático
            "nome TEXT NOT NULL, "  # Campo de nome
            "telefone TEXT NOT NULL, "  # Campo de telefone
            "email TEXT NOT NULL)"  # Campo de e-mail
        )
        
        # Salva as alterações no banco
        self.conexao.commit()

    # Função que é chamada quando o botão "Cadastrar" é clicado
    def cadastrar(self, instance):
        # Pega o texto digitado nos campos
        nome = self.nome_input.text.strip()
        telefone = self.telefone_input.text.strip()
        email = self.email_input.text.strip()

        # Verifica se todos os campos foram preenchidos
        if nome and telefone and email:
            # Insere os dados na tabela do banco de dados
            self.cursor.execute('''
                INSERT INTO voluntarios (nome, telefone, email)
                VALUES (?, ?, ?)
            ''', (nome, telefone, email))
            self.conexao.commit()  # Salva os dados

            # Exibe mensagem de sucesso e limpa os campos
            self.resposta.text = f'{nome} cadastrado com sucesso!'
            self.limpar_campos()
        else:
            # Exibe mensagem de erro se algum campo estiver vazio
            self.resposta.text = 'Por favor, preencha todos os campos.'

    # Função para limpar os campos de texto após o cadastro
    def limpar_campos(self):
        self.nome_input.text = ''
        self.telefone_input.text = ''
        self.email_input.text = ''

# Parte que inicia o aplicativo
if __name__ == '__main__':
    CadastroVoluntario().run()
