from django.test import TestCase
from envirocon.statefulgame.views import format_data, de_html


class TestHelpers(TestCase):
    def test_format_data(self):
        r = format_data(dict(foo='bar'))
        self.assertEqual(r, dict(foo='bar'))

        data = dict(foo=dict(author="bar"))
        r = format_data(data)
        self.assertEqual(r, dict())

        data = dict(foo=dict(blah="bar"))
        r = format_data(data)
        self.assertEqual(r, dict(blah="bar"))

    def test_de_html(self):
        s = dict()
        self.assertEqual(de_html(s), s)

        s = "foo"
        self.assertEqual(de_html(s), s)

        s = u"foo"
        self.assertEqual(de_html(s), s)

        s = u"foo<bar>baz"
        self.assertEqual(de_html(s), "foobaz")

        # as written, it doesn't process non-unicode
        s = "foo<bar>baz"
        self.assertEqual(de_html(s), "foo<bar>baz")
