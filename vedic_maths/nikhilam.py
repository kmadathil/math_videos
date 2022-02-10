from manim import *

class OpeningScene(Scene):
    def construct(self):
        t0 = Text("परिपूरकम्")
        t1 = Text("Complement")
        tg = VGroup(t0,t1).arrange(direction=DOWN)
        self.add(tg)
        self.wait()
        self.play(tg.animate.scale(0.3).move_to(DOWN*3+RIGHT*6))
        self.next_section()

        sg = VGroup(Text("सूत्रम्"), Text("विच्छेदः"), Text("Translation")).arrange(direction=DOWN, aligned_edge=RIGHT).set_color(BLUE).set_opacity(0.5)
        t0 = Text("निखिलं नवतश्चरमं दशतः")
        t1 = [Text("निखिलं नवतः "), Text("चरमं दशतः")]
        t2 = [Text("All from 9, "), Text("Last from 10")]
        t1g = VGroup(*t1).arrange(direction=RIGHT).set_opacity(0)
        t2g = VGroup(*t2).arrange(direction=RIGHT).set_opacity(0)
        tg = VGroup(t0, t1g, t2g).arrange(direction=DOWN)

        tg.move_to(UP+RIGHT)
        sg.next_to(tg, LEFT)
        
        self.play(FadeIn(sg))
        self.play(Write(t0.set_color(ORANGE)))
        self.wait()
        self.play(t1g.animate.set_opacity(1))
        self.play(t1g[0].animate.set_color(YELLOW),
                  t2g[0].animate.set_color(YELLOW).set_opacity(1))
        self.wait(4)

        self.play(t1g[0].animate.set_opacity(0.25),
                  t2g[0].animate.set_opacity(0.25))
        self.play(t1g[1].animate.set_color(YELLOW),
                  t2g[1].animate.set_color(YELLOW).set_opacity(1))
        self.wait(2)
        t1g.set_opacity(1)
        t2g.set_opacity(1)
        self.wait(2)
        self.play(FadeOut(sg,tg))
        self.wait(5)
