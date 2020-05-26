from unittest.mock import patch 

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # Simulate DB available behavior
        # Retrieve Default DB via Connection Handler
        # Mock Behavior
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # override return_value
            gi.return_value = True
            # monitor how many times it was called and the different calls made to it 
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # Same as with patch('blah') ,speeds up the test waiting 
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # make it raise the Operational Error 5 times, then correct on 6th try
            # called 6 times
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)


