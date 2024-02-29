from flask_sqlalchemy import SQLAlchemy

###############################################################################

db = SQLAlchemy()
#OntologyViaPortal(db.Model)

class UploadedOntology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, file_path, upload_date):
        self.file_path = file_path
        self.upload_date = upload_date

    def __repr__(self):
        return f"<UploadedOntology {self.id}>"

#######################################

class OntologyViaURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semantic_artefact_URL = db.Column(db.String(255), nullable=False)
    semantic_artefact_domain = db.Column(db.String(255), nullable=False)  # New field
    semantic_artefact_version = db.Column(db.String(255), nullable=False)
    evaluation_date = db.Column(db.DateTime, nullable=False)
    ofaire_score = db.Column(db.Float, nullable=True)
    fairchecker_score = db.Column(db.Float, nullable=True)
    foops_score = db.Column(db.Float, nullable=True)

    def __init__(self, semantic_artefact_URL, semantic_artefact_domain, semantic_artefact_version, evaluation_date,
                 ofaire_score=None, fairchecker_score=None, foops_score=None):
        self.semantic_artefact_URL = semantic_artefact_URL
        self.semantic_artefact_domain = semantic_artefact_domain  # New field
        self.semantic_artefact_version = semantic_artefact_version
        self.evaluation_date = evaluation_date
        self.ofaire_score = ofaire_score
        self.fairchecker_score = fairchecker_score
        self.foops_score = foops_score

    def __repr__(self):
        return f"<OntologyViaURL {self.id}>"

#######################################

class OntologyViaPortal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portal_name = db.Column(db.String(255), nullable=False)
    semantic_artefact_acronym = db.Column(db.String(255), nullable=False)
    semantic_artefact_domain = db.Column(db.String(255), nullable=False)  # New field
    semantic_artefact_version = db.Column(db.String(255), nullable=False)
    evaluation_date = db.Column(db.DateTime, nullable=False)
    ofaire_score = db.Column(db.Float, nullable=True)
    fairchecker_score = db.Column(db.Float, nullable=True)
    foops_score = db.Column(db.Float, nullable=True)

    def __init__(self, portal_name, semantic_artefact_acronym, semantic_artefact_domain, semantic_artefact_version,
                 evaluation_date, ofaire_score=None, fairchecker_score=None, foops_score=None):
        self.portal_name = portal_name
        self.semantic_artefact_acronym = semantic_artefact_acronym
        self.semantic_artefact_domain = semantic_artefact_domain  # New field
        self.semantic_artefact_version = semantic_artefact_version
        self.evaluation_date = evaluation_date
        self.ofaire_score = ofaire_score
        self.fairchecker_score = fairchecker_score
        self.foops_score = foops_score

    def __repr__(self):
        return f"<OntologyViaPortal {self.id}>"

#######################################

class OntologyEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=True)
    portal_name = db.Column(db.String(255), nullable=True)
    semantic_artefact_acronym = db.Column(db.String(255), nullable=True)
    semantic_artefact_URL = db.Column(db.String(255), nullable=True)
    semantic_artefact_domain = db.Column(db.String(255), nullable=False)  # New field
    semantic_artefact_version = db.Column(db.String(255), nullable=False)
    evaluation_date = db.Column(db.DateTime, nullable=False)
    ofaire_score = db.Column(db.Float, nullable=True)
    fairchecker_score = db.Column(db.Float, nullable=True)
    foops_score = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)

    def __init__(self, source=None, portal_name=None, semantic_artefact_acronym=None,
                 semantic_artefact_URL=None,semantic_artefact_domain=None, semantic_artefact_version=None,
                 evaluation_date=None, ofaire_score=None, fairchecker_score=None, foops_score=None,
                 user_id=None):
        self.source = source
        self.portal_name = portal_name
        self.semantic_artefact_acronym = semantic_artefact_acronym
        self.semantic_artefact_URL = semantic_artefact_URL
        self.semantic_artefact_domain = semantic_artefact_domain
        self.semantic_artefact_version = semantic_artefact_version
        self.evaluation_date = evaluation_date
        self.ofaire_score = ofaire_score
        self.fairchecker_score = fairchecker_score
        self.foops_score = foops_score
        self.user_id = user_id

    def __repr__(self):
        return f"<OntologyEvaluation id={self.id}, " \
               f"semantic_artefact_acronym={self.semantic_artefact_acronym}, " \
               f"semantic_artefact_acronym={self.semantic_artefact_URL}, " \
               f"semantic_artefact_domain={self.semantic_artefact_domain}, " \
               f"semantic_artefact_version={self.semantic_artefact_version}, " \
               f"evaluation_date={self.evaluation_date}, " \
               f"ofaire_score={self.ofaire_score}, " \
               f"fairchecker_score={self.fairchecker_score}, " \
               f"foops_score={self.foops_score}, " \
               f"user_id={self.user_id}>"

###############################################################################
