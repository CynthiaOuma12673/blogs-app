from app.models import Blog,User
from app import db
import unittest

class BlogTest(unittest.TestCase):

    def setUp(self):
        self.user_Cynthia = User(username = 'CynthiaOuma',password = 'test', email = 'oumacynthia817.com')
        self.new_blog = Blog(title="Family",post= "A family is all about being together",user = self.user_Cynthia )
            
    def tearDown(self):
        Blog.query.delete()
        User.query.delete()
            
    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.title,"Family")
        self.assertEquals(self.new_blog.post,"A family is all about being together")
        self.assertEquals(self.new_blog.user,self.user_Cynthia)
        
    def test_save_blog(self):
        self.new_blog.save_review()
        self.assertTrue(len(Blog.query.all())>0)