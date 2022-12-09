from pyfiglet import Figlet
from sty import fg, rs

class GradientText:
    def __init__(self, color: str, text: str, style: str):
        """ Gradient text function using pyfiglet and sty libraries.

        Args:
            color (str): color of the gradient text - Available Colors: red, green, blue, yellow, purple, orange, pink, white, black
            text (str): text to be displayed
            style (str): style of the text - Full list of styles can be found here: https://gist.githubusercontent.com/livxy/9217adc886134788032764d627f7fe51/raw/bfd75781e07981d3a40ca41244800e7940f13fb1/fonts.txt  -  Also see https://devhints.io/figlet for viusal examples of the styles
        """
        self.color = color
        self.text = text
        self.style = style

    def gradient_text(self):
        """ 
        Gradient text function using pyfiglet and sty libraries.
        """
        f = Figlet(font=self.style)
        for i, line in enumerate(f.renderText(self.text).splitlines()):
            if self.color == "red": 
                print(fg(255 - i * 10, 0, 0) + line + rs.all)
            elif self.color == "green":
                print(fg(0, 255 - i * 10, 0) + line + rs.all)
            elif self.color == "blue":
                print(fg(0, 0, 255 - i * 10) + line + rs.all)
            elif self.color == "yellow":
                print(fg(255 - i * 10, 255 - i * 10, 0) + line + rs.all)
            elif self.color == "purple":
                print(fg(255 - i * 10, 0, 255 - i * 10) + line + rs.all)
            elif self.color == "orange":
                print(fg(255 - i * 10, 100 - i * 10, 0) + line + rs.all)
            elif self.color == "pink":
                print(fg(255 - i * 10, 0, 100 - i * 10) + line + rs.all)
            elif self.color == "white":
                print(fg(255 - i * 10, 255 - i * 10, 255 - i * 10) + line + rs.all)
            elif self.color == "black":
                print(fg(0, 0, 0) + line + rs.all)
            else:
                print(fg(255 - i * 10, 0, 255 - i * 10) + line + rs.all)
        return ""