import pandas as pd
import random

def inserir_erros(texto, error = 0.5):
    """Insere erros simulando erros de digitação ou palavras faltando"""
    erros_comuns = [
        lambda t: t.replace(" ", "", 1),  # Remove um espaço no início
        lambda t: t.replace("a", "@", 1),  # Troca 'a' por '@'
        lambda t: t.replace("e", "3", 1),  # Troca 'e' por '3'
        lambda t: t.replace("o", "0", 1),  # Troca 'o' por '0'
        lambda t: t[:-1] if len(t) > 5 else t,  # Remove última letra se for longo
        lambda t: t[:len(t)//2] + t[len(t)//2+1:] if len(t) > 6 else t,  # Remove um caractere do meio
        lambda t: t + random.choice([".", "!", "?", "..."]),  # Adiciona pontuação no final
        lambda t: t.split(" ", 1)[-1] if " " in t else t  # Remove a primeira palavra
    ]
    if random.random() < error:  # 50% de chance de erro
        erro = random.choice(erros_comuns)
        return erro(texto)
    return texto

def gerar_dados_sinteticos(qtd_dados, noise=False, error = 0.5):
    # Listas de ações para cada tipo
    acoes_melhoria = [
        "Instalar ponto de rede",
        "Habilitar ponto de rede",
        "Instalar computadores",
        "Instalar campainha para telefone",
        "Atualizar firmware do roteador",
        "Expandir capacidade de armazenamento",
        "Implementar sistema de backup",
        "Configurar VPN para acesso remoto",
        "Instalar sistema de monitoramento",
        "Melhorar sinal Wi-Fi em áreas específicas",
        "Instalar Campainha"
    ]

    acoes_corretiva = [
        "Computador não está ligando",
        "Campainha está com defeito",
        "Campainha não esta tocando",
        "Cabo de rede com mau contato",
        "Tomadas dos computadores danificadas",
        "Perda de conexão com a internet",
        "Telefone sem sinal",
        "Roteador reiniciando aleatoriamente",
        "Impressora não responde aos comandos",
        "Servidor com desempenho lento",
        "Falha na autenticação de usuários",
        "VPN fora de funcionamento",
        "Rede esta lenta",
        "Internet esta lenta"
    ]

    # Listas de variações para as descrições
    variacoes = [
        "{} no setor administrativo",
        "{} na sala de reuniões",
        "{} no andar térreo",
        "{} para o departamento de TI",
        "{} para novos funcionários",
        "{} devido a atualização recente",
        "{} após queda de energia",
        "{} com prioridade alta",
        "{} solicitada pelo gerente",
        "{} detectada durante inspeção"
    ]

    dados_sinteticos = []

    for _ in range(qtd_dados):
        tipo = random.choice(["melhoria", "corretiva"])
        if tipo == "melhoria":
            acao = random.choice(acoes_melhoria)
        else:
            acao = random.choice(acoes_corretiva)

        variacao = random.choice(variacoes)
        descricao = variacao.format(acao)

        # Adiciona ruído se noise=True
        if noise:
            descricao = inserir_erros(descricao, error)
            # if random.random() > 0.9:
            #     tipo = random.choice(["melhoria", "corretiva"])

        dados_sinteticos.append([descricao, tipo])

    # Criando DataFrame
    df = pd.DataFrame(dados_sinteticos, columns=["Descrição", "Tipo"])
    return df

# Exemplo de uso:
df_dados = gerar_dados_sinteticos(10, noise=True)

