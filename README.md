# 📋 CurricuLLM - Gerador de Currículo com IA

Script que lê seu CV, aplica diretrizes de carreira e gera um novo currículo otimizado usando uma LLM (Large Language Model).

## ⚙️ Configurações para uso (rápido)

### 1. Preparare o ambiente
```bash
pip install -e .
export LLM_API_KEY="sua_chave_aqui"  # linux/mac
# Windows: $env:LLM_API_KEY="sua_chave_aqui"
```

#### Caso tenha problema com o pip install

- A partir de Python 3.11+, não é permitido instalar pacotes diretamente no Python do sistema para evitar que você quebre a instalação do SO
- Recomendo usar um ambiente virtual (venv) para isolar as dependências do projeto
```bash
python -m venv venv

source venv/bin/activate  # linux/mac
# Windows: venv\Scripts\activate 

# e aí, instalar
pip install -e .
```

- Para mais informações, recomendo que acesse esse artigo: https://www.geeksforgeeks.org/python/create-virtual-environment-using-venv-python/


### 2. Converta seu CV em um arquivo HTML
- Se seu CV já estiver em HTML, basta renomear para `profile.html` e colocar na pasta do projeto
- Se estiver em outro formato (Word, PDF, etc), use um conversor online para HTML, ou copie e cole o conteúdo em um editor de texto e salve como HTML. O importante é que o arquivo final seja `profile.html` e esteja na mesma pasta do script.
- O projeto já vem com um exemplo de `profile.html` para você testar, mas o ideal é usar seu próprio CV para obter um resultado personalizado.

### 2. Converta a descrição da vaga para um arquivo JSON
> indico que faça isso para obter o melhor resultado, mas o script também funciona sem personalização (gerando um CV genérico seguindo as diretrizes dos arquivos .md que estão aqui na pasta)
```bash
# Copie o exemplo
cp job_description.example.json job_description.json
```
Depois disso, abra o arquivo `job_description.json` com seu editor de texto preferido, e preencha com os dados reais da vaga que deseja se candidatar. Quanto mais detalhes você fornecer, melhor será a personalização do CV gerado.

### 3. Gere o CV personalizado
```bash
python curriculum.py job_description.json
```

### 📋 Resultado
- Arquivo gerado: `curriculum_gerado.html`
- Agora é abrir esse arquivo no navegador,  avaliar os resultados gerados, ajustar caso preciso, e se estiver tudo ok, convertê-lo (baixando um .pdf da página), e enviá-lo para as vagas que deseja se candidatar! 

---

## ⚙️ Configurações para uso (completo)

### 1️⃣ Instalar dependências

```bash
pip install -e .
```

Ou sem modo desenvolvimento:
```bash
pip install .
```

### 2️⃣ Configurar conexão com LLM

1. Obtenha uma chave de API de um provedor de LLM
2. Copie sua chave para um **local seguro**
3. Exporte a chave como variável de ambiente:
```bash
export LLM_API_KEY="sua_chave_aqui"
```
Ou no Windows (PowerShell):
```powershell
$env:LLM_API_KEY="sua_chave_aqui"
```
> ⚠️ **Atenção:** jamais compartilhe sua chave de API publicamente ou faça commit dela no Git!

### 3️⃣ Executar o gerador

**Opção 1: criar CV básico (sem personalização)**
```bash
python curriculum.py
```

**Opção 2: com descrição simples da vaga (texto puro \[string\] enviado como argumento)**
```bash
python curriculum.py "Senior QA Engineer - automação de testes em Python"
```

**Opção 3: com arquivo JSON completo de descrição da vaga (recomendado)**
```bash
python curriculum.py job_description.json
```

**Opção 4: podendo especificar arquivo de saída**
```bash
python curriculum.py job_description.json "curriculum_customizado.html"
```

## 📁 Estrutura de arquivos do projeto

```
CurricuLLM/
├── curriculum.py                              # Script principal
├── pyproject.toml                             # Configuração e dependências
├── LICENSE                                    # Licença CC-BY-NC 4.0 para o projeto
├── profile.html                               # Seu CV em HTML (original)
├── job_description.example.json               # Exemplo de arquivo de vaga
├── job_description.json                       # Sua vaga (crie a partir do exemplo)
├── generated/                                 # CVs gerados (pasta, não fazer commit)
│   └── curriculum_gerado.html                 # CV gerado (criado automaticamente)
├── guidelines/                                # Diretrizes para criação
│   ├── diretrizes_curriculum.md               # Diretrizes de estrutura
│   └── diretrizes_humanizacao.md              # Diretrizes de tom/estilo
├── .gitignore                                 # Arquivos ignorados pelo Git
└── .env.example                               # Exemplo de variáveis de ambiente
```

