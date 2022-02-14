from manim import *
from numpy import array

# Helper Function for Title
def Title(scene, t0, t1, wait=5, scale=0.3, move=(3, 6)):
    # Title Scene
    t0 = Text(t0)
    t1 = Text(t1)
    tg = VGroup(t0,t1).arrange(direction=DOWN)
    scene.add(tg)
    scene.wait(wait)
    scene.play(tg.animate.scale(scale).move_to(move[0]*DOWN+move[1]*RIGHT))
    return tg

# Helper function for multi-line explanation
def Explanation(scene, text, wait=3, fade=True):
    # Explanation
    el = [MarkupText(x) for x in text]
    eg = VGroup(*el).scale(0.7).arrange(DOWN)
    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
    if wait:
        scene.wait(wait)
    if fade:
        scene.play(FadeOut(eg))
    return eg

# Helper function to display text message
def DisplayText(scene, text, scale=1, move=(0, 0), wait=5, fade=True):
    t = MarkupText(text).scale(scale)
    scene.play(FadeIn(t.move_to(move[0]*DOWN+move[1]*RIGHT)))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(t))
    return t


# Helper function for Sutra display
# Inputs
#     sutra     - Sutra string
#     viccheda  - List of sandhi split segments
#   translation - List of translation segments, matching viccheda
def Sutra(scene, sutra, viccheda, translation, wait=3, scale=0.5, move=(3, 5), fade=False):
    sg = VGroup(Text("सूत्रम्"), Text("विच्छेदः"), Text("Translation")).arrange(direction=DOWN, aligned_edge=RIGHT).set_color(BLUE).set_opacity(0.5)
    #t0 = Text("निखिलं नवतश्चरमं दशतः")
    #t1 = [Text("निखिलं नवतः "), Text("चरमं दशतः")]
    #t2 = [Text("All from 9, "), Text("Last from 10")]
    t0 = MarkupText(sutra)
    t1 = [MarkupText(x) for x in viccheda]
    t2 = [MarkupText(x) for x in translation]
    assert len(viccheda) == len(translation), "Sandhi split (viccheda) and translation must be of equal length"
    t1g = VGroup(*t1).arrange(direction=RIGHT).set_opacity(0)
    t2g = VGroup(*t2).arrange(direction=RIGHT).set_opacity(0)
    tg = VGroup(t0, t1g, t2g).arrange(direction=DOWN)

    tg.move_to(UP+RIGHT)
    sg.next_to(tg, LEFT)

    scene.play(FadeIn(sg))
    scene.play(Write(t0.set_color(ORANGE)))
    scene.wait()
    scene.play(t1g.animate.set_opacity(1))
    for i in range(len(translation)):
        scene.play(t1g[i].animate.set_color(YELLOW),
                  t2g[i].animate.set_color(YELLOW).set_opacity(1))
        scene.wait(5)

        scene.play(t1g[i].animate.set_opacity(0.25),
                  t2g[i].animate.set_opacity(0.25))
    t1g.set_opacity(1)
    t2g.set_opacity(1)
    scene.wait(3)
    scene.play(FadeOut(sg,t0))
    if move is not None:
        scene.play(t1g.set_color(WHITE).animate.scale(0.5).move_to(move[0]*UP+move[1]*RIGHT))
        scene.play(t2g.set_color(WHITE).animate.scale(0.5).move_to((move[0]-0.5)*UP+move[1]*RIGHT))
        scene.wait(1)
    elif fade:
        scene.play(FadeOut(t1g, t2g))
    return (t1g, t2g)


# Helper Function for Nikhilam
def NikhilamExample(scene, num):
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
    tt = Text(ts).scale(0.7)
    g1 = VGroup(t,tt).arrange(direction=RIGHT, buff=0.1).set_opacity(0.8).next_to(t2,
                                                            UP, aligned_edge=LEFT)

    # Answer
    g2 = VGroup(t33, Text("is the complement of"), t22).arrange(RIGHT).next_to(t3, 2*DOWN)

    scene.play(Write(t2))
    scene.play(FadeIn(ln))
    scene.play(AddTextLetterByLetter(t,time_per_char=0.2))
    scene.play(AddTextLetterByLetter(tt, time_per_char=0.2))
    scene.play(AddTextLetterByLetter(t3,time_per_char=1))
    scene.play(FadeIn(g2))

    scene.wait(4)
    scene.play(FadeOut(t2,g1,ln,t3, g2))

        
