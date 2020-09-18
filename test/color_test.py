import unittest
from com.shotchart.shots.shot_colors import ShotColors
import codecs


class TestColor(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_color(self):
        sc = ShotColors()
        bad_colors = ["#EFE600", "#178A35", "#EFE600"]
        result = {}
        for k, v in sc.maristas_colors.items():
            color = int(codecs.encode(k)[1:], 16)
            bc = int(codecs.encode("#EFE600")[1:], 16)
            subs = abs(color - bc)
            result[k] = subs
            print(f"k: {k} - k(int): {color} - v: {bad_colors[0]} v(int): {bc} - resta: {subs}")
        ordered = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
        print(f"ordered: {ordered}")
        print(f"color: {next(iter(ordered.keys()))}")
