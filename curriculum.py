import os
import json
from bs4 import BeautifulSoup
from openai import OpenAI
from config import Config

SAIDA = "generated/curriculum_gerado.html"

# ======================================
# ===== CONFIGURAÇÃO DA API da LLM =====
# ======================================

# Aqui, resolvi utilizar a classe Config para centralizar a configuração da chave de API, seguindo as melhores práticas de segurança e organização.
# Sobre a LLM: a escolha do modelo "gpt-4o" foi feita pois ele é otimizado para tarefas de compreensão e geração de texto. Mas sinta-se livre para testar a LLM que preferir, basta ajustar o nome do modelo na função de geração.

def configure_llm_api():
    """Configura a API da LLM com a chave de API."""
    
    api_key = Config.LLM_API_KEY
    if not api_key:
        raise ValueError(
            "Variável de ambiente LLM_API_KEY não encontrada. "
            "Configure a chave da API da LLM antes de executar."
        )
    print("👍 Chave API LLM configurada com sucesso.")
    return OpenAI(api_key=api_key)

# ===============================
# ===== LEITURA DE ARQUIVOS =====
# ===============================

def ler_html_cv(caminho_arquivo: str) -> str:
    """Lê o arquivo HTML do CV e extrai o texto."""
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        conteudo_html = f.read()
    
    soup = BeautifulSoup(conteudo_html, "html.parser")
    
    # Remove scripts e styles, para manter só o texto relevante
    for element in soup(["script", "style"]):
        element.decompose()
    
    # Extrai todo o texto
    texto = soup.get_text(separator="\n", strip=True)
    return texto

def ler_diretrizes(caminho_arquivo: str) -> str:
    """Lê um arquivo de diretrizes em markdown."""
    
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return f.read()

def ler_diretrizes_curriculum():
    """Lê as diretrizes de criação de currículo."""
    try:
        return ler_diretrizes("guidelines/diretrizes_curriculum.md")
    except FileNotFoundError:
        print("⚠️  Aviso: Arquivo de diretrizes de currículo não encontrado.")
        return ""

def ler_diretrizes_humanizacao():
    """Lê as diretrizes de humanização."""
    try:
        return ler_diretrizes("guidelines/diretrizes_humanizacao.md")
    except FileNotFoundError:
        print("⚠️  Aviso: Arquivo de diretrizes de humanização não encontrado.")
        return ""

def ler_descricao_vaga_json(caminho_arquivo: str) -> dict:
    """
    Lê a descrição da vaga de um arquivo JSON.

    Args:
        caminho_arquivo: caminho para o arquivo JSON com a descrição
    
    Returns:
        Dicionário contendo os dados da vaga
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Aviso: Arquivo '{caminho_arquivo}' não encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"❌ Erro: Arquivo '{caminho_arquivo}' não é um JSON válido.")
        return {}

def formatar_descricao_vaga(dados_vaga: dict) -> str:
    """
    Formata os dados da vaga em um texto estruturado.
    
    Args:
        dados_vaga: Dicionário com dados da vaga
    
    Returns:
        String formatada com a descrição da vaga
    """
    if not dados_vaga:
        return ""
    
    descricao = ""
    
    # Títulos principais
    if "titulo" in dados_vaga:
        descricao += f"📌 TÍTULO DA VAGA: {dados_vaga['titulo']}\n"
    
    if "empresa" in dados_vaga:
        descricao += f"🏢 EMPRESA: {dados_vaga['empresa']}\n"
    
    if "localizacao" in dados_vaga:
        descricao += f"📍 LOCALIZAÇÃO: {dados_vaga['localizacao']}\n"
    
    if "tipo_contrato" in dados_vaga:
        descricao += f"📋 TIPO: {dados_vaga['tipo_contrato']}\n"
    
    descricao += "\n"
    
    # Descrição
    if "descricao" in dados_vaga:
        descricao += f"📝 DESCRIÇÃO GERAL:\n{dados_vaga['descricao']}\n\n"
    
    # Responsabilidades
    if "responsabilidades" in dados_vaga:
        descricao += "✅ RESPONSABILIDADES:\n"
        if isinstance(dados_vaga["responsabilidades"], list):
            for resp in dados_vaga["responsabilidades"]:
                descricao += f"  • {resp}\n"
        else:
            descricao += f"{dados_vaga['responsabilidades']}\n"
        descricao += "\n"
    
    # Requisitos
    if "requisitos" in dados_vaga:
        descricao += "🎯 REQUISITOS:\n"
        if isinstance(dados_vaga["requisitos"], list):
            for req in dados_vaga["requisitos"]:
                descricao += f"  • {req}\n"
        else:
            descricao += f"{dados_vaga['requisitos']}\n"
        descricao += "\n"
    
    # Diferenciais
    if "diferenciais" in dados_vaga:
        descricao += "⭐ DIFERENCIAIS:\n"
        if isinstance(dados_vaga["diferenciais"], list):
            for diff in dados_vaga["diferenciais"]:
                descricao += f"  • {diff}\n"
        else:
            descricao += f"{dados_vaga['diferenciais']}\n"
        descricao += "\n"
    
    # Tecnologias
    if "tecnologias" in dados_vaga:
        descricao += "🛠️  TECNOLOGIAS:\n"
        if isinstance(dados_vaga["tecnologias"], list):
            descricao += ", ".join(dados_vaga["tecnologias"]) + "\n"
        else:
            descricao += f"{dados_vaga['tecnologias']}\n"
        descricao += "\n"
    
    # Benefícios
    if "beneficios" in dados_vaga:
        descricao += "🎁 BENEFÍCIOS:\n"
        if isinstance(dados_vaga["beneficios"], list):
            for benef in dados_vaga["beneficios"]:
                descricao += f"  • {benef}\n"
        else:
            descricao += f"{dados_vaga['beneficios']}\n"
        descricao += "\n"
    
    # Salário (se houver)
    if "salario" in dados_vaga:
        descricao += f"💰 FAIXA SALARIAL: {dados_vaga['salario']}\n\n"
    
    return descricao

# ================================
# ===== CONSTRUÇÃO DO PROMPT =====
#=================================

def construir_prompt_cv(
    cv_texto: str,
    diretrizes_curriculum: str,
    diretrizes_humanizacao: str,
    vaga_descricao: str = None
) -> str:
    """
    Constrói o prompt para o ChatGPT gerar um CV melhorado.
    
    Args:
        cv_texto: Conteúdo extraído do CV atual
        diretrizes_curriculum: Diretrizes de criação de currículo
        diretrizes_humanizacao: Diretrizes de humanização de texto
        vaga_descricao: (Opcional) Descrição da vaga para personalização
    
    Returns:
        String com o prompt construído
    """
    
    prompt = f"""Você é um especialista em recrutamento e desenvolvimento de carreira. Sua tarefa é reescrever o currículo abaixo, seguindo rigorosamente as diretrizes fornecidas.

