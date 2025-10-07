from sistema_eventos import SistemaEventos

def menu():
    print("\n===== Sistema de Gerenciamento de Eventos =====")
    print("1 - Cadastrar novo evento")
    print("2 - Listar todos os eventos")
    print("3 - Buscar eventos por categoria")
    print("4 - Buscar eventos por data")
    print("5 - Inscrever participante")
    print("6 - Cancelar inscrição")
    print("7 - Fazer check-in de participante")
    print("8 - Relatórios")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def main():
    sistema = SistemaEventos()

    while True:
        try:
            opcao = menu()

            if opcao == "1":
                nome = input("Nome do evento: ").strip()
                data_str = input("Data e hora (dd-mm-YYYY HH:MM): ").strip()
                local = input("Local: ").strip()

                try:
                    capacidade = int(input("Capacidade: "))
                    preco = float(input("Preço: "))
                except ValueError:
                    print("❌ Capacidade e preço devem ser números.")
                    continue

                categoria = input("Categoria: ").strip()
                tipo = input("Tipo (Evento, Palestra, Workshop): ").strip()
                extra = None
                if tipo.lower() == "palestra":
                    extra = input("Palestrante: ").strip()
                elif tipo.lower() == "workshop":
                    extra = input("Material necessário: ").strip()

                sistema.cadastrar_evento(nome, data_str, local, capacidade, categoria, preco, tipo, extra)

            elif opcao == "2":
                sistema.listar_eventos()

            elif opcao == "3":
                categoria = input("Categoria: ").strip()
                sistema.buscar_por_categoria(categoria)

            elif opcao == "4":
                data = input("Data (dd-mm-YYYY): ").strip()
                sistema.buscar_por_data(data)

            elif opcao == "5":
                sistema.listar_eventos()
                try:
                    indice = int(input("Escolha o número do evento: "))
                except ValueError:
                    print("❌ Digite um número válido.")
                    continue
                nome = input("Nome do participante: ").strip()
                email = input("E-mail: ").strip()
                sistema.inscrever_participante(indice, nome, email)

            elif opcao == "6":
                sistema.listar_eventos()
                try:
                    indice = int(input("Escolha o evento: "))
                except ValueError:
                    print("❌ Digite um número válido.")
                    continue
                email = input("E-mail do participante a remover: ").strip()
                sistema.cancelar_inscricao(indice, email)

            elif opcao == "7":
                sistema.listar_eventos()
                try:
                    indice = int(input("Escolha o evento: "))
                except ValueError:
                    print("❌ Digite um número válido.")
                    continue
                email = input("E-mail do participante: ").strip()
                sistema.fazer_checkin(indice, email)

            elif opcao == "8":
                sistema.relatorios()

            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")

        except KeyboardInterrupt:
            print("\nEncerrando o programa...")
            break
        except Exception as e:
            print(f"⚠️ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
