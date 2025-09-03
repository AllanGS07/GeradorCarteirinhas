# app_ui.py (VERSÃO FINAL - ENDEREÇO EM 3 LINHAS E TEL2)
import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox, 
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QDateEdit
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QDate
from pdf_generator import create_student_cards_pdf
from utils import resource_path, title_case_formatter, format_telefone, format_cep

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Carteirinhas - Prefeitura de Piracanjuba")
        self.setWindowIcon(QIcon(resource_path("assets/icone.ico")))
        self.setGeometry(100, 100, 900, 700)

        self.students_data = []
        self.current_photo_path = None

        main_layout = QHBoxLayout()
        
        left_layout = QVBoxLayout()
        self.photo_preview = QLabel("Escolha a foto do aluno")
        self.photo_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_preview.setFixedSize(250, 300)
        self.photo_preview.setStyleSheet("border: 1px solid #ccc; background-color: #f0f0f0;")
        
        btn_select_photo = QPushButton("Selecionar Foto")
        btn_select_photo.clicked.connect(self.select_photo)
        
        left_layout.addWidget(self.photo_preview)
        left_layout.addWidget(btn_select_photo)
        left_layout.addStretch()

        right_layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.nome_input = QLineEdit()
        self.nascimento_input = QDateEdit()
        self.nascimento_input.setDate(QDate.currentDate())
        self.nascimento_input.setDisplayFormat("dd/MM/yyyy")
        self.escola_input = QLineEdit()
        self.responsavel_input = QLineEdit()
        self.tel1_input = QLineEdit()
        self.tel2_input = QLineEdit() # TELEFONE 2 ESTÁ AQUI
        self.zona_input = QComboBox()
        self.zona_input.addItems(["Rural", "Urbana"])
        
        self.logradouro_input = QLineEdit()
        self.numero_input = QLineEdit()
        self.bairro_input = QLineEdit()
        self.cep_input = QLineEdit()

        form_layout.addRow("Nome do Aluno:", self.nome_input)
        form_layout.addRow("Data de Nascimento:", self.nascimento_input)
        form_layout.addRow("Escola:", self.escola_input)
        form_layout.addRow("Nome do Responsável:", self.responsavel_input)
        form_layout.addRow("Telefone 1:", self.tel1_input)
        form_layout.addRow("Telefone 2 (Opcional):", self.tel2_input)
        form_layout.addRow("Zona:", self.zona_input)
        form_layout.addRow("Logradouro:", self.logradouro_input)
        form_layout.addRow("Número:", self.numero_input)
        form_layout.addRow("Bairro:", self.bairro_input)
        form_layout.addRow("CEP:", self.cep_input)
        
        btn_add_student = QPushButton("Adicionar Aluno à Lista")
        btn_add_student.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        btn_add_student.clicked.connect(self.add_student)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nome", "Escola", "Responsável"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        btn_generate_pdf = QPushButton("Gerar PDF de Impressão")
        btn_generate_pdf.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; font-size: 16px;")
        btn_generate_pdf.clicked.connect(self.generate_pdf)

        right_layout.addLayout(form_layout)
        right_layout.addWidget(btn_add_student)
        right_layout.addWidget(self.table)
        right_layout.addWidget(btn_generate_pdf)
        
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        main_layout.setStretch(1, 2)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Foto", "", "Imagens (*.png *.jpg *.jpeg)")
        if file_path:
            self.current_photo_path = file_path
            pixmap = QPixmap(file_path)
            self.photo_preview.setPixmap(pixmap.scaled(250, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def add_student(self):
        if not self.nome_input.text() or not self.current_photo_path:
            QMessageBox.warning(self, "Atenção", "O nome do aluno e a foto são obrigatórios.")
            return

        # --- LÓGICA DE FORMATAÇÃO DO ENDEREÇO (VOLTANDO COM <br/>) ---
        logradouro = title_case_formatter(self.logradouro_input.text())
        numero = self.numero_input.text()
        bairro = title_case_formatter(self.bairro_input.text())
        cep_formatado = format_cep(self.cep_input.text())

        address_lines = []
        if logradouro and numero:
            address_lines.append(f"{logradouro}, Nº {numero};")
        
        if bairro:
            address_lines.append(f"{bairro};")

        if cep_formatado and len(cep_formatado) == 9:
            address_lines.append(cep_formatado)
        
        # Junta as partes com uma quebra de linha HTML (<br/>)
        endereco_completo = "<br/>".join(address_lines)
        # --- FIM DA LÓGICA DE FORMATAÇÃO ---

        student = {
            "nome": title_case_formatter(self.nome_input.text()),
            "nascimento": self.nascimento_input.date().toString("dd/MM/yyyy"),
            "escola": title_case_formatter(self.escola_input.text()),
            "responsavel": title_case_formatter(self.responsavel_input.text()),
            "tel1": format_telefone(self.tel1_input.text()),
            "tel2": format_telefone(self.tel2_input.text()), # TELEFONE 2 ESTÁ AQUI
            "zona": self.zona_input.currentText(),
            "endereco": endereco_completo,
            "foto_path": self.current_photo_path
        }
        self.students_data.append(student)

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QTableWidgetItem(student["nome"]))
        self.table.setItem(row_count, 1, QTableWidgetItem(student["escola"]))
        self.table.setItem(row_count, 2, QTableWidgetItem(student["responsavel"]))

        self.clear_fields()

    def generate_pdf(self):
        if not self.students_data:
            QMessageBox.warning(self, "Atenção", "Nenhum aluno foi adicionado à lista.")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", "Carteirinhas.pdf", "PDF Files (*.pdf)")
        if output_path:
            try:
                create_student_cards_pdf(self.students_data, output_path)
                QMessageBox.information(self, "Sucesso", f"PDF gerado com sucesso em:\n{output_path}")
                self.students_data.clear()
                self.table.setRowCount(0)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o PDF:\n{e}")

    def clear_fields(self):
        self.nome_input.clear()
        self.nascimento_input.setDate(QDate.currentDate())
        self.escola_input.clear()
        self.responsavel_input.clear()
        self.tel1_input.clear()
        self.tel2_input.clear() # TELEFONE 2 ESTÁ AQUI
        self.logradouro_input.clear()
        self.numero_input.clear()
        self.bairro_input.clear()
        self.cep_input.clear()
        self.photo_preview.setText("Escolha a foto do aluno")
        self.current_photo_path = None