> 💡 **Nota**: Os arquivos `.env`, `job_description.json` e a pasta `/generated` estão listados no `.gitignore` para proteger dados sensíveis e não incluir arquivos gerados no repositório.
```

## 🔎 Detalhando o que o script faz

1. **Lê `profile.html`**: extrai seu CV atual
2. **Lê as diretrizes**: carrega regras de formatação e humanização
3. **Conecta à LLM**: envia as informações para gerar um novo CV
4. **Gera novo CV**: geração buscando:
   - Linguagem mais direta e imperativa
   - Destaque de números e resultados
   - Humanização do texto (evita tom de IA)
   - Variação de estrutura (frases curtas e longas)
   - Personalização para vagas (se fornecida)
5. **Salva resultado**: arquivo `curriculum_gerado.html`

## 🔧 Pontos de atenção

### Formato do JSON com a descrição da vaga

O arquivo `job_description.json` deve seguir esta estrutura:

```json
{
  "titulo": "Senior QA Engineer",
  "empresa": "Tech Company",
  "localizacao": "São Paulo, SP",
  "tipo_contrato": "CLT",
  "descricao": "Descrição geral da vaga...",
  "responsabilidades": [
    "Responsabilidade 1",
    "Responsabilidade 2"
  ],
  "requisitos": [
    "Requisito 1",
    "Requisito 2"
  ],
  "diferenciais": [
    "Diferencial 1"
  ],
  "tecnologias": [
    "Python",
    "Pytest",
    "Docker"
  ],
  "beneficios": [
    "Benefício 1"
  ],
  "salario": "R$ 10.000 - R$ 15.000"
}
```
> 💡 Preencha minimamente os campos `titulo`, `descricao`, `requisitos`  

**Referência rápida**:
- `titulo`: nome da posição
- `empresa`: nome da empresa
- `localizacao`: onde fica
- `tipo_contrato`: cLT/PJ/Freelance
- `descricao`: descreva o que a vaga procura
- `responsabilidades`: lista de responsabilidades
- `requisitos`: lista de requisitos
- `diferenciais`: bonus/diferenciais
- `tecnologias`: tecnologias usadas
- `beneficios`: benefícios oferecidos
- `salario`: faixa salarial

### Outra maneira para configurar as variáveis de ambiente

Se preferir outra maneira de usar a chave de API de forma segura, você pode:

1. Criar um arquivo `.env` na pasta do projeto:
```
export LLM_API_KEY="sua_chave_aqui"
```

2. Usar `python-dotenv` para carregr automaticamente (adicione ao `pyproject.toml`):
```bash
pip install python-dotenv
```

- Para mais informações, acesse esse artigo: 

## ⚠️ Importante

- **Segurança**: **nunca** faça commit da chave API no Git
  - ⚠️ Certifique-se de que `.env` e `job_description.json` constam no seu `.gitignore` para não expor dados sensíveis
- **Limite de uso**: a API Gemini tem limite de chamadas gratuitas
- **Qualidade**: sempre revise o CV gerado antes de enviar
- **Personalização**: para **melhores resultados**, use um arquivo JSON com a descrição completa da vaga
  - Inclua: título, empresa, responsabilidades, requisitos, tecnologias, benefícios
  - Veja `job_description.example.json` como referência

## 🐞 Troubleshooting

**Erro: "GEMINI_API_KEY não encontrada"**
- Certifique-se de que a variável de ambiente foi configurada corretamente
- Teste com: `echo $GEMINI_API_KEY` (ou `$env:GEMINI_API_KEY` no Windows)

**Erro: "Arquivo não encontrado"**
- Verifique se `profile.html` existe na mesma pasta
- Verifique se os arquivos .md das diretrizes estão presentes

**Erro: "Arquivo não é um JSON válido"**
- Valide seu JSON em https://jsonlint.com/
- Certifique-se de usar aspas duplas, não simples
- Verifique se não há vírgulas faltando

**Resposta muito genérica do CV**
- Use um arquivo JSON com informações **completas** da vaga
- Quanto mais detalhes sobre responsabilidades e requisitos, melhor a personalização
- Revise e ajuste manualmente o resultado conforme necessário

**CV não contém as keywords da vaga**
- Verifique se as palavras-chave estão escritas exatamente igual no JSON
- O script busca keywords exatas, então "Pytest" é diferente de "pytest"

## 📚 Referências

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Desenvolvido com ❤️ para melhorar sua carreira em tecnologia**