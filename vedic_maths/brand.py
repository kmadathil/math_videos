from manim import *
from numpy import array
from common import *

class GanitamLogo(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        logo_b = MAROON_E
        logo_f = GOLD_E
        ga = Text("ग", color=logo_f).scale(6.0)
        circle = Circle(color=logo_b, radius=4, fill_opacity=1)
        logo = VGroup(circle, ga)
        logo.move_to(ORIGIN)
        self.add(logo)


class GanitamBanner(Scene):
    def construct(self):
        self.camera.background_color = MAROON_E
        logo_f = GOLD_E
        ga = Paragraph("बहुभिर्विप्रलापै: किं त्रैलोक्ये सचराचरे।", 
                       "यत्किंचिद्वस्तु तत्सर्वं गणितेन विना न हि॥",
                       "What more needs to be said?",
                       "Nothing exists without mathematics.",
                       color=logo_f,
                       line_spacing=1.25).scale(0.35)
        self.add(ga)