# Helper function for subtraction example
def SubExample(scene, num1, num2):
        op = Text("-")
        op1 = Text("+")
        sn1 = str(num1)
        sn2 = str(num2)
        # Number lengths
        len1 = len(sn1)
        len2 = len(sn2)
        dlen = abs(len1-len2)
        mlen = max(len1, len2)
        lenz = len2 - len(sn2.rstrip('0'))
        len9 = len2-1-lenz
        
        # Prepend shorter number with 0s
        if len1 > len2:
            sn2 = "0"*dlen + sn2
        elif len2 > len1:
            sn1 = "0"*dlen + sn1
            
        # Setup minuend, subtrahend, complement and answer
        #n1 = Text("91234").set_color(GREEN)
        n1 = Text(sn1).set_color(GREEN) 
        d1 = Text("Minuend").set_color(GREEN) 
        #n2 = Text("18765").set_color(YELLOW)
        n2 = Text(sn2).set_color(YELLOW)
        d2 = Text("Subtrahend").set_color(YELLOW) 
        n3 = Text("?")
        #ans = "172469"
        if num1 >= num2:
            # Positive answer
            ans = "1" + str(num1-num2)
            posans = True
        else:
            # Negative answer
            ans = str(10**mlen - (num2-num1))
            posans = False
            
        res = Text(ans)
        ln = Line(start=array([-1*2,0,0]), end=array([0,0,0])).set_color(YELLOW)
        g1 = VGroup(n1, n2, ln, n3).arrange(DOWN, aligned_edge=RIGHT).move_to(UP*2)
        g = VGroup(g1, op).arrange(RIGHT, aligned_edge=UP)
        op.next_to(n1, RIGHT)
        g2 = VGroup(d1, d2).arrange(DOWN).next_to(g, LEFT, aligned_edge=UP, buff=1)
        
        #nik = MarkupText("9999<span size='small'>10</span>")
        nik = MarkupText('9'*len9 + "<span size='small'>10</span>")
        n2c = n2.copy()
        lnc = ln.copy()
        g3  = VGroup(nik, n2c, lnc).arrange(DOWN, aligned_edge=LEFT)
        cmpl = Text(str(10**mlen - num2)).set_color(ORANGE)
        cmplc = cmpl.copy()
        ct  = Text("Complement of Subtrahend").scale(0.5).set_color(ORANGE)
        
        scene.play(FadeIn(g))
        scene.play(FadeIn(g2))
        DisplayText(scene, "Subtract these numbers", wait=3, move=(-3, 0))
        #scene.wait(2)
        scene.play(FadeOut(g2))
        scene.play(g.animate.move_to(LEFT*2))
        scene.play(FadeIn(g3.next_to(g, RIGHT, buff=1, aligned_edge=UP)))
        DisplayText(scene, "1. Find the complement of the <span color='yellow'>Subtrahend</span>", scale=1, wait=2, move=(-3, 0))
        scene.play(AddTextLetterByLetter(cmpl.next_to(g3, DOWN, aligned_edge=LEFT), time_per_char=0.3))
        scene.play(FadeIn(ct.next_to(cmpl, RIGHT)))
        pos = n2.get_center()
        opos = op.get_center()
        DisplayText(scene, "2. Add the complement to the Minuend", wait=3, move=(-3, 0))
        scene.play(FadeOut(n2), FadeOut(op), FadeIn(cmplc.move_to(pos)), FadeIn(op1.move_to(opos)))
        scene.play(FadeOut(n3))
        scene.play(FadeIn(res.next_to(ln, DOWN, aligned_edge=RIGHT)))
        scene.wait(3)
        if posans:
            fb = SurroundingRectangle(res[0], buff=0.1)
            scene.play(Create(fb))
            DisplayText(scene, "If the result has an extra digit of 1, the answer is positive", scale=0.5, wait=3, move=(2,-2))
            DisplayText(scene, "Drop the extra 1 to get the final answer", scale=0.5,  wait=3, move=(2,-2))
            #scene.wait(2)
            scene.play(res[0].animate.set_opacity(0.3))
            scene.play(FadeOut(fb))
            DisplayText(scene, f"Answer is {ans[1:]}", wait=5, move=(3,-2))
        else:
            DisplayText(scene, "If the result does not have an extra digit, it is negative", scale=0.5, wait=3, move=(2,-2))
            DisplayText(scene, "The complement of the result is the absolute value of the answer", scale=0.5, wait=3, move=(2,-2))
            DisplayText(scene, f"Answer is -{10**mlen - int(ans)}", wait=5, move=(3,-2))
        
        #scene.wait(5)
        scene.remove(n1, ln, g3, op1, cmpl, ct, cmplc, res)

        
