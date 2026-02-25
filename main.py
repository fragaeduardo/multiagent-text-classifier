from memory.queue_manager import enviar_para_fila

if __name__ == "__main__":
    input_text = input("Digite o texto a ser analisado: ")
    enviar_para_fila(input_text)