from manim import *
from numpy import array

class OpeningScene(Scene):
    def construct(self):

        # Title Scene
        t0 = Text("परिपूरकम्")
        t1 = Text("Complement")
        tg = VGroup(t0,t1).arrange(direction=DOWN)
        self.add(tg)
        self.wait()
        self.play(tg.animate.scale(0.3).move_to(DOWN*3+RIGHT*6))
        self.next_section()

        # Definition
        el = [MarkupText(x) for x in ["A Complement Completes a Number",
                                "A <span foreground='yellow'>Number</span> and its <span foreground='orange'>Complement</span>",
                                "always add up to a power of 10"]]
        eg = VGroup(*el).scale(0.7).arrange(DOWN).move_to(LEFT)
        for _el in el:
            self.play(AddTextLetterByLetter(_el, time_per_letter=0.5))
        self.wait(3)
        self.play(eg.animate.move_to(UP*2.5))
        for k in [55, 90, 145, 270]:
            s = Sector(inner_radius=0, outer_radius=1, start_angle=0, angle=k * DEGREES, color=YELLOW)
            s1 = Sector(inner_radius=0, outer_radius=1, start_angle=k*DEGREES,
                        angle=(360-k) * DEGREES, color=ORANGE)
            self.play(s.animate)
            self.play(s1.animate)
            self.wait(2)
            self.play(FadeOut(s,s1))
        self.play(FadeOut(eg))
        self.next_section()
        
        
        # Sutra Scene
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
        self.wait(2)

        self.play(t1g[0].animate.set_opacity(0.25),
                  t2g[0].animate.set_opacity(0.25))
        self.play(t1g[1].animate.set_color(YELLOW),
                  t2g[1].animate.set_color(YELLOW).set_opacity(1))
        self.wait(2)
        t1g.set_opacity(1)
        t2g.set_opacity(1)
        self.wait(2)
        self.play(FadeOut(sg,t0))
        self.play(t1g.set_color(WHITE).animate.scale(0.5).move_to(RIGHT*5+UP*3))
        self.play(t2g.set_color(WHITE).animate.scale(0.5).move_to(RIGHT*5+UP*2.5))
        self.wait(1)

        self.next_section()
        # Explanation
        el = [Text(x) for x in ["To Calculate the Complement of a Number", "Subtract the last nonzero digit from 10", "And Subtract all digits to the left of it from 9"]]
        eg = VGroup(*el).scale(0.7).arrange(DOWN).move_to(LEFT)
        for _el in el:
            self.play(AddTextWordByWord(_el, time_per_word=0.5))
        self.wait(3)
        self.play(eg.animate.scale(0.4).move_to(RIGHT*5))
        
        self.next_section()
        
        # Example 1
        # 17, 83, 189, 320, 765432 , 58730, 982000
        titex = Text("Examples")
        self.play(Write(titex))
        self.wait(2)
        self.play(titex.animate.scale(0.7).move_to(UP*3+LEFT))
    
        examples = ["17", "83", "189", "320", "765432" , "58730", "982000"]
        
        def _show(num):
            l = len(num)
            # Text version of input
            t2 = Text(num).set_color(YELLOW).move_to(LEFT) # Calc
            t22 = Text(num).set_color(YELLOW) # Final Display
            
            # Horizontal line
            ln = Line(start=array([-1*l,0,0]), end=array([0,0,0])).set_color(YELLOW).next_to(t2, DOWN)

            # COmplement
            l9 = l - len(num.lstrip('9'))
            p = str(10**l - int(num))
            p0 = '0'*l9+p
            t3 = Text(p0).set_color(ORANGE).next_to(ln, DOWN)
            t33 = Text(p).set_color(ORANGE) #Final Display
            
            # 9s and 10
            # Trailing zeros
            lz = l - len(num.rstrip('0'))
            t = Text("9"*(l-lz-1)).scale(0.9)
            ts = "10"
            #if lz > 0:
            #    ts = ts+'0'*lz
            tt = Text(ts).scale(0.7)
            g1 = VGroup(t,tt).arrange(direction=RIGHT, buff=0.1).set_opacity(0.8).next_to(t2,
                                                                    UP, aligned_edge=LEFT)

            # Answer
            g2 = VGroup(t33, Text("is the complement of"), t22).arrange(RIGHT).next_to(t3, 2*DOWN)
            
            self.play(Write(t2))
            #self.play(Write(g1))
            self.play(FadeIn(ln))
            #self.play(Write(t3))
            self.play(AddTextLetterByLetter(t,time_per_char=0.2))
            self.play(AddTextLetterByLetter(tt, time_per_char=0.2))
            self.play(AddTextLetterByLetter(t3,time_per_char=1))
            self.play(FadeIn(g2))
            
            self.wait(4)
            self.play(FadeOut(t2,g1,ln,t3, g2))
                      
        for num in examples:
            _show(num)
        self.wait(5)

