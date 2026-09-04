import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF


class ReportGenerator:
    """Classe responsável por processar os dados e gerar o documento PDF."""
    
    def __init__(self, dataframe):
        self.df = dataframe

    def generate_category_chart(self, output_image="spending_by_category.png"):
        """Gera e salva o gráfico de barras por categoria."""
        plt.figure(figsize=(10, 5))
        category_summary = self.df.groupby('categoria')['ValorCompra'].sum()
        category_summary.plot(kind='bar', color='skyblue')
        
        plt.title("Spending by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Spend (R$)")
        plt.tight_layout()
        plt.savefig(output_image)
        plt.close()
        
        return output_image

    def export_pdf(self, filename="fatura_analysis.pdf"):
        """Monta a estrutura do PDF e exporta o relatório final."""
        total_value = self.df['ValorCompra'].sum()
        chart_path = self.generate_category_chart()

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Cabeçalho
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 10, txt="Fatura Analysis Report", ln=True, align='C')

        # Resumo Financeiro
        pdf.set_font('Arial', '', 12)
        pdf.cell(190, 10, txt=f"Total Value of Purchases: R$ {total_value:.2f}", ln=True)

        # Inserção do Gráfico
        pdf.image(chart_path, x=15, y=45, w=180)

        # Salva o arquivo
        pdf.output(filename)

        # Remove a imagem temporária gerada para o gráfico
        if os.path.exists(chart_path):
            os.remove(chart_path)


class FaturaAnalyzerApp:
    """Classe principal para gerenciar a interface gráfica (Tkinter)."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Fatura Analysis")
        self.root.geometry("400x200")
        
        self._setup_ui()

    def _setup_ui(self):
        """Configura os elementos visuais da janela."""
        self.upload_button = tk.Button(
            self.root, 
            text="Upload Fatura CSV", 
            command=self.upload_and_analyze, 
            padx=10, 
            pady=5
        )
        self.upload_button.pack(pady=60)

    def upload_and_analyze(self):
        """Gerencia o evento de upload de arquivo e chamada da análise."""
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return

        try:
            dataframe = pd.read_csv(filepath)
            
            # Instancia o gerador de relatório e executa
            report = ReportGenerator(dataframe)
            report.export_pdf()

            messagebox.showinfo("Success", "PDF generated successfully: fatura_analysis.pdf")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaturaAnalyzerApp(root)
    root.mainloop()
