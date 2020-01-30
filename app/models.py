from app import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(40), index=True)
    song_name = db.Column(db.String(100), index=True)
    source = db.Column(db.String(50), index=True)
    source_type = db.Column(db.Integer, index=True)
    times = db.Column(db.String(20), index=True)
    throughout = db.Column(db.Integer, index=True)
    answer = db.relationship('Answer', backref='song', lazy='select', uselist=True)
    
    def __repr__(self):
        return f"ID: {self.id} - Artist: '{self.artist}' - Song:'{self.song}' - Answer: '{self.answer}'"

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(40), index=True)
    song_name = db.Column(db.String(65), index=True)
    source = db.Column(db.String(50), index=True)
    source_type = db.Column(db.Integer, index=True)
    answers = db.Column(db.String(1000))
    times = db.Column(db.String(20), index=True)
    throughout = db.Column(db.Integer, index=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
