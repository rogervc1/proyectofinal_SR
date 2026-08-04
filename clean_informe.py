import re

with open('Iinforme_tex/informe.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace all **text** with \textbf{text}
text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)

# 2. Remove '\textit{Análisis Técnico}: ' prefix in Section 4
text = text.replace(r'\textit{Análisis Técnico}: ', '')
text = text.replace(r'\textit{Análisis Técnico}:', '')

with open('Iinforme_tex/informe.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print("¡Reemplazos realizados con éxito en Iinforme_tex/informe.tex!")