class Nikhilam(Scene):
    def construct(self):

        # Title Scene
        Title(self, "परिपूरकम्", "Complement")
        self.next_section()

        # Definition
        el = ["A Complement Completes a Number",
              "A <span foreground='yellow'>Number</span> and its <span foreground='orange'>Complement</span>",
              "always add up to a power of 10"]
        eg = Explanation(self, el, wait=3)
        self.play(eg.animate.move_to(UP*2.5))
        for k in [55, 90, 145, 270]:
            s = Sector(inner_radius=0, outer_radius=1, start_angle=0, angle=k * DEGREES, color=YELLOW)
            s1 = Sector(inner_radius=0, outer_radius=1, start_angle=k*DEGREES,
                        angle=(360-k) * DEGREES, color=ORANGE)
            self.play(s.animate)
            self.play(s1.animate)
            self.wait(3)
            self.play(FadeOut(s,s1))
        self.play(FadeOut(eg))
        self.next_section()
        
        
        # Sutra Scene
        t0 = "निखिलं नवतश्चरमं दशतः"
        t1 = ["निखिलं नवतः ", "चरमं दशतः"]
        t2 = ["All from 9, ", "Last from 10"]
        Sutra(self, t0, t1, t2, wait=3, scale=0.5, move=(3, 5), fade=False)
        self.next_section()

        # Explanation
        el = ["To Calculate the Complement of a Number", "Subtract the last nonzero digit from 10", "And Subtract all digits to the left of it from 9"]
        eg = Explanation(self, el, wait=5)
        self.play(eg.animate.scale(0.4).move_to(RIGHT*5))
        self.next_section()
        
        # Example 1
        # 17, 83, 189, 320, 765432 , 58730, 982000
        titex = Text("Examples")
        self.play(Write(titex))
        self.wait(3)
        self.play(titex.animate.scale(0.7).move_to(UP*3+LEFT))
    
        examples = ["17", "83", "189", "320", "765432" , "58730", "982000"]
        for num in examples:
           NikhilamExample(self, num)
        self.wait(5)

class Subtraction(Scene):
    def construct(self):
        # Title
        Title(self, "परिपूरकेण व्यवकलनम्", "Subtraction using Complement", move=(3,5), wait=1)
        self.next_section()
        # Introduction
        text = ["Application of Complement",
                "Subtraction without the pain of borrowing!"]
        Explanation(self, text)
        self.next_section()
        # Revision and Example

        # Explanation
        eg = DisplayText(self, "Revision", fade=True)
        self.next_section()

        # Sutra Scene
        t0 = "निखिलं नवतश्चरमं दशतः"
        t1 = ["निखिलं नवतः ", "चरमं दशतः"]
        t2 = ["All from 9, ", "Last from 10"]
        Sutra(self, t0, t1, t2, wait=3, scale=0.5, move=None, fade=True)
        self.next_section()
        # Explanation
        el = ["To Calculate the Complement of a Number", "Subtract the last nonzero digit from 10", "And Subtract all digits to the left of it from 9"]
        eg = Explanation(self, el, wait=2, fade=True)
        self.next_section()
    
        NikhilamExample(self, "6583200")
        self.next_section()
  
        eg = DisplayText(self, "How do we use this for subtraction?", fade=True)
        self.next_section()
        
        # Explanation
        text = ["To subtract a number",
                "Compute the complement of the subtrahend using निखिलं",
                "Add it to the minuend",
                "This removes the need to borrow"]
        Explanation(self, text)
        self.next_section()

        # Detailed Example
        SubExample(self, 91234,18765)
        self.next_section()
        # Detailed Example - Negative Answer
        SubExample(self, 14569,69875)
        self.next_section()
