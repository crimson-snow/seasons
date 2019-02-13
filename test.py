#!/usr/bin/env python3

import unittest
import seasons


class NamingSchemeTestCase(unittest.TestCase):

    testep = seasons.Episode('Dragon Ball Super',
                             5,
                             'dbs.s1.e5.mp4',
                             extension='mp4')

    def test_series_title(self):
        scheme = '{t} - S{s} E{e}'
        self.testep.makefilename(3, scheme)

        self.assertIn('Dragon Ball Super', self.testep.newfilename)

    def test_series_title_dots(self):
        scheme = '{t.dot} - S{s} E{e}'
        self.testep.makefilename(3, scheme)

        self.assertIn('Dragon.Ball.Super', self.testep.newfilename)

    def test_season_num(self):
        scheme = '{t.dot} - S{s} E{e}'
        self.testep.makefilename(3, scheme)

        self.assertIn('S3', self.testep.newfilename)

    def test_season_num_pad(self):
        scheme = '{t.dot} - S{s.pad} E{e}'
        self.testep.makefilename(3, scheme)

        self.assertIn('S03', self.testep.newfilename)

    def test_episode_num(self):
        scheme = '{t.dot} - S{s} E{e}'
        self.testep.makefilename(3, scheme)

        self.assertIn('E5', self.testep.newfilename)

    def test_episode_num_pad(self):
        scheme = '{t.dot} - S{s} E{e.pad}'
        self.testep.makefilename(3, scheme)

        self.assertIn('E05', self.testep.newfilename)


if __name__ == '__main__':
    unittest.main()
