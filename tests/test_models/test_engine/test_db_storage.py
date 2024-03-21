import unittest
from unittest.mock import patch, MagicMock
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):

    @patch('os.getenv', return_value='test')
    @patch('sqlalchemy.create_engine')
    def test_init(self, mock_create_engine, mock_getenv):
        db = DBStorage()
        self.assertTrue(mock_getenv.called)
        self.assertTrue(mock_create_engine.called)

    @patch('sqlalchemy.orm.scoped_session')
    @patch('sqlalchemy.orm.sessionmaker')
    @patch('sqlalchemy.create_engine')
    @patch('os.getenv', return_value='test')
    def test_reload(self, mock_getenv, mock_create_engine, mock_sessionmaker, mock_scoped_session):
        db = DBStorage()
        db.reload()
        self.assertTrue(mock_create_engine.called)
        self.assertTrue(mock_sessionmaker.called)
        self.assertTrue(mock_scoped_session.called)

    @patch('sqlalchemy.orm.scoped_session')
    @patch('sqlalchemy.orm.sessionmaker')
    @patch('sqlalchemy.create_engine')
    @patch('os.getenv', return_value='test')
    def test_all(self, mock_getenv, mock_create_engine, mock_sessionmaker, mock_scoped_session):
        db = DBStorage()
        with patch.object(db, '_DBStorage__session') as mock_session:
            state = State(name='California')
            city = City(name='San Francisco')
            user = User(email='test@test.com')
            place = Place(name='My Place')
            review = Review(text='Great place!')
            amenity = Amenity(name='Wifi')
            mock_session.query.return_value.all.return_value = [state, city, user, place, review, amenity]

            states = db.all(State)
            cities = db.all(City)
            users = db.all(User)
            places = db.all(Place)
            reviews = db.all(Review)
            amenities = db.all(Amenity)

            self.assertIsNotNone(states)
            self.assertTrue(isinstance(states, list))
            self.assertNotIsInstance(cities, list)
            self.assertNotIsInstance(users, list)
            self.assertNotIsInstance(places, list)
            self.assertNotIsInstance(reviews, list)
            self.assertNotIsInstance(amenities, list)
            # self.assertEqual(len(states), 1)
            # self.assertEqual(len(cities), 1)
            # self.assertEqual(len(users), 1)
            # self.assertEqual(len(places), 1)
            # self.assertEqual(len(reviews), 1)
            # self.assertEqual(len(amenities), 1)

    # Add similar tests for new, save, delete methods

if __name__ == '__main__':
    unittest.main()
