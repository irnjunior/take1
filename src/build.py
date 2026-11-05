#!/usr/bin/env python3
"""Monta as páginas do site da Take 1 a partir de src/paginas/*.html.

Uso (na raiz do projeto):
    python3 src/build.py
    npx tailwindcss@3.4 -i ./src/input.css -o ./assets/css/style.css --minify

Cabeçalho, rodapé, metadados, dados estruturados, perguntas frequentes e
sitemap ficam aqui; o miolo de cada página fica em src/paginas/<arquivo>.html.
Marcadores aceitos no miolo: {{P}} (prefixo de caminho), {{FAQ}}, {{CTA}},
{{OUTROS}} (outros serviços), {{WA}} (link do WhatsApp) e {{CLIENTES}}.
"""
import json
import os
import re
from html import escape

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.take01.com.br'
WA_NUM = '5527999848276'
WA = f'https://wa.me/{WA_NUM}'
TEL = '(27) 3256-4561'
TEL_LINK = 'tel:+552732564561'
WHATS = '(27) 99984-8276'
EMAIL = 'take01@take01.com.br'
ENDERECO = 'Rua Quintino Loureiro, 628 – Centro'
CIDADE = 'Aracruz — ES'
MAPA = 'https://www.google.com/maps/search/?api=1&query=Rua+Quintino+Loureiro%2C+628%2C+Centro%2C+Aracruz+-+ES'
INSTAGRAM = 'https://www.instagram.com/take1comunicacao/'
FACEBOOK = 'https://www.facebook.com/Take1Agencia/'


def wa(texto):
    from urllib.parse import quote
    return f'{WA}?text={quote(texto)}'


# --------------------------------------------------------------------------
# Serviços (ordem do menu)
# --------------------------------------------------------------------------
SERVICOS = [
    ('publicidade', 'Publicidade', 'Campanhas, plano de mídia, PDV e ações promocionais.'),
    ('comunicacao-empresarial', 'Comunicação empresarial', 'Comunicação interna, endomarketing e institucional.'),
    ('marketing-digital', 'Marketing digital', 'Redes sociais, conteúdo, tráfego e sites com a Take 1 Lab.'),
    ('design-grafico', 'Editoração e design gráfico', 'Identidade visual, catálogos, revistas e embalagens.'),
    ('videos-de-treinamento', 'Vídeos de treinamento de segurança', 'Normas e procedimentos em vídeos animados.'),
    ('regulamentacao-de-rifas', 'Regulamentação de rifas', 'Autorização de rifas filantrópicas na SPA/MF.'),
]

# --------------------------------------------------------------------------
# Ícones de traço (24x24). Uso no miolo: {{ICONE:nome}} ou {{ICONE:nome|classes}}
# --------------------------------------------------------------------------
ICONES = {
    'megafone': '<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1Z"/><path d="M15 8.5a5 5 0 0 1 0 7M18 6a8.5 8.5 0 0 1 0 12"/>',
    'pessoas': '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="17" cy="9" r="2.4"/><path d="M16.5 13.6c2.6.2 4.5 2 4.5 4.9"/>',
    'pena': '<path d="M12 3 5 10l3 9h8l3-9-7-7Z"/><circle cx="12" cy="11" r="1.6"/><path d="M12 3v6.4M8 19h8"/>',
    'play': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m10 9.5 5 2.5-5 2.5v-5Z"/>',
    'bilhete': '<path d="M4 7h16v3a2 2 0 0 0 0 4v3H4v-3a2 2 0 0 0 0-4V7Z"/><path d="M14 7v10" stroke-dasharray="2 2"/>',
    'balao': '<path d="M4 5h16v11H9l-5 4V5Z"/><path d="M8 9.5h8M8 12.5h5"/>',
    'mapa': '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2Z"/><path d="M9 4v14M15 6v14"/>',
    'lampada': '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2V16h5v-.1c0-.8.4-1.5 1-2A6 6 0 0 0 12 3Z"/>',
    'link': '<path d="M9 15 15 9"/><path d="M10.5 6.5 12 5a4 4 0 0 1 5.7 5.7L16 12.3M8 11.7 6.3 13.3A4 4 0 0 0 12 19l1.5-1.5"/>',
    'fabrica': '<path d="M3 20V10l5 3v-3l5 3V5h4l1 15"/><path d="M2 20h20M14 9h2"/>',
    'escudo': '<path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',
    'alvo': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="0.6"/>',
    'grafico': '<path d="M4 4v16h16"/><path d="m7 15 4-4 3 3 5-6"/>',
    'camadas': '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>',
    'calendario': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'impressora': '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/>',
    'livro': '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5Z"/><path d="M4 19a2 2 0 0 1 2-2h13"/>',
    'infinito': '<path d="M7.5 15.5C5 15.5 3 13.9 3 12s2-3.5 4.5-3.5c3.5 0 5.5 7 9 7 2.5 0 4.5-1.6 4.5-3.5s-2-3.5-4.5-3.5c-3.5 0-5.5 7-9 7Z"/>',
    'checklist': '<path d="M10 6h10M10 12h10M10 18h10"/><path d="m3 6 1.5 1.5L7 5M3 12l1.5 1.5L7 11M3 18l1.5 1.5L7 17"/>',
    'lupa': '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
    'documento': '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5M9 13h7M9 17h7"/>',
    'trofeu': '<path d="M8 4h8v5a4 4 0 0 1-8 0V4Z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M9 21h6M10 17h4"/>',
    'telefone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A17 17 0 0 1 4 5a1 1 0 0 1 1-1Z"/>',
    'email': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'tv': '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8M12 17v4"/>',
    'outdoor': '<rect x="3" y="4" width="18" height="10" rx="1"/><path d="M8 14v7M16 14v7M6 21h4M14 21h4"/>',
    'loja': '<path d="M4 9h16l-1-5H5L4 9Z"/><path d="M5 9v11h14V9M10 20v-6h4v6"/>',
    'presente': '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v9h14v-9M12 8v13M12 8c-2-4-6-4-6-1.5S10 8 12 8Zm0 0c2-4 6-4 6-1.5S14 8 12 8Z"/>',
    'jornal': '<path d="M4 5h13v14a2 2 0 0 0 2 2H6a2 2 0 0 1-2-2V5Z"/><path d="M17 9h3v10a2 2 0 0 1-2 2M7 9h7M7 13h7M7 17h4"/>',
    'apresentacao': '<rect x="3" y="4" width="18" height="12" rx="1"/><path d="M12 16v3M8 21l4-2 4 2M7 12l3-3 3 2 4-4"/>',
    'caminhao': '<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    'camera': '<path d="M4 8h3l2-3h6l2 3h3v11H4V8Z"/><circle cx="12" cy="13" r="3.5"/>',
    'coracao': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z"/>',
    'trafego': '<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    'pagina': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M6.5 6.5h.01M9.5 6.5h.01"/>',
    'codigo': '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    'engrenagem': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9 7 7M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    'carrinho': '<path d="M3 4h2l2.5 11h11L21 7H6"/><circle cx="9" cy="19.5" r="1.5"/><circle cx="17" cy="19.5" r="1.5"/>',
    'caixa': '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>',
    'brilho': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    'microfone': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/>',
    'ajustes': '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
    'predio': '<path d="M4 21V5l8-2v18M12 8l8 2v11M2 21h20M7 8h2M7 12h2M7 16h2M15 13h2M15 17h2"/>',
    'estrela': '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3Z"/>',
    'paleta': '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 1.5-.8 1.5-1.5 0-1.2-1-1.5-1-2.5s.8-1.5 2-1.5H17a4 4 0 0 0 4-4c0-4.7-4-8.5-9-8.5Z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
}