{'='*80}
DIRETRIZES DE CRIAÇÃO DE CURRÍCULO:
{'='*80}
{diretrizes_curriculum}

{'='*80}
DIRETRIZES DE HUMANIZAÇÃO DE TEXTO:
{'='*80}
{diretrizes_humanizacao}

{'='*80}
CURRÍCULO ATUAL:
{'='*80}
{cv_texto}

{'='*80}
INSTRUÇÕES:
{'='*80}
1. Reescreva o currículo aplicando TODAS as diretrizes de criação
2. Use imperativo e linguagem direta
3. Destaque números e resultados concretos
4. Aplique as técnicas de humanização para que pareça escrito por uma pessoa
5. Varie estrutura de frases (curtas e longas)
6. Evite vocabulário de IA genérico
7. Mantenha a autenticidade e tons anedóticos quando apropriado
8. **IMPORTANTE**: Se a descrição da vaga foi fornecida, personalize COMPLETAMENTE o currículo para ela:
   - Destaque experiências relevantes para os requisitos mencionados
   - Use keywords EXATAS da descrição da vaga
   - Adapte o resumo profissional para alinhar com o perfil buscado
   - Reorganize a ordem das seções para dar prioridade ao mais relevante
   - Reforce competências técnicas solicitadas
   - Mostre como sua experiência resolve os problemas da vaga

CURRÍCULO REESCRITO (em formato HTML estruturado):
"""
    
    if vaga_descricao:
        prompt += f"\n\n{'='*80}\nDESCRIÇÃO COMPLETA DA VAGA (USE PARA PERSONALIZAR):\n{'='*80}\n{vaga_descricao}\n"
    
    return prompt

# ===========================
# ===== GERAÇÃO COM LLM =====
# ===========================

def gerar_cv_com_llm(prompt: str, client: OpenAI) -> str:
    """
    Envia o prompt para a LLM e retorna o CV gerado.
    
    Args:
        prompt: Prompt construído para o modelo
        client: Cliente OpenAI configurado
    
    Returns:
        String com o CV gerado pela LLM
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em recrutamento e desenvolvimento de carreira. Sua tarefa é reescrever currículos de forma profissional e impactante."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, # aqui, você pode regular a temperatura para controlar a criatividade da resposta (indo de 0 a 1); quanto mais alta, mais criativa, mas menos focada; para um CV, 0.7 é um bom equilíbrio
            max_tokens=4000 # ajuste conforme necessário, dependendo do tamanho esperado do CV gerado; lembre-se que o prompt + resposta não pode ultrapassar o limite de tokens do modelo
        )
        cv_gerado = response.choices[0].message.content
        
        # limpando caso venha o conteúdo em um bloco de código Markdown
        if "```" in cv_gerado:
            partes = cv_gerado.split("```")
            cv_gerado = partes[1]
            
            # Remove identificadores de linguagem (html, markdown, etc) da primeira linha
            linhas = cv_gerado.splitlines()
            if linhas and not linhas[0].strip().startswith("<"):
                cv_gerado = "\n".join(linhas[1:])
        
        return cv_gerado
    except Exception as e:
        print(f"❌ Erro ao comunicar com a API da LLM: {e}")
        raise

