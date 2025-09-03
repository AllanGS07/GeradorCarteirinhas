# pdf_generator.py (VERSÃO FINAL REFEITA - CADA ELEMENTO NO SEU LUGAR)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from utils import resource_path
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black

# ==============================================================================
# CONFIGURAÇÕES GLOBAIS
# ==============================================================================
# O tamanho da carteirinha individual (em polegadas)
CARD_WIDTH = 3.370 * inch
CARD_HEIGHT = 2.130 * inch

# ==============================================================================


def draw_single_card_content(c, student, is_front, card_x_offset, card_y_offset):
    """
    Desenha o conteúdo de UMA carteirinha nas coordenadas relativas (0,0) do cartão.
    card_x_offset e card_y_offset são as coordenadas do canto inferior esquerdo do cartão na folha A4.
    """
    template_path = (
        resource_path("assets/frente_template.png")
        if is_front
        else resource_path("assets/verso_template.png")
    )
    c.drawImage(
        template_path,
        card_x_offset,
        card_y_offset,
        width=CARD_WIDTH,
        height=CARD_HEIGHT,
        mask="auto",
    )

    # As coordenadas aqui são RELATIVAS ao canto inferior esquerdo da carteirinha (card_x_offset, card_y_offset)
    if is_front:
        # --- FOTO ---
        # x_offset + x_da_foto, y_offset + y_da_foto (do template)
        c.drawImage(
            student["foto_path"],
            card_x_offset + 0.283 * inch,
            card_y_offset + 0.389 * inch,
            width=0.982 * inch,
            height=1.352 * inch,
            mask="auto",
        )

        # --- TEXTOS DA FRENTE ---
        # Coordenadas calculadas para a LINHA DE BASE do texto

        # Nome do Aluno
        c.setFont("Poppins-Bold", 8)
        c.drawString(
            card_x_offset + 1.442 * inch,
            card_y_offset + 1.25 * inch,
            student["nome"].upper(),
        )

        c.setFont("Poppins-Bold", 7)
        # Data de Nascimento
        c.drawString(
            card_x_offset + 1.442 * inch,
            card_y_offset + 1.12 * inch,
            student["nascimento"],
        )
        # Escola
        c.drawString(
            card_x_offset + 2.400 * inch,
            card_y_offset + 1.12 * inch,
            student["escola"].upper(),
        )
        # Telefone 1
        c.drawString(
            card_x_offset + 1.442 * inch, card_y_offset + 0.88 * inch, student["tel1"]
        )
        # Telefone 2 (Desenha apenas se o campo não estiver vazio)
        if student["tel2"].strip():  # Usa .strip() para verificar se há texto real
            c.drawString(
                card_x_offset + 1.442 * inch,
                card_y_offset + 0.76 * inch,
                student["tel2"],
            )
        # Responsável
        c.drawString(
            card_x_offset + 2.400 * inch,
            card_y_offset + 0.88 * inch,
            student["responsavel"],
        )
    else:
        # --- TEXTOS DO VERSO ---
        # Coordenadas calculadas para a LINHA DE BASE do texto

        # Nome do Aluno (Verso)
        c.setFont("Poppins-Bold", 8)
        c.drawString(
            card_x_offset + 1.500 * inch,
            card_y_offset + 1.340 * inch,
            student["nome"].upper(),
        )

        # Zona
        c.setFont("Poppins-Bold", 7)
        c.drawString(
            card_x_offset + 0.754 * inch, card_y_offset + 1.120 * inch, student["zona"]
        )

        # --- ENDEREÇO COM PARAGRAPH ---
        styles = getSampleStyleSheet()
        address_style = ParagraphStyle(
            "AddressStyle",
            parent=styles["Normal"],
            fontName="Poppins-Bold",
            fontSize=6.5,  # Fonte um pouco menor para caber melhor
            textColor=black,
            leading=8,
        )  # Espaçamento entre linhas

        # Posição X do canto esquerdo do bloco de texto do endereço
        addr_x_relative = 1.848 * inch
        # Posição Y do canto INFERIOR do bloco de texto do endereço
        addr_y_bottom_relative = 0.900 * inch
        # Largura máxima do bloco de texto para quebrar a linha
        addr_width_relative = 1.200 * inch
        # Altura máxima do bloco de texto para o endereço (para 3 linhas)
        addr_height_relative = 0.35 * inch

        p = Paragraph(student["endereco"], style=address_style)

        # wrapOn calcula a altura real do parágrafo
        p.wrapOn(c, addr_width_relative, addr_height_relative)

        # p.drawOn(canvas, x, y) onde x e y são as coordenadas do canto inferior esquerdo do parágrafo
        p.drawOn(
            c, card_x_offset + addr_x_relative, card_y_offset + addr_y_bottom_relative
        )


def create_student_cards_pdf(students, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    PAGE_WIDTH, PAGE_HEIGHT = A4

    font_path = resource_path("assets/Poppins-Bold.ttf")
    pdfmetrics.registerFont(TTFont("Poppins-Bold", font_path))

    # Calcula as margens na folha A4 para 10 carteirinhas
    MARGIN_X = (PAGE_WIDTH - (2 * CARD_WIDTH)) / 3
    MARGIN_Y = (PAGE_HEIGHT - (5 * CARD_HEIGHT)) / 6

    # Lista de coordenadas para cada uma das 10 posições na folha A4
    positions_on_a4 = []
    for row in range(5):
        for col in range(2):
            x = MARGIN_X * (col + 1) + CARD_WIDTH * col
            # O y é calculado da borda superior da página, mas o ReportLab usa a borda inferior como 0
            # Então: Altura da página - (margem_superior + (altura_do_cartão + margem_vertical_entre_cartoes) * linha_atual)
            y = PAGE_HEIGHT - (MARGIN_Y * (row + 1) + CARD_HEIGHT * (row + 1))
            positions_on_a4.append((x, y))

    # --- DESENHA AS FRENTES ---
    for i, student in enumerate(students):
        # Pega a posição na folha A4 para a carteirinha atual
        card_x_offset, card_y_offset = positions_on_a4[i % 10]

        # Desenha todo o conteúdo da frente da carteirinha
        draw_single_card_content(
            c,
            student,
            is_front=True,
            card_x_offset=card_x_offset,
            card_y_offset=card_y_offset,
        )

        # Gerencia a paginação para as frentes
        if (i + 1) % 10 == 0 and (i + 1) < len(students):
            c.showPage()

    if students:
        c.showPage()  # Adiciona uma nova página para os versos

    # --- DESENHA OS VERSOS ---
    for i, student in enumerate(students):
        # Pega a posição na folha A4 para a carteirinha atual
        card_x_offset, card_y_offset = positions_on_a4[i % 10]

        # Desenha todo o conteúdo do verso da carteirinha
        draw_single_card_content(
            c,
            student,
            is_front=False,
            card_x_offset=card_x_offset,
            card_y_offset=card_y_offset,
        )

        # Gerencia a paginação para os versos
        if (i + 1) % 10 == 0 and (i + 1) < len(students):
            c.showPage()

    c.save()