WA_PATH = ('M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Zm0 18.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 4.54 0 8.24 3.7 8.24 8.24 0 4.55-3.7 8.24-8.24 8.24Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.13-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.42h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.28Z')


def icone(nome, cls='h-8 w-8 text-vinho'):
    if nome == 'whatsapp':
        return f'<svg viewBox="0 0 24 24" class="{cls}" aria-hidden="true"><path fill="currentColor" d="{WA_PATH}"/></svg>'
    return (f'<svg viewBox="0 0 24 24" class="{cls}" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONES[nome]}</svg>')


# Ícone de cada item de "O que fazemos" (mesma ordem de SERVICO_DADOS[...]['itens'])
ICONE_ITENS = {
    'publicidade': ['megafone', 'mapa', 'tv', 'outdoor', 'loja', 'presente', 'jornal', 'lampada', 'calendario'],
    'comunicacao-empresarial': ['pessoas', 'mapa', 'camadas', 'escudo', 'apresentacao', 'caminhao', 'livro', 'camera', 'documento', 'play'],
    'marketing-digital': ['alvo', 'coracao', 'documento', 'grafico', 'megafone', 'trafego', 'balao', 'codigo', 'engrenagem', 'pagina', 'carrinho', 'email', 'play', 'brilho'],
    'design-grafico': ['pena', 'email', 'livro', 'livro', 'jornal', 'documento', 'jornal', 'outdoor', 'caixa'],
    'videos-de-treinamento': ['documento', 'brilho', 'camera', 'microfone', 'ajustes', 'play'],
    'regulamentacao-de-rifas': ['pessoas', 'predio', 'estrela', 'trofeu', 'paleta', 'coracao'],
}

ICONE_SERVICO = {'publicidade': 'megafone', 'comunicacao-empresarial': 'pessoas', 'marketing-digital': 'balao',
                 'design-grafico': 'pena', 'videos-de-treinamento': 'play', 'regulamentacao-de-rifas': 'bilhete'}
ICONE_PILAR = {'publicidade': ['mapa', 'lampada', 'link'],
               'comunicacao-empresarial': ['fabrica', 'pessoas', 'escudo'],
               'marketing-digital': ['alvo', 'balao', 'grafico'],
               'design-grafico': ['camadas', 'calendario', 'impressora'],
               'videos-de-treinamento': ['livro', 'infinito', 'checklist']}


# --------------------------------------------------------------------------
# Perguntas frequentes (alimentam o HTML e o JSON-LD)
# --------------------------------------------------------------------------
FAQ = {
    'inicio': [
        ('Quais serviços a Take 1 oferece?',
         'Publicidade, comunicação empresarial e endomarketing, marketing digital com a Take 1 Lab (redes sociais, conteúdo, tráfego pago, sites e e-commerce), vídeos animados de treinamento de segurança, editoração e design gráfico, além da regulamentação de rifas filantrópicas na SPA/MF.'),
        ('Posso contratar apenas um serviço, como um site ou um catálogo?',
         'Sim. As frentes da Take 1 funcionam de forma integrada, mas também podem ser contratadas separadamente para uma entrega pontual, como um site, uma campanha, um catálogo ou uma identidade visual.'),
        ('A Take 1 atende empresas de todo o Brasil?',
         'Sim. Atendemos empresas e instituições de todo o Brasil, com reuniões on-line e entregas digitais, e também presencialmente quando o projeto pede.'),
    ],
    'publicidade': [
        ('A Take 1 faz o plano de mídia da campanha?',
         'Sim. Planejamos a campanha, definimos o plano de mídia e cuidamos da execução, de acordo com a realidade do seu investimento.'),
        ('Vocês produzem material para ponto de venda?',
         'Sim. Criamos material para PDV, peças para mídia impressa e externa e ações promocionais integradas à campanha.'),
        ('A Take 1 cria campanhas para eventos?',
         'Sim. Criamos campanhas para eventos empresariais, sociais e culturais, da identidade do evento às peças de divulgação.'),
    ],
    'comunicacao-empresarial': [
        ('O que é endomarketing?',
         'É a comunicação voltada ao público interno da empresa. Campanhas de segurança, de qualidade de vida e de ambiente de trabalho, informativos e eventos internos aproximam a empresa dos colaboradores e reforçam a cultura e as metas do negócio.'),
        ('A Take 1 cria o manual de identidade visual da empresa?',
         'Sim. Desenvolvemos o manual de identidade visual e aplicamos a marca de forma consistente em apresentações, catálogos, frota, sinalização e materiais institucionais.'),
        ('Vocês fazem vídeo institucional e de treinamento?',
         'Sim. Produzimos vídeos institucionais, promocionais, de segurança e de treinamento, inclusive vídeos animados que transformam normas e procedimentos em orientações claras.'),
    ],
    'marketing-digital': [
        ('A Take 1 faz a gestão das redes sociais da minha empresa?',
         'Sim. Pela Take 1 Lab, nossa agência digital, criamos e gerenciamos as redes sociais da sua empresa: planejamento estratégico, produção de conteúdo, anúncios e acompanhamento das métricas, para fortalecer a sua marca e aproximá-la de clientes e futuros clientes.'),
        ('A Take 1 ajuda a vender pelo WhatsApp?',
         'Sim. Configuramos o WhatsApp Business da sua empresa com horários de atendimento, catálogo digital e mensagens automáticas, para transformar o aplicativo numa ferramenta de vendas mais profissional.'),
        ('Vocês criam sites e lojas virtuais?',
         'Sim. Desenvolvemos sites, hotsites, landing pages e e-commerce, e cuidamos da manutenção e da otimização depois da publicação.'),
    ],
    'design-grafico': [
        ('A Take 1 cria logomarca?',
         'Sim. Criamos a logomarca e a papelaria da sua empresa e aplicamos a identidade visual em todos os materiais.'),
        ('Vocês fazem a editoração de livros e revistas?',
         'Sim. Fazemos a editoração e o projeto gráfico de publicações periódicas e não periódicas, como livros, revistas, jornais, informativos e catálogos.'),
    ],
    'videos-de-treinamento': [
        ('Como funcionam os vídeos de treinamento de segurança?',
         'Transformamos as normas e os procedimentos de segurança da sua empresa em vídeos animados, ou híbridos com imagens reais e cartelas, claros e padronizados. Fazemos todas as etapas, do roteiro à pós-produção, e entregamos o vídeo pronto para usar quantas vezes for preciso, sem depender de uma equipe dedicada para aplicar o treinamento.'),
        ('Qual a diferença entre o vídeo animado e o híbrido?',
         'O vídeo animado é todo feito em animação. O híbrido une imagens reais da sua operação, animação e cartelas, aproximando o conteúdo da rotina do colaborador.'),
    ],
    'regulamentacao-de-rifas': [
        ('Rifa filantrópica precisa de autorização?',
         'Sim. A rifa com prêmio de entidade sem fins lucrativos é prevista na Lei 5.768/1971 e regulamentada pelo Decreto 70.951/1972, e precisa de autorização prévia da Secretaria de Prêmios e Apostas do Ministério da Fazenda (SPA/MF). Distribuir prêmios sem essa autorização expõe quem promove à multa e à suspensão da rifa.'),
        ('Com quanto tempo de antecedência devo pedir a autorização da rifa?',
         'O pedido é feito à SPA/MF pelo SCPC com prazo mínimo de 40 dias antes do início da campanha. Por isso, o ideal é começar o diagnóstico com a Take 1 assim que a rifa for planejada.'),
        ('Posso divulgar a rifa antes da autorização?',
         'Não. A divulgação começa depois da emissão do Certificado de Autorização. A partir daí, a Take 1 também pode cuidar da divulgação e do marketing da campanha.'),
        ('Quem pode fazer uma rifa autorizada?',
         'Entidades sem fins lucrativos formalmente constituídas e enquadradas na Lei 5.768/1971, como associações, fundações e instituições religiosas, esportivas, culturais ou assistenciais. A origem dos prêmios precisa ser comprovada, em geral por doação de terceiros formalizada.'),
    ],
}

