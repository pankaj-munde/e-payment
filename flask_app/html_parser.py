import AdvancedHTMLParser

parser = AdvancedHTMLParser.AdvancedHTMLParser()

parser.parseFile('templates/index.html')
html = "<h1 id='parse'>Parser worked</h1>"
ele_id = parser.getElementById('phn')

# AdvancedHTMLParser.AdvancedTag.
ele_id = parser.getElementById('phn')