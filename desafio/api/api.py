from flask import Flask, redirect, url_for, request, render_template
import cryp
import os
import sys

app = Flask(__name__)
app.config["DEBUG"] = True

crypt = cryp.Cryp()
AC = None
if os.path.exists("AC_certificate.pem"):
    AC = cryp.ACRoot(crypt.import_pem_key_file("private.pem"))

@app.route('/', methods=['GET']) # main page
def home():
    return '''
<html>
   <body style="background-color:rgb(173, 216, 230)">
      <div style="background-color:rgb(187, 235, 250)">
          <h1 style="text-align:center;"> PARABENS, VOCE LOGOU</h1>
          <p style="text-align:center;"> --------------------------------------------------------------------------- </p>
      </div>
      <div style="background-color:rgb(173, 216, 230)">
          <form action = "http://127.0.0.1:5000/resumo_crypto" method = "POST">
             <h3 style="text-align:left;"> Resumo criptográfico </h3>
             <p style="text-align:left;">input de texto:</p>
             <p style="text-align:left;"><input type = "text" name = "doc" /></p>
             <p style="text-align:left;"><input type = "submit" value = "obter resumo criptográfico" /></p>
          </form>
      </div>
      <div style="background-color:rgb(173, 216, 230)>
          <h3 style="text-align:left;"> gerar par de chaves RSA:</h3>
          <form action = "http://127.0.0.1:5000/RSA1024" method = "GET">
             <p><input type = "submit" value = "1024" /></p>
          </form>
          <form action = "http://127.0.0.1:5000/RSA2048" method = "GET">
             <p><input type = "submit" value = "2048" /></p>
          </form>
      </div>
      <form action = "http://127.0.0.1:5000/create_root" method = "GET">
         <p> </p>
         <h3><input type = "submit" value = "criar AC_raiz" /></h3>
      </form>
      <form action = "http://127.0.0.1:5000/create_signed_certificate" method = "POST">
         <p> </p>
         <h3> Gerar x509 assinado pela AC_raiz </h3>
         <h4>Subject:</h4>
         <p> * formato(separado por espaços): País Estado Companhia
         <p><input type = "text" name = "subject" /></p>
         <p><input type = "submit" value = "submeter para AC-raiz" /></p>
      </form>
      <form action = "http://127.0.0.1:5000/list_subject" method = "POST">
         <h3> listar certificados </h3>
         <p><input type = "submit" value = "por subject" /></p>
      </form>
      <form action = "http://127.0.0.1:5000/list_serial" method = "POST">
         <p><input type = "submit" value = "por serial_number" /></p>
      </form>
   </body>
</html>'''

@app.route('/resumo_crypto', methods=['POST'])
def resumo_crypto():
    documento = request.form['doc']
    out = crypt.generate_crypt_resume(documento)
    return '''
<html>
   <body>
      <form action = "http://127.0.0.1:5000/" method = "GET">
         <p>Resumo criptográfico:</p>
         <h>''' + out + '''</h>
         <p><input type = "submit" value = "voltar" /></p>
      </form>
   </body>
</html>'''


@app.route('/RSA1024', methods=['GET', 'POST'])
def RSA1024():
    crypt.generate_RSA_pair(1024)
    file = open("private.pem", "rU")
    # key = crypt.import_pem_key_file("mykey.pem")
    priv_key = file.read()
    file = open("public.pem", "rU")
    # key = crypt.import_pem_key_file("mykey.pem")
    publ_key = file.read()
    return '''
<html>
   <body>
      <form action = "http://127.0.0.1:5000/" method = "GET">
         <p>chaves criadas:</p>
         <h>''' + priv_key + '''</h>
         <p></p>
         <h>''' + publ_key + '''</h>
         <p><input type = "submit" value = "voltar" /></p>
      </form>
   </body>
</html>'''

@app.route('/RSA2048', methods=['GET', 'POST'])
def RSA2048():
    crypt.generate_RSA_pair(2048)
    file = open("private.pem", "rU")
    priv_key = file.read()
    file = open("public.pem", "rU")
    publ_key = file.read()
    return '''
<html>
   <body>
      <form action = "http://127.0.0.1:5000/" method = "GET">
         <p>chaves criadas:</p>
         <h>''' + priv_key + '''</h>
         <p></p>
         <h>''' + publ_key + '''</h>
         <p><input type = "submit" value = "voltar" /></p>
      </form>
   </body>
</html>'''

@app.route('/create_root', methods=['GET','POST'])
def create_root():
    global AC
    private_key = crypt.import_pem_key_file('private.pem')
    AC = cryp.ACRoot(private_key)
    cert = AC.certificado
    a, b, c = cryp.get_cert_info(cryp.get_cert("AC_certificate.pem"))
    return '''
<html>
   <body>
      <form action = "http://127.0.0.1:5000/" method = "GET">
         <h3>subject:</h3>
         <h>''' + a + '''</h>
         <h3>serial_number:</h3>
         <h>''' + b + '''</h>
         <h3>issuer:</h3>
         <h>''' + c + '''</h>
         <p><input type = "submit" value = "voltar" /></p>
      </form>
   </body>
</html>'''

@app.route('/create_signed_certificate', methods=['GET','POST'])
def create_signed_certificate():
    subject = request.form['subject']
    global AC
    cert = AC.gera_cert(subject)
    return '''
<html>
   <body>
      <form action = "http://127.0.0.1:5000/" method = "GET">
         <h3>success</h3>
         <p><input type = "submit" value = "voltar" /></p>
      </form>
   </body>
</html>'''

@app.route('/list_serial', methods=['GET','POST'])
def list_serial():
    out = ""
    lista = cryp.list_certificates(2)
    for i in range(len(lista)):
        out += lista[i] + "/------------------------/"
    return '''
<html>
   <body>
      <form action = "http://127.0.0.1:5000/" method = "GET">
         <h3>listado por serial</h3>
         <h>'''+out+'''<h>
         <p><input type = "submit" value = "voltar" /></p>
      </form>
   </body>
</html>'''

@app.route('/list_subject', methods=['GET','POST'])
def list_subject():
    out = ''
    lista = cryp.list_certificates(1)
    for i in range(len(lista)):
        out += lista[i] + "/------------------------/"
    return '''
<html>
   <body>
      <form action = "http://127.0.0.1:5000/" method = "GET">
         <h3>listado por subject</h3>
         <h>'''+out+'''<h>
         <p><input type = "submit" value = "voltar" /></p>
      </form>
   </body>
</html>'''


if __name__ == '__main__':
   app.run(debug = True)
