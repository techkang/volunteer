# -*- coding:utf-8 -*-
import os
import volunteer
import unittest
import tempfile

class VolunteerTestClass(unittest.TestCase):
    def setUp(self):
        self.db_fd, volunteer.app.config['DATABASE'] = tempfile.mkstemp()
        volunteer.app.testing=True
        self.app=volunteer.app.test_client()
        with volunteer.app.app_context():
            volunteer.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(volunteer.app.config['DATABASE'])

    def test_empty_db(self):
        rv=self.app.get('/')
        assert '新社员报名' in rv.data

    def register_new(self,stdnum,name,sex,email,phone,info):
        self.app.post('/new',data=dict(
            stdnum=stdnum,
            name=name,
            sex=sex,
            email=email,
            phone=phone,
            info=info
        ),follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/manager', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_register_and_login(self):
        self.register_new('PB15123456','tech康','male','ksc@mail.ustc.edu.cn',
                         '17730222022','我爱学习，学习爱我')
        rv = self.login('admin', 'default')
        assert '我爱学习，学习爱我' in rv.data
        rv = self.logout()
        assert '新社员报名' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data


if __name__=='__main__':
    unittest.main()