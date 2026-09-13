from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///atrial.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Modelo do paciente
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    nascimento = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    observacoes = db.Column(db.Text)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pacientes/novo", methods=["GET", "POST"])
def cadastro_paciente():

    if request.method == "POST":

        nome = request.form["nome"]
        nascimento = request.form["nascimento"]
        cpf = request.form["cpf"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        observacoes = request.form["observacoes"]

        paciente = Paciente(
            nome=nome,
            nascimento=nascimento,
            cpf=cpf,
            telefone=telefone,
            email=email,
            observacoes=observacoes
        )

        db.session.add(paciente)
        db.session.commit()

        print("Paciente cadastrado com sucesso!")

    return render_template("cadastros.html")


@app.route("/pacientes")
def pacientes():

    pacientes = Paciente.query.all()

    return render_template("pacientes.html", pacientes=pacientes)


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)