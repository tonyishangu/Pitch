import unittest
from app.models import Pitch, User
from app import db

class TestPitch(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Pitches class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.user_Abuga = User(username = 'Abuga',password = 'ndizi', email = 'gmail@gmail.com')
        self.new_Pitch = Pitch(1234,'My pitch','Motivational','You can do it dont give up', user= self.user_Abuga)


    def tearDown(self):
            Review.query.delete()
            User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_Pitch,Pitch))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_Pitch.id,12345)
        self.assertEquals(self.new_Pitch.pitch_title,'My pitch')
        self.assertEquals(self.new_Pitch.pitch_description,"You can do it dont give up")
        self.assertEquals(self.new_Pitch.user_id,self.user_Abuga)

    def test_save_pitch(self):
        self.new_Pitch.save_pitch()
        self.assertTrue(len(Review.query.all())>0)

    def test_get_pitches(self):
        self.new_Pitch.save_pitch()
        got_Pitch = Pitch.get_pitches()
        self.assertTrue(len(got_reviews) == 1)