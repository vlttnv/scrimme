from scrimme import db

class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    steam_id = db.Column(db.String(40), unique=True)
    nickname  = db.Column(db.String(80))
    avatar_url = db.Column(db.String(80))
    profile_url = db.Column(db.String(80))
    avatar_url_full = db.Column(db.String(80))
    join_date = db.Column(db.DateTime)
    last_online = db.Column(db.DateTime)
    is_merc = db.Column(db.Integer)
    is_mentor = db.Column(db.Integer)
    last_updated = db.Column(db.String(45))
    skill_level = db.Column(db.String(80))
    main_class = db.Column(db.String(45))
    note = db.Column(db.Text)
    region = db.Column(db.String(45))
    availability = db.Column(db.String(100))

    # Relationship
    # memberships             = db.relationship('Membership',
    #         backref='member',
    #         lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)