# ================================
# ===== SALVANDO O CV GERADO =====
# ================================

def salvar_cv_html(conteudo: str, nome_arquivo: str = SAIDA):
    
    """Salva o CV gerado como arquivo HTML."""
    
    # Garante que o conteúdo tenha estrutura HTML (se não tiver)
    # Você pode ajustar isso dependendo do formato que a LLM retorna, inclusive ajustando as cores e estilos para algo mais direcionado
    
    # Cria o diretório de destino se não existir
    diretorio = os.path.dirname(nome_arquivo)
    if diretorio:
        os.makedirs(diretorio, exist_ok=True)

    if not conteudo.strip().startswith("<!DOCTYPE"):
        conteudo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Curriculum Vitae</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 40px; }}
        h1 {{ margin-bottom: 5px; color: #111; }}
        h2 {{ border-bottom: 2px solid #ccc; padding-bottom: 5px; margin-top: 30px; color: #222; }}
        h3 {{ margin-bottom: 0; color: #444; }}
        p {{ margin-top: 5px; }}
        .subtitle {{ font-size: 1.1em; color: #555; font-weight: bold; }}
        .date-location {{ color: #666; font-style: italic; font-size: 0.9em; }}
        ul {{ margin-top: 5px; padding-left: 20px; }}
        .contact-info ul {{ list-style-type: none; padding: 0; display: flex; gap: 15px; flex-wrap: wrap; }}
    </style>
</head>
<body>
{conteudo}
</body>
</html>"""
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    print(f"✅ CV gerado salvo em: {nome_arquivo}")

# ============================
# ===== FUNÇÃO PRINCIPAL =====
# ============================

def processar_curriculum(
    caminho_cv: str = "profile.html",
    vaga_descricao: str = None,
    arquivo_saida: str = SAIDA
):
    """
    Processa o currículo completo: lê, gera com LLM, e salva.
    
    Args:
        caminho_cv: Caminho do arquivo HTML do CV
        vaga_descricao: (Opcional) Descrição da vaga para personalização
        arquivo_saida: Nome do arquivo de saída
    """
    
    print("🚀 Iniciando processamento do currículo...")
    
    # 1. Configurar API
    print("🔐 Configurando API LLM...")
    client = configure_llm_api()
    
    # 2. Ler arquivos
    print("📖 Lendo currículo atual...")
    cv_texto = ler_html_cv(caminho_cv)
    
    print("📋 Lendo diretrizes...")
    diretrizes_curriculum = ler_diretrizes_curriculum()
    diretrizes_humanizacao = ler_diretrizes_humanizacao()
    
    # 3. Construir prompt
    print("✍️  Construindo prompt para LLM...")
    prompt = construir_prompt_cv(
        cv_texto,
        diretrizes_curriculum,
        diretrizes_humanizacao,
        vaga_descricao
    )
    
    # 4. Gerar com LLM
    print("🤖 Gerando novo currículo com LLM...")
    cv_gerado = gerar_cv_com_llm(prompt, client)
    
    # 5. Salvar resultado
    print("💾 Salvando currículo gerado...")
    salvar_cv_html(cv_gerado, arquivo_saida)
    
    print("\n✨ Processo concluído com sucesso!")
    return cv_gerado

# =====================
# ===== INTERFACE =====
# =====================

if __name__ == "__main__":
    import sys
    
    vaga_descricao = None
    arquivo_saida = SAIDA
    
    # Processar argumentos da linha de comando
    if len(sys.argv) > 1:
        arg_vaga = sys.argv[1]
        
        # Verifica se é um arquivo JSON
        if arg_vaga.endswith('.json') and os.path.exists(arg_vaga):
            print(f"📂 Lendo descrição da vaga de: {arg_vaga}")
            dados_vaga = ler_descricao_vaga_json(arg_vaga)
            if dados_vaga:
                vaga_descricao = formatar_descricao_vaga(dados_vaga)
        else:
            # Trata como string simples
            vaga_descricao = arg_vaga
    
    if len(sys.argv) > 2:
        arquivo_saida = sys.argv[2]
    
    try:
        cv_final = processar_curriculum(
            caminho_cv="profile.html",
            vaga_descricao=vaga_descricao,
            arquivo_saida=arquivo_saida
        )
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
