## les fonctions sont importe automatiquement en important les libarys
from flask import Flask, request, render_template_string
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# Définition des tokens
tokens = ('BISM', 'ALLAH', 'ALRAHMAN', 'ALRAHEEM')

t_BISM = r'بِسْمِ'
t_ALLAH = r'اللَّهِ'
t_ALRAHMAN = r'الرَّحْمَٰنِ'
t_ALRAHEEM = r'الرَّحِيمِ'

t_ignore = ' \t\n'

def t_error(t):
    return f"Erreur lexicale : caractère inconnu '{t.value[0]}' à la position {t.lexpos}"

def t_SPACE(t):
    r'\s+'
    pass  # Ignore spaces

lexer = lex.lex()

# Grammaire
def p_phrase(p):## p_ est predefinie dans yacc donc automatiquement lorsque yacc voir fonction commence par p_  .Alors il va connaitre qu'il s'agit d'une phrase a verifier l'ordre des mots dans une phrase 
    '''phrase : BISM ALLAH ALRAHMAN ALRAHEEM'''##ici on defini la phrase a verifier et on a automatiquement p[1]= BISM et p[2]=ALLAH grace au yacc
    # et on a alors la verification d'apres les expressions regulieres il fait la correspondace automatiquemnent avec les tokens BISM dans la list tokens de lex voir faw9 dessus 
    #et apres on a le correspondance aux expressions regulier qui commence par t_BISM
    p[0] = "Syntaxe correcte : بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"## le yacc met automatiquement le p comme un tableau et alors p[0] prend le resultat si la phrase est correcte en ordre des mots sinon il gener un erreur 
##eN RESUME  cette fonction est pour verifier l'ordre ### et c'est la valeur que notre 
def p_error(p):
    if p:  # Si le token problématique existe
        raise Exception(f"Erreur syntaxique : mot inattendu '{p.value}' à la position {p.lexpos}")# hada lexical verifie tokens 7rouf
    else:  # Si la chaîne est incomplète
        raise Exception("Erreur syntaxique : Fin de chaîne inattendue.")#hada syntaxique qui verifie si il y a plus a ajouter


parser = yacc.yacc()### ici  on crre notre analyeur syntaxique  qui va utiliser tous les fonctions commencants par p_ 

# Fonction pour analyser la chaîne
def analyser_chaine(texte):##c'est un fonction qu'on va l'appler apres il est pris du formulaire dans l'interface web kijibou men tamak chouf code ta3  #interface web avec flask on a texte = request.form.get("texte") 
    try:
        result = parser.parse(texte)##notre anlyseur qui est objet et il a des fonction ,  verifie l'ordre de  texte en se basant sur ce qu'on a fait dans p_phrase et p_errotr par la fonction parse(texte) utilise par parser qu'on a cree par ycc.yacc()
        if result:#bach madokhch parse c'est analyse , donc  il retourne une phrase, 
            return result
    except Exception as e:
        return f"Erreur : {e}"

# Interface web avec Flask
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        texte = request.form.get("texte")###ici ou on definie texte  pour prendre de le texte l'input pour la fonction analyser_chaine(texte)
        if texte:
            result = analyser_chaine(texte)## ici le texte si il est retoune avec succes donc il sera anlyser  syntaxiquement  et retourne la valeur de l'analyse result soit erreru en basant sur p_erreur 

    # Interface HTML
    html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Analyseur Lexical et Syntaxique</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
            textarea { width: 100%; height: 100px; font-size: 18px; direction: rtl; }
            button { font-size: 18px; padding: 10px 20px; margin-top: 20px; }
            .result { margin-top: 20px; font-size: 20px; color: green; }
        </style>
    </head>
    <body>
        <h1>تحليل الآية الأولى من سورة الفاتحة</h1>
        <form method="POST">
            <textarea name="texte" placeholder="اكتب النص هنا..."></textarea><br>
            <button type="submit">تحليل</button>
        </form>
        <div class="result">{{ result }}</div> <!--ici ou on a la valeur de result= anlayser_chaine(texte)=yacc.yacc().parse(texte)=soit la valeur de p_phrase  p[0]=syntax correcte ou p_error la valeur de -->
    </body>
    </html>
    """
    return render_template_string(html, result=result) ## cette fonction est predefinie par  flask il contient les phrases d'erreur comme Erreur scanning error

if __name__ == "__main__":

  app.run(debug=True)

    ## traduction 
    ## audio 
