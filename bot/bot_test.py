import unittest
import bot


class BotTest(unittest.TestCase):
    def test_check_url(self):
        bot.url = "http://some.url.local"
        bot.search_string = "any"
        check = bot.check_url()
        self.assertEqual(check, 1)

    def test_check_timeout(self):
        bot.url = "http://yandex.ru"
        bot.search_string = "randomstring"
        bot.connection_timeout = (1, 0.001)
        check = bot.check_url()
        self.assertEqual(check, 1)

if __name__ == '__main__':
    unittest.main()
