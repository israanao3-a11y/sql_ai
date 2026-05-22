from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from models import (
    db,
    Produit,
    Stock
)

# =====================================================
# CONFIGURATION APPLICATION
# =====================================================

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:casa2%40%406@localhost:5432/"
    "stock_vetement?options=-csearch_path=cours_sql"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisation SQLAlchemy
db.init_app(app)

# =====================================================
# PAGE PRINCIPALE
# =====================================================

@app.route("/")
def index():

    produits = Produit.query.all()

    return render_template(
        "index.html",
        produits=produits
    )

# =====================================================
# RECEPTION STOCK
# =====================================================

@app.route(
    "/reception/<int:id_produit>",
    methods=["POST"]
)
def reception(id_produit):

    try:

        # Quantité entrée
        quantite_recue = int(
            request.form["quantite"]
        )

        # Recherche stock
        stock = Stock.query.filter_by(
            id_produit=id_produit
        ).first()

        # Vérification
        if stock is None:

            return "Stock introuvable"

        # Mise à jour stock
        stock.quantite_disponible = (
            stock.quantite_disponible
            + quantite_recue
        )

        # Validation transaction
        db.session.commit()

        return redirect(
            url_for("index")
        )

    except Exception as e:

        # Rollback transaction
        db.session.rollback()

        return f"Erreur : {str(e)}"

# =====================================================
# EXECUTION APPLICATION
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )