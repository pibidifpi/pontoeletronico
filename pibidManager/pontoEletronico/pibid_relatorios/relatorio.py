__author__ = 'charles'

from django.views.generic import *
from django.http import HttpResponse
from reportlab.pdfgen import canvas

class Relatorios(View):
    #dados do cabecalho
    instituicao = 'INSTITUTO FEDERAL DO PIAUI - IFPI'
    coordenacao = 'COORDENACAO DE APERFEICOAMENTO DE PESSOAL DE NIVEL SUPERIOR'
    programa = 'PROGRAMA INSTITUCIONAL DE BOLSAS DE INICIACAO A DOCENCIA - PIBID'
    complemento = 'AREA: Informatica.       MES / ANO:  '
    titulo = None

    #fim dados do cabecalho

    response = None
    nome_arquivo = None
    listagem = None
    cabecalho_tabela = None
    alinhamento_texto = None

    def set_nome_arquivo(self, nome_arquivo):
        self.response['Content-Disposition'] = 'attachment; filename="'+nome_arquivo+'"'

    def set_texto_a_esquerda(self):
        self.alinhamento_texto = 'Left'

    def set_texto_centralizado(self):
        self.alinhamento_texto = 'center'

    def set_texto_a_direita(self):
        self.alinhamento_texto = 'Right'

    def set_texto_justificado(self):
        self.alinhamento_texto = 'Justify'

    def set_limpar_alinhamento(self):
        self.alinhamento_texto = None


class RelatoriosPDF(Relatorios):
    p = None
    nome_arquivo = 'relatorio_pdf'

    def novo_arquivo(self):
        self.response = HttpResponse(content_type='application/pdf')
        self.set_nome_arquivo(self.nome_arquivo+'.pdf')

    def abrir(self):
        # Create the PDF object, using the response object as its "file."
        self.p = canvas.Canvas(self.response)

    def seta(self, x, y, string):
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        self.p.drawString(x, y, string)

    def imprimir(self):
        # Close the PDF object cleanly, and we're done.
        self.p.showPage()
        self.p.save()

class RelatoriosWord(Relatorios):
    nome_arquivo = 'relatorio_word'

    def novo_arquivo(self):
        self.response = HttpResponse(content_type='application/msword')
        self.seta_cabecalho()
        self.set_nome_arquivo(self.nome_arquivo+'.doc')

    def seta_cabecalho(self):

        self.set_texto_centralizado()
        self.seta(self.negrito(self.instituicao))
        self.seta(self.negrito(self.coordenacao))
        self.seta(self.negrito(self.programa))
        self.quebrar_linha()
        self.seta(self.negrito(self.complemento))
        self.quebrar_linha()
        self.seta(self.negrito(self.titulo))
        self.set_limpar_alinhamento()

    def quebrar_linha(self):
        self.seta('')

    def seta(self, string):
        texto = '<p'
        if(self.alinhamento_texto):
            texto += ' align="'+self.alinhamento_texto+'"';
        texto += ' >'+string+'</p>'

        self.response.write(texto)

    def negrito(self, string):
        return '<b>'+string+'</b>'

    def criar_tabela(self):
        self.response.write('<table width="650">')

    def abrir_tabela(self):
        self.criar_tabela()
        self.seta_linha(self.cabecalho_tabela)

    def fechar_tabela(self):
        self.response.write('</table>')

    def seta_linha(self, array_string):
        self.response.write('<tr>')

        for string in array_string:
            self.response.write('<td>'+string+'</td>')

        self.response.write('</tr>')

    def seta_agrupamento(self, string, colspan):
        self.criar_tabela()
        self.response.write('<td colspan="'+ str(colspan) +'">'+ self.negrito(string) +'</td>')
        self.fechar_tabela()
