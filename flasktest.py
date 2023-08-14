from unittest import TestCase
from flask_webtest import TestApp
from main import app, db

class ExampleTest(TestCase):
    def setUp(self):
        self.app = app
        self.w = TestApp(self.app, db=db, use_session_scopes=True)

    def test(self):
        r = self.w.get('/')
        # Assert there was no messages flushed:
        self.assertFalse(r.flashes)
        # Access and check any variable from template context...
        self.assertEqual(r.context['text'], 'Hello!')
        self.assertEqual(r.template, 'template.html')
        # ...and from session
        self.assertNotIn('user_id', r.session)

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/user/<int:id>/')
def user(id):
    return User.query.get_or_404(id).greet()

@app.route('/user/<int:id>/preview/', methods=['POST'])
def preview(id):
    user = User.query.get_or_404(id)
    user.greeting = request.form['name']
    # Expunge `user` from the session so that we can
    # call `db.session.commit` later and do not change
    # user data in table
    db.session.expunge(user)
    return user.greet()


class Test(TestCase):
    def setUp(self):
        self.w = TestApp(self.app)
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test(self):
        user = User(name='Mohan')
        db.session.add(user)
        db.session.commit()
        r = self.w.get('/user/%i/' % user.id)
        self.assertEqual(r.body, 'Hello, Mohan!')
