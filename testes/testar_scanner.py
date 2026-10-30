import win32com.client
import pywintypes


def testar_scanner():
    print("=" * 50)
    print("DIAGNÓSTICO DO SCANNER - WIA")
    print("=" * 50)

    try:
        wia = win32com.client.Dispatch("WIA.DeviceManager")

        dispositivos = wia.DeviceInfos

        print(f"\nDispositivos encontrados: {dispositivos.Count}")

        if dispositivos.Count == 0:
            print("\nNenhum scanner foi identificado pela WIA.")
            print("Verifique o driver e a compatibilidade WIA.")
            return

        for indice in range(1, dispositivos.Count + 1):
            dispositivo = dispositivos.Item(indice)

            nome = "Nome não identificado"

            for propriedade in dispositivo.Properties:
                if propriedade.Name == "Name":
                    nome = propriedade.Value
                    break

            print(f"\nDispositivo {indice}: {nome}")

            try:
                print("Tentando conectar...")

                scanner = dispositivo.Connect()

                print("Conexão realizada com sucesso!")

                print("Itens disponíveis:", scanner.Items.Count)

            except pywintypes.com_error as erro:
                print("O dispositivo foi encontrado, mas a conexão falhou.")
                print(f"Detalhes: {erro}")

    except Exception as erro:
        print("\nNão foi possível inicializar a WIA.")
        print(f"Tipo do erro: {type(erro).__name__}")
        print(f"Detalhes: {erro}")


if __name__ == "__main__":
    testar_scanner()