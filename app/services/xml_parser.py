from lxml import etree
from .mongo import save_to_mongodb


def process_xml(xml_path):
    try:
        # Parse o XML usando lxml
        tree = etree.parse(xml_path)
        root = tree.getroot()

        # Extração de dados do XML (exemplo)
        data = {
            "tag1": root.find('.//tag1').text,
            "tag2": root.find('.//tag2').text,
            # Adicionar mais extração conforme necessidade
        }

        # Aqui você pode enviar para o banco de dados ou outro sistema
        save_to_mongodb(data)

    except Exception as e:
        print(f"Erro ao processar XML {xml_path}: {e}")