# --------------------------------------------------------------------------
# Páginas
# --------------------------------------------------------------------------
PAGINAS = [
    dict(arquivo='inicio', caminho='', nome='Início',
         titulo='Take 1 Comunicação | Agência de Publicidade, Comunicação Integrada e Marketing Digital',
         descricao='Agência de publicidade e comunicação integrada desde 1997, com atendimento em todo o Brasil: campanhas publicitárias, comunicação empresarial, vídeos animados de treinamento de segurança, marketing digital, criação de sites e design gráfico.'),
    dict(arquivo='quem-somos', caminho='quem-somos/', nome='Quem somos',
         titulo='Quem somos | Take 1 Comunicação Integrada, desde 1997',
         descricao='Conheça a Take 1: agência de comunicação integrada criada em 1997 por profissionais com mais de 15 anos na comunicação corporativa da Aracruz Celulose.'),
    dict(arquivo='publicidade', caminho='publicidade/', nome='Publicidade', servico=True,
         titulo='Agência de Publicidade | Campanhas, Plano de Mídia e PDV | Take 1',
         descricao='Campanhas publicitárias institucionais e promocionais, plano de mídia, peças para mídia impressa e externa, material para PDV e ações promocionais.'),
    dict(arquivo='comunicacao-empresarial', caminho='comunicacao-empresarial/', nome='Comunicação empresarial', servico=True,
         titulo='Comunicação Empresarial e Endomarketing | Take 1',
         descricao='Comunicação interna, endomarketing, comunicação institucional, manual de identidade visual, campanhas de segurança e vídeos institucionais para empresas.'),
    dict(arquivo='marketing-digital', caminho='marketing-digital/', nome='Marketing digital', servico=True,
         titulo='Marketing Digital e Gestão de Redes Sociais | Take 1 Lab',
         descricao='A Take 1 Lab cria e gerencia as redes sociais da sua empresa: conteúdo, tráfego pago, métricas, WhatsApp Business, sites, landing pages e e-commerce.'),
    dict(arquivo='design-grafico', caminho='design-grafico/', nome='Editoração e design gráfico', servico=True,
         titulo='Editoração e Design Gráfico | Logomarca, Catálogo e Revista | Take 1',
         descricao='Criação de logomarca, papelaria, catálogos, livros, revistas, jornais, folders, banners e embalagens com a identidade visual da sua empresa.'),
    dict(arquivo='videos-de-treinamento', caminho='videos-de-treinamento/', nome='Vídeos de treinamento de segurança', servico=True,
         titulo='Vídeos Animados de Treinamento de Segurança | Take 1',
         descricao='Normas e procedimentos de segurança em vídeos animados e híbridos, claros e padronizados. Do roteiro à pós-produção, prontos para usar sempre.'),
    dict(arquivo='regulamentacao-de-rifas', caminho='regulamentacao-de-rifas/', nome='Regulamentação de rifas', servico=True,
         titulo='Regulamentação de Rifa Filantrópica na SPA/MF | Take 1',
         descricao='Autorização de rifas filantrópicas na SPA/MF para entidades sem fins lucrativos: regulamento, plano de operação, protocolo no SCPC e prestação de contas.'),
    dict(arquivo='clientes', caminho='clientes/', nome='Clientes',
         titulo='Clientes | Take 1 Comunicação',
         descricao='Indústrias, construtoras, instituições de ensino, comércio e serviços que confiam na comunicação da Take 1.'),
    dict(arquivo='fale-conosco', caminho='fale-conosco/', nome='Fale conosco',
         titulo='Fale Conosco | Take 1 Comunicação',
         descricao='Fale com a Take 1 pelo WhatsApp (27) 99984-8276, telefone (27) 3256-4561 ou e-mail. Atendimento de segunda a sexta-feira, das 8h às 18h.'),
]

CLIENTES = [
    ('imetame.jpg', 'Imetame'), ('jsl.png', 'JSL'), ('faacz.jpg', 'FAACZ'), ('aracruz.jpg', 'Aracruz'),
    ('metalvix.jpg', 'Metalvix'), ('pneuvix.png', 'Pneuvix'), ('oriundi-supermercados.png', 'Oriundi Supermercados'),
    ('estel.jpg', 'Estel'), ('plamont.jpg', 'Plamont'), ('fortanks.png', 'Fortanks'), ('medcor.jpg', 'Medcor'),
    ('edificar.png', 'Edificar'), ('apoio-engenharia.png', 'Apoio Engenharia'), ('rid-metalmecanica.jpg', 'RID Metalmecânica'),
    ('logica-automacao.jpg', 'Lógica Automação'), ('qualiar.png', 'Qualiar'), ('alpbras.png', 'Alpbras'),
    ('quartgran.png', 'Quartgran'), ('pimacol.png', 'Pimacol'), ('fetransportes.jpg', 'FE Transportes'),
    ('gc-brasil.jpg', 'GC Brasil'), ('devens.jpg', 'Devens'), ('tesselaris.png', 'Tesselaris'), ('face-faculdade.jpg', 'FACE Faculdade'),
    ('acricel.jpg', 'Acricel'), ('agroelite.jpg', 'Agroelite'), ('aguape.jpg', 'Aguapé'), ('amazonia.png', 'Amazônia'),
    ('amear.png', 'Amear'), ('amigos-da-terra.png', 'Amigos da Terra'), ('beija-flor.jpg', 'Beija-Flor'),
    ('cacha-mel.png', 'Cacha Mel'), ('casa-do-estudante.jpg', 'Casa do Estudante'), ('cidade-jardim.png', 'Cidade Jardim'),
    ('contrex.png', 'Contrex'), ('doradinha.png', 'Doradinha'), ('douradinha.png', 'Douradinha'), ('espaco-livre.png', 'Espaço Livre'),
    ('fortes.jpg', 'Fortes'), ('giongo.png', 'Giongo'), ('kakoa.png', 'Kakoa'), ('loserv.png', 'Loserv'),
    ('lumine.png', 'Lumine'), ('m-locacoes.png', 'M Locações'), ('pollomag.png', 'Pollomag'), ('rampineli.png', 'Rampineli'),
    ('ravenna.jpg', 'Ravenna'), ('redux.png', 'Redux'), ('residencial-alegria.png', 'Residencial Alegria'),
    ('residencial-felicidade.png', 'Residencial Felicidade'), ('sitiosantajoana.png', 'Sítio Santa Joana'),
    ('speed.png', 'Speed'), ('studio-g.png', 'Studio G'), ('thonson-lab.jpg', 'Thonson Lab'),
]


