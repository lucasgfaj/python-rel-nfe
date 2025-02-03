
import os
import xml.etree.ElementTree as ET

def ler_nfes_da_pasta(pasta):
    nfes = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.xml'):
            caminho_completo = os.path.join(pasta, arquivo)
            tree = ET.parse(caminho_completo)
            root = tree.getroot()
            
            # Namespaces necessários para acessar os elementos
            ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

            numero = root.find('.//nfe:infNFe/nfe:ide/nfe:nNF', ns).text
            data_completa = root.find('.//nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
            data = data_completa.split('T')[0]  # Extrai apenas a data
            
            preco = float(root.find('.//nfe:total/nfe:ICMSTot/nfe:vNF', ns).text)
            status_code = root.find('.//nfe:protNFe/nfe:infProt/nfe:cStat', ns).text
            cfop = root.find('.//nfe:det/nfe:prod/nfe:CFOP', ns).text

            if status_code == '100':
                status = 'APROVADA'
            elif status_code == '110':
                status = 'INUTILIZADA'
            elif status_code == '101':
                status = 'CANCELADA'
            elif cfop.startswith('1') or cfop.startswith('2') or cfop.startswith('3') or cfop.startswith('5'):
                status = 'DEVOLUCAO'
            else:
                status = 'OUTRO'
            
            nfes.append({
                'numero': numero,
                'data': data,
                'preco': preco,
                'status': status,
                'cfop': cfop
            })
    return nfes

def gerar_relatorio(nfes):
    aprovadas = [nfe for nfe in nfes if nfe['status'] == 'APROVADA']
    devolucoes = [nfe for nfe in nfes if nfe['status'] == 'DEVOLUCAO']
    inutilizadas = [nfe for nfe in nfes if nfe['status'] == 'INUTILIZADA']
    canceladas = [nfe for nfe in nfes if nfe['status'] == 'CANCELADA']
    
    total_final = sum(nfe['preco'] for nfe in aprovadas)
    
    with open('relatorio_nfes.txt', mode='w') as file:
        file.write("NF-es Aprovadas:\n")
        for nfe in aprovadas:
            file.write(f"Numero: {nfe['numero']}, Data: {nfe['data']}, Preco: {nfe['preco']}, CFOP: {nfe['cfop']}\n")
        
        file.write("\nNF-es Devoluções:\n")
        for nfe in devolucoes:
            file.write(f"Numero: {nfe['numero']}, Data: {nfe['data']}, Preco: {nfe['preco']}, CFOP: {nfe['cfop']}\n")

        file.write("\nNF-es Inutilizadas:\n")
        for nfe in inutilizadas:
            file.write(f"Numero: {nfe['numero']}, Data: {nfe['data']}, Preco: {nfe['preco']}, CFOP: {nfe['cfop']}\n")
        
        file.write("\nNF-es Canceladas:\n")
        for nfe in canceladas:
            file.write(f"Numero: {nfe['numero']}, Data: {nfe['data']}, Preco: {nfe['preco']}, CFOP: {nfe['cfop']}\n")
        
        file.write(f"\nValor Total das NF-es Aprovadas: {total_final}\n")

def main():
    pasta_nfes = 'nfe'  # Diretório onde os arquivos XML estão armazenados
    nfes = ler_nfes_da_pasta(pasta_nfes)
    gerar_relatorio(nfes)
    print("Relatório gerado com sucesso!")

if __name__ == "__main__":
    main()
