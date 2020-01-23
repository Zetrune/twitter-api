from flask_testing import TestCase
from app import create_app, db
from app.models import Tweet, User

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()
        first_user = User(username="First user", email="first@user.com", api_key="12345")
        db.session.add(first_user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_tweet_list(self):
        response = self.client.get("/users")
        response_user = response.json[-1]
        user_id = response_user["id"]
        first_tweet = Tweet(text="First tweet", user=user_id)
        db.session.add(first_tweet)
        second_tweet = Tweet(text="Second tweet", user=user_id)
        db.session.add(second_tweet)
        db.session.commit()
        response = self.client.get("/tweets")
        response_tweet = response.json
        print(response_tweet)
        first_tweet = response_tweet[0]
        second_tweet = response_tweet[1]
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_tweet, list)
        self.assertEqual(len(response_tweet), 2)
        self.assertEqual(first_tweet["text"], "First tweet")
        self.assertIsNotNone(first_tweet["created_at"])
        self.assertEqual(second_tweet["text"], "Second tweet")
        self.assertIsNotNone(second_tweet["created_at"])

    def test_tweet_empty_list(self):
        response = self.client.get("/tweets")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_tweet, list)
        self.assertEqual(len(response_tweet), 0)

    def test_tweet_show(self):
        response = self.client.get("/users")
        response_user = response.json[-1]
        user_id = response_user["id"]
        first_tweet = Tweet(text="First tweet", user=user_id)
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])

    def test_tweet_create(self):
        response = self.client.get("/users")
        response_user = response.json[-1]
        user_id = response_user["id"]
        response = self.client.post("/tweets", json={'text': 'New tweet!', 'user': user_id})
        created_tweet = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_tweet["id"], 1)
        self.assertEqual(created_tweet["text"], "New tweet!")

    def test_tweet_update(self):
        response = self.client.get("/users")
        response_user = response.json[-1]
        user_id = response_user["id"]
        first_tweet = Tweet(text="First tweet", user=user_id)
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.patch("/tweets/1", json={'text': 'New text', 'user': user_id})
        updated_tweet = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_tweet["id"], 1)
        self.assertEqual(updated_tweet["text"], "New text")

    def test_tweet_delete(self):
        response = self.client.get("/users")
        response_user = response.json[-1]
        user_id = response_user["id"]
        first_tweet = Tweet(text="First tweet", user=user_id)
        db.session.add(first_tweet)
        db.session.commit()
        self.client.delete("/tweets/1")
        self.assertIsNone(db.session.query(Tweet).get(1))