# --------------------------------------------------------------------------
# Componentes
# --------------------------------------------------------------------------
def org_jsonld():
    return {
        '@type': ['AdvertisingAgency', 'LocalBusiness'],
        '@id': f'{SITE}/#empresa',
        'name': 'Take 1 Comunicação Integrada',
        'legalName': 'Take 1 Publicidade Propaganda e Marketing Ltda',
        'taxID': '01.915.175/0001-91',
        'alternateName': ['Take 1 Comunicação', 'Take01', 'Take 1 Lab'],
        'url': f'{SITE}/',
        'logo': f'{SITE}/assets/img/logo-take1.png',
        'image': f'{SITE}/assets/img/logo-take1.png',
        'foundingDate': '1997',
        'description': 'Agência de publicidade e comunicação integrada com atendimento em todo o Brasil.',
        'telephone': '+55-27-3256-4561',
        'email': EMAIL,
        'address': {'@type': 'PostalAddress', 'streetAddress': ENDERECO, 'addressLocality': 'Aracruz',
                    'addressRegion': 'ES', 'addressCountry': 'BR'},
        'areaServed': {'@type': 'Country', 'name': 'Brasil'},
        'openingHoursSpecification': {'@type': 'OpeningHoursSpecification',
                                      'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                      'opens': '08:00', 'closes': '18:00'},
        'sameAs': [INSTAGRAM, FACEBOOK],
    }


def jsonld(pg):
    url = f"{SITE}/{pg['caminho']}"
    grafo = [org_jsonld(),
             {'@type': 'WebPage', '@id': url, 'url': url, 'name': pg['titulo'], 'description': pg['descricao'],
              'inLanguage': 'pt-BR', 'isPartOf': {'@type': 'WebSite', 'url': f'{SITE}/', 'name': 'Take 1 Comunicação'}}]
    if pg['caminho']:
        grafo.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': f'{SITE}/'},
            {'@type': 'ListItem', 'position': 2, 'name': pg['nome'], 'item': url}]})
    if pg.get('servico'):
        grafo.append({'@type': 'Service', 'name': pg['nome'], 'description': pg['descricao'], 'url': url,
                      'provider': {'@id': f'{SITE}/#empresa'}, 'areaServed': {'@type': 'Country', 'name': 'Brasil'}})
    if FAQ.get(pg['arquivo']):
        grafo.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
            for q, a in FAQ[pg['arquivo']]]})
    dados = json.dumps({'@context': 'https://schema.org', '@graph': grafo}, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{dados}\n</script>'


def head(pg, P):
    url = f"{SITE}/{pg['caminho']}"
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>document.documentElement.classList.add('js')</script>

  <title>{escape(pg['titulo'])}</title>
  <meta name="description" content="{escape(pg['descricao'])}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#aa2845">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Take 1 Comunicação">
  <meta property="og:title" content="{escape(pg['titulo'])}">
  <meta property="og:description" content="{escape(pg['descricao'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/logo-take1.png">
  <meta name="twitter:card" content="summary">

  <link rel="icon" type="image/png" href="{P}assets/img/favicon.png">
  <link rel="apple-touch-icon" href="{P}assets/img/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400;1,9..144,500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{P}assets/css/style.css">

{jsonld(pg)}
</head>
<body id="topo">
  <a href="#conteudo" class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] focus:rounded-full focus:bg-vinho focus:px-5 focus:py-3 focus:text-white">Pular para o conteúdo</a>
'''


def link_nav(P, caminho, rotulo, atual):
    ativo = ' aria-current="page"' if caminho == atual else ''
    return f'<li><a href="{P}{caminho}" class="nav-link block py-3 lg:py-2"{ativo}>{rotulo}</a></li>'


def header(pg, P):
    atual = pg['caminho']
    serv_ativo = ' text-vinho' if pg.get('servico') else ''
    itens = '\n'.join(
        f'''              <li><a href="{P}{s}/" class="block rounded-xl px-3 py-2.5 transition hover:bg-vinho-50"{' aria-current="page"' if atual == s + '/' else ''}>
                <span class="block text-sm font-semibold text-tinta">{n}</span>
                <span class="hidden text-xs text-nevoa lg:block">{d}</span></a></li>'''
        for s, n, d in SERVICOS)
    return f'''
  <header class="fixed inset-x-0 top-0 z-50 transition-all duration-300" data-header>
    <div class="container-site flex h-20 items-center justify-between gap-6">
      <a href="{P or './'}" class="shrink-0" aria-label="Take 1 Comunicação — página inicial">
        <img src="{P}assets/img/logo-take1.png" alt="Take 1 Comunicação Integrada" width="222" height="108" class="h-12 w-auto sm:h-14">
      </a>

      <nav id="menu" aria-label="Menu principal"
           class="fixed inset-x-0 top-20 hidden max-h-[calc(100vh-5rem)] flex-col gap-1 overflow-y-auto border-t border-tinta/10 bg-marfim px-4 pb-8 pt-4 shadow-xl lg:static lg:flex lg:max-h-none lg:flex-row lg:items-center lg:gap-8 lg:overflow-visible lg:border-0 lg:bg-transparent lg:p-0 lg:shadow-none">
        <ul class="flex flex-col lg:flex-row lg:items-center lg:gap-8">
          {link_nav(P, 'quem-somos/', 'Quem somos', atual)}
          <li class="group relative">
            <button type="button" class="nav-link flex w-full items-center justify-between gap-1.5 py-3 lg:w-auto lg:py-2{serv_ativo}" aria-haspopup="true">
              Serviços
              <svg viewBox="0 0 20 20" class="h-4 w-4 transition group-hover:rotate-180 group-focus-within:rotate-180" fill="currentColor" aria-hidden="true"><path d="M5.3 7.3a1 1 0 0 1 1.4 0L10 10.6l3.3-3.3a1 1 0 1 1 1.4 1.4l-4 4a1 1 0 0 1-1.4 0l-4-4a1 1 0 0 1 0-1.4Z"/></svg>
            </button>
            <ul class="mb-2 border-l border-tinta/10 pl-3 lg:invisible lg:absolute lg:left-1/2 lg:top-full lg:mb-0 lg:w-80 lg:-translate-x-1/2 lg:translate-y-2 lg:rounded-2xl lg:border lg:border-tinta/10 lg:bg-white lg:p-2 lg:opacity-0 lg:shadow-2xl lg:shadow-tinta/10 lg:transition lg:duration-200 lg:group-hover:visible lg:group-hover:translate-y-0 lg:group-hover:opacity-100 lg:group-focus-within:visible lg:group-focus-within:translate-y-0 lg:group-focus-within:opacity-100">
{itens}
            </ul>
          </li>
          {link_nav(P, 'clientes/', 'Clientes', atual)}
          {link_nav(P, 'fale-conosco/', 'Contato', atual)}
        </ul>
        <a href="{wa('Olá! Vim pelo site da Take 1.')}" target="_blank" rel="noopener" class="btn-primario mt-4 lg:mt-0 lg:px-5 lg:py-2.5">{icone('whatsapp', 'h-5 w-5')}Vamos conversar</a>
      </nav>

      <button type="button" class="relative flex h-12 w-12 items-center justify-center rounded-full bg-vinho shadow-lg shadow-vinho/25 lg:hidden"
              aria-controls="menu" aria-expanded="false" aria-label="Abrir menu" data-menu-toggle>
        <span class="absolute h-0.5 w-5 -translate-y-1 rounded-full bg-white transition" data-bar-1></span>
        <span class="absolute h-0.5 w-5 translate-y-1 rounded-full bg-white transition" data-bar-2></span>
      </button>
    </div>
  </header>
