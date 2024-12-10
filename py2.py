import re
from flask import Flask, request, render_template_string
import ply.lex as lex
import ply.yacc as yacc
from difflib import get_close_matches

app = Flask(__name__)

# Définition des tokens
tokens = ('BISM', 'ALLAH', 'ALRAHMAN', 'ALRAHEEM')

# Expressions régulières pour les tokens
t_BISM = r'بسم'
t_ALLAH = r'الله'
t_ALRAHMAN = r'الرحمن'
t_ALRAHEEM = r'الرحيم'

# Ignorer les espaces et les diacritiques
t_ignore = ' \t\n'

# Fonction pour ignorer les diacritiques arabes
def t_ignore_TASHKEEL(t):
    r'[ًٌٍَُِّْ]'  # Regex pour les voyelles courtes
    pass

def t_SPACE(t):
    r'\s+'
    pass  # Ignore spaces

# Construire le lexer
lexer = lex.lex()

# Règles de syntaxe
def p_phrase(p):
    '''phrase : BISM ALLAH ALRAHMAN ALRAHEEM'''
    p[0] = "✅ النص صحيح: بسم الله الرحمن الرحيم"

# Gestion des erreurs syntaxiques
def p_error(p):
    if p:
        raise Exception(f"⛔ الكلمة '{p.value}' لي كتبتي فالپوزيشن {p.lexpos} مشي صحيحة.")
    raise Exception("⛔ النص ناقص، كمل الجملة!")

# Construire le parser
parser = yacc.yacc()

# Liste des mots corrects
mots_corrects = ["بسم", "الله", "الرحمن", "الرحيم"]

# Analyse de la chaîne
def analyser_chaine(texte):
    texte = re.sub(r'[ًٌٍَُِّْ]', '', texte)  # Nettoyer les diacritiques
    mots_entree = texte.split()

    # Vérification des mots incorrects
    for i, mot in enumerate(mots_entree):
        if mot not in mots_corrects:
            suggestions = get_close_matches(mot, mots_corrects, n=1, cutoff=0.8)
            if suggestions:
                return f"⛔ واش كنتي تقصد '{suggestions[0]}'؟"
            return f"⛔ الكلمة '{mot}' لي كتبتي فالپوزيشن {texte.index(mot)} ماخاصهاش تكون تماكة."

    # Vérification des mots en trop
    for mot in mots_entree:
        if mot not in mots_corrects:
            return f"⛔ الجملة خاطئة حيت زدت كلمات لي ما خاصهومش يكونو: {mot}"

    try:
        # Essayer d'analyser le texte
        result = parser.parse(texte)
        if result:
            return result
        else:
            return "⛔ ما لقيتش الجملة صحيحة!"
    except Exception as e:
        return str(e)
    
##verifier les caracteres en francais 
def is_lettrre_francais(mot):
    # Vérifier si le mot contient uniquement des lettres françaises (y compris les lettres accentuées)
    return bool(re.match(r'^[a-zA-ZéèàâêîôûçœÉÈÀÂÊÎÔÛÇŒ]+$', mot))

# Interface web avec Flask
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    texte = ""
    if request.method == "POST":
        texte = request.form.get("texte")
        if texte:
            result = analyser_chaine(texte)

    # Interface HTML
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تحليل الآية الأولى من سورة الفاتحة</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 50px;
                background-color: #f4f4f9;
            }
            textarea {
                width: 100%;
                height: 150px;
                font-size: 22px;
                direction: rtl;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #ccc;
                box-sizing: border-box;
            }
            button {
                font-size: 20px;
                padding: 15px 30px;
                margin-top: 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #45a049;
            }
            .result {
                margin-top: 20px;
                font-size: 24px;
                color: #333;
                margin-top: 40px;
            }
        </style>
    </head>
    <body>
        <h1>تحليل الآية الأولى من سورة الفاتحة</h1>
        <form method="POST">
            <textarea name="texte" placeholder="اكتب النص هنا..." >{{ texte }}</textarea><br>
            <button type="submit">تحليل</button>
        </form>
        <div class="result">{{ result }}</div>
    </body>
    </html>
    """
    return render_template_string(html, result=result, texte=texte)

if __name__ == "__main__":
    app.run(debug=True)
