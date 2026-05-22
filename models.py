from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# =====================================================
# TABLE CATEGORIE
# =====================================================

class Categorie(db.Model):

    __tablename__ = "categorie"
    __table_args__ = {"schema": "cours_sql"}

    id_categorie = db.Column(
        db.Integer,
        primary_key=True
    )

    libelle_categorie = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    produits = db.relationship(
        "Produit",
        back_populates="categorie"
    )


# =====================================================
# TABLE FOURNISSEUR
# =====================================================

class Fournisseur(db.Model):

    __tablename__ = "fournisseur"
    __table_args__ = {"schema": "cours_sql"}

    id_fournisseur = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.String(100),
        nullable=False
    )

    telephone = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(100)
    )

    adresse = db.Column(
        db.Text
    )

    commandes = db.relationship(
        "Commande",
        back_populates="fournisseur"
    )


# =====================================================
# TABLE PRODUIT
# =====================================================

class Produit(db.Model):

    __tablename__ = "produit"
    __table_args__ = {"schema": "cours_sql"}

    id_produit = db.Column(
        db.Integer,
        primary_key=True
    )

    reference = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    libelle = db.Column(
        db.String(200),
        nullable=False
    )

    prix_vente = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    taille = db.Column(
        db.String(10)
    )

    couleur = db.Column(
        db.String(30)
    )

    id_categorie = db.Column(
        db.Integer,
        db.ForeignKey(
            "cours_sql.categorie.id_categorie"
        ),
        nullable=False
    )

    # Relations

    categorie = db.relationship(
        "Categorie",
        back_populates="produits"
    )

    stock = db.relationship(
        "Stock",
        back_populates="produit",
        uselist=False
    )

    lignes_commande = db.relationship(
        "LigneCommande",
        back_populates="produit"
    )

    # =====================================================
    # PROPRIETE ALERTE
    # =====================================================

    @property
    def est_en_alerte(self):

        if self.stock:

            return (
                self.stock.quantite_disponible
                < self.stock.seuil_minimum
            )

        return False


# =====================================================
# TABLE STOCK
# =====================================================

class Stock(db.Model):

    __tablename__ = "stock"
    __table_args__ = {"schema": "cours_sql"}

    id_stock = db.Column(
        db.Integer,
        primary_key=True
    )

    quantite_disponible = db.Column(
        db.Integer,
        default=0
    )

    seuil_minimum = db.Column(
        db.Integer,
        default=5
    )

    emplacement_rayon = db.Column(
        db.String(50)
    )

    id_produit = db.Column(
        db.Integer,
        db.ForeignKey(
            "cours_sql.produit.id_produit"
        ),
        nullable=False,
        unique=True
    )

    produit = db.relationship(
        "Produit",
        back_populates="stock"
    )


# =====================================================
# TABLE COMMANDE
# =====================================================

class Commande(db.Model):

    __tablename__ = "commande"
    __table_args__ = {"schema": "cours_sql"}

    id_commande = db.Column(
        db.Integer,
        primary_key=True
    )

    date_commande = db.Column(
        db.Date,
        nullable=False
    )

    statut = db.Column(
        db.String(50)
    )

    montant_total = db.Column(
        db.Numeric(10, 2)
    )

    date_livraison_prev = db.Column(
        db.Date
    )

    id_fournisseur = db.Column(
        db.Integer,
        db.ForeignKey(
            "cours_sql.fournisseur.id_fournisseur"
        ),
        nullable=False
    )

    fournisseur = db.relationship(
        "Fournisseur",
        back_populates="commandes"
    )

    lignes_commande = db.relationship(
        "LigneCommande",
        back_populates="commande"
    )


# =====================================================
# TABLE LIGNE_COMMANDE
# =====================================================

class LigneCommande(db.Model):

    __tablename__ = "ligne_commande"
    __table_args__ = {"schema": "cours_sql"}

    id_ligne = db.Column(
        db.Integer,
        primary_key=True
    )

    quantite_commandee = db.Column(
        db.Integer,
        nullable=False
    )

    prix_unitaire_achat = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    quantite_recue = db.Column(
        db.Integer,
        default=0
    )

    id_commande = db.Column(
        db.Integer,
        db.ForeignKey(
            "cours_sql.commande.id_commande"
        ),
        nullable=False
    )

    id_produit = db.Column(
        db.Integer,
        db.ForeignKey(
            "cours_sql.produit.id_produit"
        ),
        nullable=False
    )

    commande = db.relationship(
        "Commande",
        back_populates="lignes_commande"
    )

    produit = db.relationship(
        "Produit",
        back_populates="lignes_commande"
    )