'''


def footer(P):
    servs = '\n'.join(f'          <li><a href="{P}{s}/" class="hover:text-white">{n}</a></li>' for s, n, _ in SERVICOS)
    return f'''
  <footer class="bg-tinta pt-20 text-sm text-white/85">
    <div class="container-site grid grid-cols-2 gap-x-6 gap-y-12 pb-16 lg:grid-cols-12">
      <div class="col-span-2 lg:col-span-4">
        <img src="{P}assets/img/logo-take1.png" alt="Take 1 Comunicação Integrada" width="222" height="108" class="logo-claro h-14 w-auto" loading="lazy">
        <p class="mt-6 max-w-xs leading-relaxed">Agência de publicidade e comunicação integrada desde 1997, com atendimento em todo o Brasil.</p>
        <p class="mt-4">CNPJ 01.915.175/0001-91</p>
      </div>
      <nav class="lg:col-span-3" aria-label="Serviços">
        <p class="mb-4 text-xs font-semibold uppercase tracking-eyebrow text-white">Serviços</p>
        <ul class="space-y-2.5">
{servs}
        </ul>
      </nav>
      <nav class="lg:col-span-2" aria-label="Institucional">
        <p class="mb-4 text-xs font-semibold uppercase tracking-eyebrow text-white">Take 1</p>
        <ul class="space-y-2.5">
          <li><a href="{P or './'}" class="hover:text-white">Início</a></li>
          <li><a href="{P}quem-somos/" class="hover:text-white">Quem somos</a></li>
          <li><a href="{P}clientes/" class="hover:text-white">Clientes</a></li>
          <li><a href="{P}fale-conosco/" class="hover:text-white">Fale conosco</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener" class="hover:text-white">Instagram</a></li>
          <li><a href="{FACEBOOK}" target="_blank" rel="noopener" class="hover:text-white">Facebook</a></li>
        </ul>
      </nav>
      <div class="col-span-2 lg:col-span-3">
        <p class="mb-4 text-xs font-semibold uppercase tracking-eyebrow text-white">Contato</p>
        <ul class="space-y-2.5">
          <li><a href="{WA}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 hover:text-white">{icone('whatsapp', 'h-[1.1rem] w-[1.1rem] shrink-0')}WhatsApp {WHATS}</a></li>
          <li><a href="{TEL_LINK}" class="hover:text-white">Telefone {TEL}</a></li>
          <li><a href="mailto:{EMAIL}" class="hover:text-white">{EMAIL}</a></li>
          <li>{ENDERECO}<br>{CIDADE}</li>
          <li>Seg. a sex., das 8h às 18h</li>
        </ul>
      </div>
    </div>
    <div class="container-site flex flex-col gap-3 border-t border-white/10 py-8 text-xs sm:flex-row sm:items-center sm:justify-between">
      <p>© <span data-ano>2026</span> Take 1 Comunicação Integrada. Todos os direitos reservados.</p>
      <a href="#topo" class="hover:text-white">Voltar ao topo ↑</a>
    </div>
  </footer>

  <a href="{WA}" target="_blank" rel="noopener" aria-label="Conversar pelo WhatsApp"
     class="fixed bottom-5 right-5 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-vinho text-white shadow-xl shadow-vinho/30 transition hover:scale-105 hover:bg-vinho-600">
    {icone('whatsapp', 'h-7 w-7')}
  </a>

  <script src="{P}assets/js/main.js" defer></script>
</body>
</html>
'''


def bloco_faq(chave, titulo='Perguntas frequentes'):
    itens = '\n'.join(f'''          <details class="faq-item revelar">
            <summary>{q}</summary>
            <p class="pb-6 leading-relaxed">{a}</p>
          </details>''' for q, a in FAQ[chave])
    return f'''    <section class="bg-areia py-24 lg:py-28" aria-labelledby="faq-titulo">
      <div class="container-site grid gap-12 lg:grid-cols-12 lg:gap-16">
        <div class="lg:col-span-5">
          <p class="eyebrow">{titulo}</p>
          <h2 id="faq-titulo" class="titulo-secao revelar">Dúvidas <em>frequentes</em>.</h2>
        </div>
        <div class="divide-y divide-tinta/10 border-y border-tinta/10 lg:col-span-7">
{itens}
        </div>
      </div>
    </section>'''


def bloco_cta(texto_wa='Olá! Vim pelo site da Take 1.'):
    return f'''    <section class="relative overflow-hidden bg-vinho-800 py-20 text-white lg:py-24" aria-labelledby="cta-titulo">
      <img src="{{{{P}}}}assets/img/espiral-clara.svg" alt="" aria-hidden="true"
           class="pointer-events-none absolute -right-60 top-1/2 w-[44rem] max-w-none -translate-y-1/2 opacity-[0.07]">
      <div class="container-site relative grid items-center gap-10 lg:grid-cols-12">
        <div class="lg:col-span-6">
          <p class="eyebrow text-vinho-200">Fale conosco</p>
          <h2 id="cta-titulo" class="revelar text-4xl font-normal leading-none tracking-tight text-white sm:text-5xl lg:text-6xl">
            Vamos levar <em class="text-vinho-200">um papo?</em>
          </h2>
          <p class="revelar mt-5 max-w-md text-lg text-white/85">Conte o que a sua marca precisa. Atendemos de segunda a sexta-feira, das 8h às 18h.</p>
        </div>
        <div class="revelar flex flex-col gap-3 sm:flex-row lg:col-span-6 lg:justify-end">
          <a href="{wa(texto_wa)}" target="_blank" rel="noopener" class="btn-claro">{icone('whatsapp', 'h-5 w-5')}WhatsApp {WHATS}</a>
          <a href="{TEL_LINK}" class="btn-vazado">{icone('telefone', 'h-5 w-5')}Ligar {TEL}</a>
        </div>
      </div>
    </section>'''


def bloco_outros(atual):
    cards = '\n'.join(f'''          <li><a href="{{{{P}}}}{s}/" class="group flex h-full flex-col justify-between gap-6 rounded-3xl border border-tinta/10 bg-white/60 p-6 transition hover:-translate-y-0.5 hover:border-vinho/40 hover:bg-white">
            <span>{icone(ICONE_SERVICO[s], 'h-7 w-7 text-vinho')}<span class="mt-5 block font-display text-xl text-tinta">{n}</span><span class="mt-2 block text-sm text-nevoa">{d}</span></span>
            <span class="text-sm font-semibold text-vinho">Saiba mais <span aria-hidden="true" class="inline-block transition group-hover:translate-x-1">→</span></span></a></li>'''
                      for s, n, d in SERVICOS if s != atual)
    return f'''    <section class="py-20 lg:py-24" aria-labelledby="outros-titulo">
      <div class="container-site">
        <p class="eyebrow">Comunicação integrada</p>
        <h2 id="outros-titulo" class="titulo-secao revelar max-w-2xl">Conheça os <em>outros serviços</em>.</h2>
        <ul class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
{cards}
        </ul>
      </div>
    </section>'''


def bloco_clientes(lista):
    return '\n'.join(f'          <li class="logo-cliente flex h-28 items-center justify-center bg-white p-6"><img src="{{{{P}}}}assets/img/clientes/{f}" alt="{n}" loading="lazy"></li>'
                     for f, n in lista)


# --------------------------------------------------------------------------
# Conteúdo das páginas de serviço (modelo único)
# --------------------------------------------------------------------------
VIDEO_MOCK = """<figure class="revelar quadro text-vinho" aria-hidden="true">
          <div class="relative aspect-video overflow-hidden rounded-sm bg-gradient-to-br from-vinho via-vinho-700 to-vinho-900">
            <img src="{{P}}assets/img/espiral-clara.svg" alt="" class="absolute -right-24 -top-24 w-96 opacity-10">
            <span class="absolute left-5 top-5 rounded-full bg-black/25 px-3 py-1.5 text-xs font-semibold uppercase tracking-eyebrow text-white/90">Procedimento 03 · Uso de EPI</span>
            <svg viewBox="0 0 120 80" class="absolute left-1/2 top-[42%] w-[26%] -translate-x-1/2 -translate-y-1/2 text-white/90" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 58c0-22 16-40 38-40s38 18 38 40"/>
              <path d="M14 58h92a4 4 0 0 1 4 4v4a4 4 0 0 1-4 4H14a4 4 0 0 1-4-4v-4a4 4 0 0 1 4-4Z"/>
              <path d="M60 18v-8M48 20l4 22M72 20l-4 22"/>
            </svg>
            <span class="absolute left-1/2 top-[68%] -translate-x-1/2 -translate-y-1/2 whitespace-nowrap font-display text-lg text-white sm:text-2xl">Capacete sempre ajustado.</span>
            <div class="absolute inset-x-4 bottom-4 flex items-center gap-3 text-white sm:inset-x-5 sm:bottom-5">
              <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-white text-vinho">
                <svg viewBox="0 0 24 24" class="ml-0.5 h-4 w-4" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
              </span>
              <span class="relative h-1 flex-1 rounded-full bg-white/25"><span class="absolute inset-y-0 left-0 w-[38%] rounded-full bg-white"></span></span>
              <span class="text-xs tabular-nums text-white/85">01:12 / 03:05</span>
            </div>
          </div>
        </figure>"""

RIFAS_EXTRA = """    <section class="relative overflow-hidden bg-tinta py-24 text-white lg:py-32" aria-labelledby="etapas-titulo">
      <div class="pointer-events-none absolute -right-40 -top-40 h-[30rem] w-[30rem] rounded-full bg-vinho/30 blur-[120px]"></div>
      <div class="container-site relative">
        <div class="grid gap-10 lg:grid-cols-12 lg:gap-16">
          <div class="lg:col-span-6">
            <p class="eyebrow text-vinho-300"><span class="cena">02</span>Como funciona</p>
            <h2 id="etapas-titulo" class="titulo-secao revelar text-white">Do diagnóstico à <em class="text-vinho-300">prestação de contas</em>.</h2>
          </div>
          <p class="revelar rounded-2xl border border-vinho-300/30 bg-vinho/20 p-6 leading-relaxed text-white/90 lg:col-span-6 lg:self-end">
            <strong class="text-white">Atenção:</strong> distribuir prêmios sem a autorização prévia da SPA/MF expõe quem promove
            à multa e à suspensão da rifa. Regulamento, plano de operação, protocolo no SCPC e exigências da Secretaria:
            um erro pode custar semanas.
          </p>
        </div>

        <div class="mt-14 flex flex-wrap items-center gap-6 text-sm text-white/80">
          <span class="flex items-center gap-2"><span class="h-3 w-3 rounded-full bg-vinho-300"></span>Etapa feita pela Take 1</span>
          <span class="flex items-center gap-2"><span class="h-3 w-3 rounded-full border border-white/70"></span>Etapa feita pela Plataforma Rifa</span>
        </div>

        <ol class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
""" + "\n".join(f"""          <li class="revelar rounded-3xl border {'border-white/15 bg-white/[0.05]' if take else 'border-dashed border-white/25'} p-7">
            <div class="flex items-center justify-between">
              <span class="font-display text-3xl font-normal {'text-vinho-300' if take else 'text-white/85'}">{n}</span>
              <span class="flex items-center gap-3">{icone(ic, 'h-7 w-7 ' + ('text-vinho-300' if take else 'text-white/80'))}<span class="h-3 w-3 rounded-full {'bg-vinho-300' if take else 'border border-white/70'}"></span></span>
            </div>
            <h3 class="mt-6 text-2xl text-white">{tt}</h3>
            <p class="mt-3 text-white/85">{d}</p>
          </li>""" for n, take, ic, tt, d in [
    ('01', True, 'lupa', 'Diagnóstico', 'Análise do enquadramento: quem promove, a finalidade da rifa e os prêmios oferecidos.'),
    ('02', True, 'documento', 'Regulamento e plano de operação', 'Documentos elaborados com os critérios de apuração da Plataforma Rifa.'),
    ('03', True, 'escudo', 'Autorização na SPA/MF', 'Protocolo no SCPC, acompanhamento e respostas às exigências até o Certificado de Autorização.'),
    ('04', False, 'bilhete', 'Venda dos bilhetes', 'Site da rifa com Pix e cartão, repasse vinculado ao CPF/CNPJ e painel em tempo real.'),
    ('05', False, 'trofeu', 'Apuração pela Loteria Federal', 'Resultado oficial consultado e aplicado automaticamente, com transparência.'),
    ('06', True, 'grafico', 'Prestação de contas', 'Encerramento junto à SPA/MF com os relatórios gerados pela plataforma.'),
]) + """
        </ol>

        <div class="mt-12 grid gap-5 lg:grid-cols-2">
          <div class="revelar rounded-3xl border border-white/15 p-8">
            <h3 class="text-2xl text-white">Divulgação e marketing da sua rifa</h3>
            <p class="mt-3 leading-relaxed text-white/80">Com o Certificado de Autorização emitido, a Take 1 também planeja e executa a divulgação: identidade da campanha, peças para redes sociais, anúncios e materiais impressos.</p>
          </div>
          <div class="revelar rounded-3xl border border-white/15 p-8">
            <h3 class="text-2xl text-white">Parceria com a Plataforma Rifa</h3>
            <p class="mt-3 leading-relaxed text-white/80">A <a href="https://plataformarifa.com.br/regulamentacao" target="_blank" rel="noopener" class="underline underline-offset-2 hover:text-white">Plataforma Rifa</a> é responsável pela tecnologia de venda e apuração. A regulamentação e o marketing são contratados diretamente com a Take 1. O orçamento depende do tipo de rifa, do valor dos prêmios e dos serviços escolhidos.</p>
          </div>
        </div>
      </div>
    </section>"""

VIDEOS_EXTRA = """    <section class="py-20 lg:py-28" aria-label="Mensagem">
      <div class="container-site">
        <p class="revelar mx-auto max-w-5xl text-center font-display text-4xl font-normal leading-tight tracking-tight text-tinta sm:text-5xl lg:text-6xl">
          Mais compreensão, mais prevenção, <em class="italic text-vinho">mais segurança</em> para todos.
        </p>
      </div>
    </section>"""

SERVICO_DADOS = {
    'publicidade': dict(
        h1='Publicidade que <em>constrói marca</em> e gera vendas.',
        lead='A publicidade é estratégica para empresas, construção de marca e venda de produtos e serviços. A Take 1 oferece soluções e ferramentas para planejar e desenvolver a publicidade na conquista dos melhores resultados, com soluções criativas e funcionais de acordo com a realidade do investimento.',
        itens=['Campanha publicitária institucional e promocional', 'Planejamento e execução', 'Plano de mídia',
               'Peça para mídia impressa e externa', 'Material para PDV', 'Ação promocional',
               'Anúncio de revista e jornal', 'Criação de mídias alternativas', 'Campanha para evento empresarial, social e cultural'],
        pilares=[('Planejamento antes da criação', 'Cada campanha parte de objetivos claros, público definido e um plano de mídia coerente com o investimento.'),
                 ('Criativa e funcional', 'Ideias que funcionam no mundo real: na mídia, no ponto de venda e no evento.'),
                 ('Integrada às outras frentes', 'A campanha conversa com o digital, com o vídeo e com a comunicação interna da sua empresa.')],
        wa='Olá! Vim pelo site da Take 1 e quero falar sobre publicidade.'),
    'comunicacao-empresarial': dict(
        h1='Comunicação empresarial que <em>aproxima</em> a empresa dos seus públicos.',
        lead='A Take 1 oferece soluções completas e integradas de comunicação empresarial, com o objetivo de incrementar o relacionamento da sua empresa com os diferentes públicos que integram seus ambientes de negócios: colaboradores, clientes, fornecedores e comunidade.',
        itens=['Projeto de comunicação interna', 'Planejamento de comunicação institucional', 'Manual de identidade visual',
               'Campanhas de segurança, qualidade de vida e ambiente de trabalho', 'Apresentação institucional de alto nível',
               'Layout de frota', 'Catálogo e folder corporativo', 'Relatório fotográfico de obras',
               'Produção de conteúdos editoriais customizados', 'Vídeo institucional, de segurança, de treinamento e promocional'],
        pilares=[('Experiência de grande indústria', 'Os sócios da Take 1 atuaram por mais de 15 anos na comunicação corporativa da Aracruz Celulose.'),
                 ('Interna e institucional', 'Do endomarketing às apresentações de alto nível, a mesma mensagem para todos os públicos.'),
                 ('Segurança e cultura', 'Campanhas e vídeos que reforçam comportamentos seguros, qualidade de vida e a cultura da empresa.')],
        wa='Olá! Vim pelo site da Take 1 e quero falar sobre comunicação empresarial.'),
    'marketing-digital': dict(
        h1='Marketing digital e redes sociais com a <em>Take 1 Lab</em>.',
        lead='Procurando uma agência para criar e gerenciar as redes sociais da sua empresa? A Take 1 Lab, nossa agência digital, leva o seu negócio para o universo digital, fortalece a imagem da sua marca e cria um relacionamento mais próximo com clientes e futuros clientes.',
        logo=True,
        itens=['Planejamento estratégico', 'Gestão de redes sociais', 'Produção de conteúdo', 'Métricas e anúncios',
               'Campanhas on-line', 'Campanha de tráfego', 'WhatsApp Business: catálogo e mensagens automáticas',
               'Desenvolvimento de site', 'Manutenção e otimização de site', 'Hotsite e landing page',
               'E-commerce e loja virtual', 'E-mail marketing', 'Vídeo', 'Criação e interatividade'],
        pilares=[('Presença com estratégia', 'Planejamento antes de postar: objetivos, públicos, tom de voz e calendário.'),
                 ('Conteúdo e anúncios', 'Produção de conteúdo, gestão das redes e campanhas de tráfego para alcançar quem importa.'),
                 ('Resultados medidos', 'Métricas acompanhadas de perto para ajustar as ações pelos resultados.')],
        wa='Olá! Vim pelo site e quero conhecer a Take 1 Lab.'),
    'design-grafico': dict(
        h1='Editoração e design gráfico com a <em>identidade</em> da sua marca.',
        lead='A Take 1 faz editoração e design gráfico de diferentes publicações, de caráter periódico e não periódico, com soluções integradas de comunicação, focadas na identidade visual da sua empresa.',
        itens=['Logomarca', 'Papelaria', 'Catálogo', 'Livro', 'Revista', 'Folder e panfleto', 'Jornal e informativo',
               'Banner, placa e display', 'Embalagem'],
        pilares=[('Identidade consistente', 'Cada peça segue a identidade visual da sua empresa, do cartão de visita à embalagem.'),
                 ('Publicações periódicas', 'Revistas, jornais e informativos com projeto gráfico e editoração para todas as edições.'),
                 ('Pronto para produção', 'Arquivos finalizados e preparados para impressão ou para uso digital.')],
        wa='Olá! Vim pelo site da Take 1 e quero falar sobre design gráfico.'),
    'videos-de-treinamento': dict(
        h1='Treinamentos de segurança em vídeos que o colaborador <em>entende e lembra</em>.',
        lead='Treinamentos de segurança precisam ser claros, objetivos e impactantes. Com vídeos animados, a sua empresa comunica procedimentos críticos de forma simples, padronizada e fácil de absorver, reduzindo riscos e aumentando a adesão das equipes.',
        figura=VIDEO_MOCK,
        titulo_itens='Do roteiro à <em>pós-produção</em>.',
        intro_itens='Transformamos a apresentação das normas e dos procedimentos em vídeos animados criativos, claros e que prendem a atenção do colaborador. Fazemos todas as etapas e entregamos o vídeo pronto para usar.',
        itens=['Roteiro a partir das suas normas e procedimentos', 'Animação', 'Versão híbrida: imagens reais, animação e cartelas',
               'Locução e trilha', 'Pós-produção', 'Vídeo pronto para usar'],
        pilares=[('Normas viram prática', 'Orientações do dia a dia que reforçam comportamentos seguros, sem complicação.'),
                 ('Uso ilimitado', 'Um recurso para usar sempre, sem precisar de equipe dedicada para aplicar o treinamento.'),
                 ('Padronizado', 'Todas as equipes recebem a mesma orientação, do mesmo jeito, em qualquer turno ou unidade.')],
        extra=VIDEOS_EXTRA,
        wa='Olá! Vim pelo site da Take 1 e quero saber sobre vídeos de treinamento de segurança.'),
    'regulamentacao-de-rifas': dict(
        h1='Regulamentação de rifas filantrópicas na <em>SPA/MF</em>.',
        lead='Rifa com prêmio precisa de autorização. A Take 1 cuida de todo o processo junto à Secretaria de Prêmios e Apostas do Ministério da Fazenda, do regulamento ao Certificado de Autorização e à prestação de contas.',
        imagem=None,
        titulo_itens='Para entidades <em>sem fins lucrativos</em>.',
        intro_itens='Rifas filantrópicas de entidades formalmente constituídas e enquadradas na Lei 5.768/1971, em todo o Brasil:',
        itens=['Associações', 'Fundações', 'Instituições religiosas', 'Instituições esportivas', 'Instituições culturais', 'Instituições assistenciais'],
        pilares=None,
        extra=RIFAS_EXTRA,
        wa='Olá! Vim pelo site da Take 1 e quero regulamentar minha rifa.'),
}


def pagina_servico(pg):
    d = SERVICO_DADOS[pg['arquivo']]
    if d.get('figura'):
        figura = d['figura']
    elif d.get('imagem'):
        figura = f"""<figure class="revelar quadro text-tinta/40">
          <div class="reservado aspect-[4/3] rounded-sm">{d['imagem']}</div>
        </figure>"""
    else:
        figura = ''
    logo = ('<img src="{{P}}assets/img/logo-take1lab.png" alt="Take 1 Lab — Marketing Digital" width="91" height="72" class="revelar mb-8 h-16 w-auto">'
            if d.get('logo') else '')
    col_txt = 'lg:col-span-7' if figura else 'lg:col-span-10'
    topo = f"""    <section class="relative overflow-hidden pb-20 pt-28 lg:pb-28 lg:pt-32" aria-labelledby="pagina-titulo">
      <img src="{{{{P}}}}assets/img/espiral.svg" alt="" aria-hidden="true"
           class="pointer-events-none absolute -right-56 -top-40 w-[44rem] max-w-none animate-girar opacity-[0.08] lg:w-[56rem]">
      <div class="container-site relative">
        <div class="grid items-center gap-14 lg:grid-cols-12 lg:gap-16">
          <div class="min-w-0 {col_txt}">
            {logo}
            <h1 id="pagina-titulo" class="revelar text-[2.5rem] font-normal leading-[1.08] tracking-tight sm:text-6xl lg:text-7xl">{d['h1']}</h1>
            <p class="revelar lead mt-8 max-w-3xl">{d['lead']}</p>
            <div class="revelar mt-10 flex flex-col gap-3 sm:flex-row">
              <a href="{wa(d['wa'])}" target="_blank" rel="noopener" class="btn-primario">{icone('whatsapp', 'h-5 w-5')}Fale com a Take 1 pelo WhatsApp</a>
              <a href="#o-que-fazemos" class="btn-contorno">O que fazemos</a>
            </div>
          </div>
          {'<div class="lg:col-span-5">' + figura + '</div>' if figura else ''}
        </div>
      </div>
    </section>"""

    icones_itens = ICONE_ITENS[pg['arquivo']]
    assert len(icones_itens) == len(d['itens']), pg['arquivo']
    itens = '\n'.join(f"""          <li class="revelar flex items-center gap-5 rounded-2xl border border-transparent bg-marfim p-5 transition duration-300 hover:-translate-y-0.5 hover:border-vinho/20 hover:shadow-lg hover:shadow-tinta/5">
            <span class="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-vinho-50">{icone(ic, 'h-7 w-7 text-vinho')}</span>
            <span class="min-w-0 flex-1 text-lg font-semibold leading-snug text-tinta">{x}</span>
            <span class="self-start font-display text-sm tabular-nums text-vinho/60">{i:02d}</span>
          </li>""" for i, (x, ic) in enumerate(zip(d['itens'], icones_itens), 1))
    secao_itens = f"""    <section id="o-que-fazemos" class="bg-white py-24 lg:py-32" aria-labelledby="itens-titulo">
      <div class="container-site">
        <div class="mb-14 grid gap-8 lg:grid-cols-12 lg:items-end lg:gap-16">
          <div class="lg:col-span-7">
            <p class="eyebrow"><span class="cena">01</span>O que fazemos</p>
            <h2 id="itens-titulo" class="titulo-secao revelar">{d.get('titulo_itens', 'Tudo o que a sua marca <em>precisa</em>.')}</h2>
          </div>
          {f'<p class="revelar text-lg leading-relaxed text-nevoa lg:col-span-5">{d["intro_itens"]}</p>' if d.get('intro_itens') else ''}
        </div>
        <ul class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
{itens}
        </ul>
      </div>
    </section>"""

    pilares = ''
    if d.get('pilares'):
        cols = '\n'.join(f"""          <li class="revelar flex flex-col rounded-[1.75rem] bg-white p-8 shadow-sm shadow-tinta/5">
            <span class="flex items-start justify-between gap-4">{icone(ICONE_PILAR[pg['arquivo']][i - 1], 'h-9 w-9 text-vinho')}<span class="font-display text-lg text-vinho/60">0{i}</span></span>
            <h3 class="mt-6 text-2xl">{tt}</h3>
            <p class="mt-3 text-nevoa">{tx}</p>
          </li>""" for i, (tt, tx) in enumerate(d['pilares'], 1))
        pilares = f"""    <section class="bg-areia py-24 lg:py-32" aria-labelledby="pilares-titulo">
      <div class="container-site">
        <p class="eyebrow"><span class="cena">02</span>Por que a Take 1</p>
        <h2 id="pilares-titulo" class="titulo-secao revelar max-w-3xl">Comunicação <em>integrada</em> de ponta a ponta.</h2>
        <ul class="mt-14 grid gap-5 md:grid-cols-3">
{cols}
        </ul>
      </div>
    </section>"""

    return '\n\n'.join(x for x in [topo, secao_itens, pilares, d.get('extra', ''), '{{FAQ}}', '{{OUTROS}}', bloco_cta(d['wa'])] if x)


def montar(pg):
    P = '../' * pg['caminho'].count('/')
    if pg['arquivo'] in SERVICO_DADOS:
        miolo = pagina_servico(pg)
    else:
        miolo = open(os.path.join(RAIZ, 'src', 'paginas', pg['arquivo'] + '.html'), encoding='utf-8').read()
    trocas = {
        '{{FAQ}}': bloco_faq(pg['arquivo']) if pg['arquivo'] in FAQ else '',
        '{{CTA}}': bloco_cta(),
        '{{OUTROS}}': bloco_outros(pg['arquivo']) if pg.get('servico') else '',
        '{{CLIENTES}}': bloco_clientes(CLIENTES),
        '{{CLIENTES_DESTAQUE}}': bloco_clientes(CLIENTES[:12]),
    }
    for k, v in trocas.items():
        miolo = miolo.replace(k, v)
    miolo = re.sub(r'\{\{ICONE:(\w+)(?:\|([^}]*))?\}\}', lambda m: icone(m.group(1), m.group(2) or 'h-8 w-8 text-vinho'), miolo)
    miolo = miolo.replace('{{WA}}', WA).replace('{{P}}', P).replace('{{HOME}}', P or './')
    html = head(pg, P) + header(pg, P) + '\n  <main id="conteudo">\n' + miolo.rstrip() + '\n  </main>\n' + footer(P)
    destino = os.path.join(RAIZ, pg['caminho'], 'index.html')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    open(destino, 'w', encoding='utf-8').write(html)
    return destino


def sitemap():
    urls = '\n'.join(f'  <url><loc>{SITE}/{pg["caminho"]}</loc><priority>{"1.0" if not pg["caminho"] else "0.8"}</priority></url>'
                     for pg in PAGINAS)
    open(os.path.join(RAIZ, 'sitemap.xml'), 'w', encoding='utf-8').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    open(os.path.join(RAIZ, 'robots.txt'), 'w', encoding='utf-8').write(
        f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')


if __name__ == '__main__':
    for pg in PAGINAS:
        print('ok', os.path.relpath(montar(pg), RAIZ))
    sitemap()
    print('ok sitemap.xml e robots.txt')
