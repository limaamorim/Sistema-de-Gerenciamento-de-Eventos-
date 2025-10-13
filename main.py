import time
from sistema.sistema_eventos import SistemaEventos
from sistema.autenticador import Autenticador
from cores import Cores


# ============================================================
def cabecalho(titulo):
    print(f"{Cores.ROXO}{'=' * 60}{Cores.RESET}")
    print(f"{Cores.NEGRITO}{Cores.AZUL}{titulo.center(60)}{Cores.RESET}")
    print(f"{Cores.ROXO}{'=' * 60}{Cores.RESET}")


def menu_admin():
    print(f"""
{Cores.CIANO}1{Cores.RESET} - Cadastrar novo evento
{Cores.CIANO}2{Cores.RESET} - Listar eventos
{Cores.CIANO}3{Cores.RESET} - Buscar por categoria
{Cores.CIANO}4{Cores.RESET} - Buscar por data
{Cores.CIANO}5{Cores.RESET} - Inscrever-se em evento
{Cores.CIANO}6{Cores.RESET} - Cancelar inscrição
{Cores.CIANO}7{Cores.RESET} - Relatórios
{Cores.CIANO}8{Cores.RESET} - Excluir evento
{Cores.VERMELHO}0{Cores.RESET} - Sair
""")


def menu_usuario():
    print(f"""
{Cores.CIANO}1{Cores.RESET} - Cadastrar novo evento
{Cores.CIANO}2{Cores.RESET} - Listar eventos
{Cores.CIANO}3{Cores.RESET} - Buscar por categoria
{Cores.CIANO}4{Cores.RESET} - Buscar por data
{Cores.CIANO}5{Cores.RESET} - Inscrever-se em evento
{Cores.CIANO}6{Cores.RESET} - Cancelar inscrição
{Cores.VERMELHO}0{Cores.RESET} - Sair
""")


# ============================================================
def main():
    sistema = SistemaEventos()
    login = Autenticador()

    Autenticador.limpar_tela()
    cabecalho("🎟️ Sistema de Gerenciamento de Eventos 🎟️")
    print(f"{Cores.VERDE}Bem-vindo! Faça login ou cadastre-se.{Cores.RESET}")

    usuario = None
    while not usuario:
        print(f"\n{Cores.CIANO}1{Cores.RESET} - Login")
        print(f"{Cores.CIANO}2{Cores.RESET} - Cadastro")
        escolha = input("Escolha: ").strip()

        if escolha == "1":
            email = input("E-mail: ")
            senha = input("Senha: ")
            usuario = login.fazer_login(email, senha)
            if usuario:
                time.sleep(2)
                Autenticador.limpar_tela()
        elif escolha == "2":
            nome = input("Nome: ")
            email = input("E-mail: ")
            senha = input("Senha: ")
            login.cadastrar_usuario(nome, email, senha)
            time.sleep(2)
            Autenticador.limpar_tela()
        else:
            print(f"{Cores.AMARELO}⚠️ Opção inválida. Digite 1 ou 2{Cores.RESET}")
            time.sleep(1)
            Autenticador.limpar_tela()


    # --------------------------------------------------------
    while True:
        Autenticador.limpar_tela()
        cabecalho("MENU PRINCIPAL")

        if usuario.get_tipo() == "admin":
            menu_admin()
        else:
            menu_usuario()

        opcao = input(f"{Cores.AMARELO}👉 Escolha uma opção: {Cores.RESET}")

        # ================= ADMIN OU USUÁRIO ==================
        if opcao == "1":
            Autenticador.limpar_tela()
            cabecalho("🗓️ Cadastrar novo evento")

            nome = input("Nome do evento: ")
            data = input("Data (dd/mm/YYYY): ")
            hora = input("Hora (HH:MM): ")
            local = input("Local: ")
            categoria = input("Categoria: ")
            capacidade = int(input("Capacidade: "))
            preco = float(input("Preço: "))
            tipo = input("Tipo (1-Evento | 2-Palestra | 3-Workshop): ")

            sistema.cadastrar_evento(nome, data, hora, local, capacidade, categoria, preco, tipo)
            input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")

        elif opcao == "2":
            Autenticador.limpar_tela()
            sistema.listar_eventos()
            input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")

        elif opcao == "3":
            Autenticador.limpar_tela()
            categorias = sistema.listar_categorias_enumeradas()
            if categorias:  # só continua se houver categorias
                escolha = input("\nDigite o número da categoria que deseja visualizar: ").strip()
                
                if not escolha.isdigit():
                    print("❌ Digite um número válido.")
                else:
                    idx = int(escolha) - 1
                    if 0 <= idx < len(categorias):
                        categoria_selecionada = categorias[idx]
                        sistema.buscar_por_categoria(categoria_selecionada)
                    else:
                        print("❌ Número fora do intervalo.")

            input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")

        elif opcao == "4":
            Autenticador.limpar_tela()
            print("🔎 Buscar eventos por intervalo de datas")
            data_inicial = input("Data inicial (dd/mm/YYYY): ").strip()
            data_final = input("Data final (dd/mm/YYYY): ").strip()
            sistema.buscar_por_data(data_inicial, data_final)
            input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")


        elif opcao == "5":
            Autenticador.limpar_tela()
            sistema.listar_eventos()
            indice = int(input("Escolha o evento: "))
            sistema.inscrever_participante(indice, usuario)
            input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")

        elif opcao == "6":
            Autenticador.limpar_tela()
            eventos_inscritos = sistema.listar_eventos_inscritos(usuario)

            if not eventos_inscritos:
                input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")
                continue  # volta ao menu se não tiver eventos

            try:
                indice = int(input("\nDigite o número do evento que deseja cancelar: "))
                if 1 <= indice <= len(eventos_inscritos):
                    evento = eventos_inscritos[indice - 1]
                    sistema.cancelar_inscricao(sistema.eventos.index(evento) + 1, usuario)
                else:
                    print(f"{Cores.VERMELHO}❌ Número inválido.{Cores.RESET}")
            except ValueError:
                print(f"{Cores.VERMELHO}❌ Entrada inválida. Digite um número.{Cores.RESET}")

            input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")


        elif opcao == "7" and usuario.get_tipo() == "admin":
            Autenticador.limpar_tela()
            sistema.relatorios()
            input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")
        
        elif opcao == "8":                   
            Autenticador.limpar_tela()
            # Verifica se é admin antes de listar
            if usuario.get_tipo() != "admin":
                print(f"{Cores.AMARELO}⚠️ Apenas administradores podem excluir eventos.{Cores.RESET}")
                input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")
                continue

            # Lista eventos disponíveis
            sistema.listar_eventos()

            # Pede número do evento para excluir
            try:
                indice = int(input("\nDigite o número do evento que deseja excluir: "))
                sistema.deletar_evento(indice, usuario)
            except ValueError:
                print(f"{Cores.VERMELHO}❌ Entrada inválida. Digite um número.{Cores.RESET}")

            input(f"\n{Cores.AMARELO}Pressione Enter para continuar...{Cores.RESET}")


        elif opcao == "0":
            print(f"{Cores.VERMELHO}👋 Saindo... Até a próxima!{Cores.RESET}")
            time.sleep(1)
            Autenticador.limpar_tela()
            break
        else:
            print(f"{Cores.AMARELO}⚠️ Opção inválida.{Cores.RESET}")
            time.sleep(1)
            Autenticador.limpar_tela()


if __name__ == "__main__":
    main()
