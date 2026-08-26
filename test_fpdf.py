from datetime import date
from decimal import Decimal
from fpdf import FPDF

def _gerar_pdf(nome: str, dados: list[dict]) -> bytes:
    pdf = FPDF()
    pdf.add_page(orientation="L")
    pdf.set_font("helvetica", size=10)
    
    pdf.set_font("helvetica", style="B", size=14)
    pdf.cell(0, 10, f"Relatorio: {nome.replace('_', ' ').title()}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    if not dados:
        pdf.set_font("helvetica", size=10)
        pdf.cell(0, 10, "Nenhum dado encontrado.", new_x="LMARGIN", new_y="NEXT")
        return pdf.output()
        
    colunas = list(dados[0].keys())
    col_width = pdf.epw / len(colunas)
    line_height = 8
    
    pdf.set_font("helvetica", style="B", size=9)
    for col in colunas:
        pdf.cell(col_width, line_height, col.replace('_', ' ').title(), border=1)
    pdf.ln(line_height)
    
    pdf.set_font("helvetica", size=8)
    for linha in dados:
        for col in colunas:
            val = linha.get(col)
            if val is None:
                txt = "-"
            elif isinstance(val, (date,)):
                txt = val.strftime("%d/%m/%Y")
            elif isinstance(val, Decimal):
                txt = f"R$ {val:,.2f}"
            else:
                txt = str(val)
                
            if len(txt) > 35:
                txt = txt[:32] + "..."
            
            txt = txt.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(col_width, line_height, txt, border=1)
        pdf.ln(line_height)
        
    return pdf.output()

dados = [{"nome_jornal": "A", "total_edicoes": 1, "ultima_edicao": date(2023,1,1)}]
out = _gerar_pdf("teste", dados)
print(type(out))
