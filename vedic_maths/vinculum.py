from manim import *
from numpy import array, sign
from common import *
import math

def vinc_str(x):
        return "\overline{" + str(abs(int(x))) + "}" if (int(x) < 0) else str(x)

def ut_vinc(scene, sn1, sn2,  move=(0, 0), wait=3, d_wait=1, explain=True, show_res=True,
       show_carry=True, play=True, fade=True, oplen=0):
    ''' Urdhvatiryagbhyam helper function '''
    def _explain():
        ''' Step explanation '''
        # Get the ordinal right - ix comes in starting with 0
        _ord = {0: "1st", 1: "2nd", 2: "3rd"}
        ord = _ord[ix] if ix in _ord else f"{ix+1}th"
        etext = [f"The <span color='Turquoise'>{ord}</span> partial product is: <span color='Turquoise'>{_pp}</span>.",
                 ]
        if c_p:
            etext.append(f"<span color='Turquoise'>{_pp}</span> + <span color='Turquoise'>{c_p_t}</span> (prev. carry) =  <span color='Turquoise'>{pp}</span>.")
        if ix==(nit-1):
            etext.append(f"We retain <span color='yellow'>{pp}</span> as the rest of the answer.")
        else:
            etext.append(f"We retain <span color='yellow'>{d}</span> as a  digit of the answer.")
            if c:
                etext.append(f"<span color='yellow'>{vinc_str(c)}</span> becomes the next carry.")

        el = [MarkupText(x, font="Cambria Math") for x in etext]
        eg = VGroup(*el).scale(0.5).arrange(DOWN, aligned_edge=LEFT).move_to(RIGHT*4)

        for _el in eg:
            scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
        scene.wait(2)
        return eg

    def _vf(n):
        vincD = find_vinc_form(scene, n)
        el = [vinc_str(x) for x in reversed(vincD)]
        eg = MathTex(*el, color="Cyan")
        return eg
    
    sr = int(sn1)*int(sn2) # Result
    sop = "×"

    n = max(len(str(sn1)), len(str(sn2)))
    n1 = MathTex(str(sn1).zfill(n), color=YELLOW).arrange(buff=0.5)
    n2 = MathTex(str(sn2).zfill(n), color=YELLOW).arrange(buff=0.5)

    
    # First pass, find max length of vinculum form
    vn1 = find_vinc_form(scene, sn1)
    vn2 = find_vinc_form(scene, sn2)
    n = max(len(vn1), len(vn2))
    nit = 2*n-1
    
    # Recompute with proper zero padding
    vn1 = list(reversed(find_vinc_form(scene, str(sn1).zfill(n))))
    vn2 = list(reversed(find_vinc_form(scene, str(sn2).zfill(n))))

    # Zero fill multiplier/multiplicand as necessary
    n11  =_vf(str(sn1).zfill(n))
    n21  = _vf(str(sn2).zfill(n))
    op = MarkupText(str(sop), font='Cambria Math')
    res = _vf(str(sr))  # Placeholder for later replacement
    res2 = MathTex(str(sr), color="Yellow") # Final result
    
    if oplen==0:
        oplen=res.width
    lr = len(str(sr)) # Length of result

    ln = Line(start=array([-1 * oplen, 0, 0]), end=array([0, 0, 0])).set_color(YELLOW)
    # First arrange as usual
    g1 = VGroup(n1, n2, ln, res).arrange(DOWN, aligned_edge=RIGHT)
    n1.next_to(n2, UP, buff=0.5, aligned_edge=RIGHT)  # Add some gap for ut lines
    g = VGroup(g1, op).arrange(RIGHT, aligned_edge=UP) # Final assembly
    g.move_to(UP * move[0] + RIGHT * move[1]) # move
    res2.next_to(res, DOWN*2, aligned_edge=RIGHT)
    n11.next_to(n1, ORIGIN, aligned_edge=RIGHT)
    n21.next_to(n2, ORIGIN, aligned_edge=RIGHT)
    
    if play:
        scene.play(FadeIn(n1, n2, ln, op))
        scene.wait(2)
        scene.play(Transform(n1, n11))
        scene.wait(1)
        scene.play(Transform(n2, n21))
        scene.wait(1)
        lines = None
        show = [] # Lines to display
        cl = []
        c = 0
        c_p = None
        for ix in range(nit):
            x = res[-1-ix]  # Reversed
            # Display ixth urdhvatiryagbhyam pattern
            lines, show, pp = utlines(scene, ix, n1, n2, vn1, vn2, lines, show)
            n1.set_color_with_tex(WHITE)
            n2.set_color_with_tex(WHITE)
            # Only the digits relevant for this pattern are
            # shown in yellow
            for s in show:
                n1[s].set_color_with_tex(YELLOW)
                n2[s].set_color_with_tex(YELLOW)
            # Previous result digit turned back to White
            if show_res and (ix > 0):  
                res[lr-ix].set_color_with_tex(WHITE)
            scene.wait(3)
            if c_p is not None:
                c_p.set_color_with_tex(GREY)
            _pp = pp # For display
            pp += c  # Previous carry
            #d = int(str(sr)[-1-ix])  # ixth digit of the answer
            d = sign(pp) * (abs(pp) - (abs(pp) // 10))
            #c = (pp - d) // 10
            c = sign(pp) * (abs(pp) // 10)
            if explain:
               eg =  _explain()
            if show_res:
                # Add current result digit in Yellow
                _x = MathTex(vinc_str(d))
                _x.next_to(x, ORIGIN)
                x.become(_x)
                scene.add(x.set_color_with_tex(YELLOW))

            # Display carry down and to the left
            # Not done for the last step, because if there's a carry
            # it just becomes an extra digit directly
            if show_res and show_carry and c and (ix!=(nit-1)):
                ct = MathTex(vinc_str(c)).scale(0.7).next_to(x, DOWN*0.5+LEFT*0.5)
                scene.add(ct)
                c_p = ct
                c_p_t = c
                cl.append(ct)
            # At the last step, display remaining digits of answer too
            if show_res and (ix==(nit-1)) and (lr>nit):
                scene.add(c).set_color_with_tex(YELLOW)
            scene.wait(d_wait)
            if explain:
                scene.play(FadeOut(eg))
        scene.remove(*lines)  # Remove last u line
        # Remove color emphasis
        n1.set_color_with_tex(WHITE)
        n2.set_color_with_tex(WHITE)
        if show_res:
            res.set_color_with_tex(WHITE)
            scene.wait(3)
            scene.add(res2)
        if show_carry:
            scene.remove(*cl)
        if wait:
            scene.wait(wait)
        if fade:
            if show_res:
                scene.play(FadeOut(g, res2))
            else:
                scene.play(FadeOut(n1, n2, ln, op))
    return g


def utlines(scene, ix, n1, n2, vn1, vn2, lines=None, show=[]):
    ''' Update and display connections for ixth urdhvatiryagbhyam pattern '''
    n = len(n1) # Length of inputs
    nit = 2*n-1  # Number of ut iterations
    # Initialize lines if required
    if lines is None:
        lines =  [Line(n2[i].get_top(), [n2[-1].get_top()[0], n1[-1].get_bottom()[1], n1[-1].get_bottom()[2]]).set_color(YELLOW) for i in range(n)]
    
    def _display(show):
        # list show is in the order of top vertices (eg: [5, 4, 3])
        # bottom vertices will be the same reversed (eg: [3, 4, 5])
        # We zip the two to get the connection iterator (eg [(3, 5), (4, 4), (5, 3)])
        cnxns = zip(reversed(show), show)
        for c in cnxns:
            # Update line connections to get each urdhvatiryagbhyam pattern
            lines[c[0]].put_start_and_end_on([n2[c[0]].get_top()[0], n2[c[0]].get_top()[1] + 0.05, n2[c[0]].get_top()[2]],
                                             [n2[c[1]].get_top()[0], n1[c[1]].get_bottom()[1] - 0.05, n1[c[1]].get_bottom()[2]])
            # This could have been (n2[c[0]].get_top(), [n2[c[1]].get_bottom())
            # However, we see some lines not looking "straight"

    def _pp(show):
        ''' Partial Product '''
        pp = 0
        cnxns = zip(reversed(show), show)
        for c in cnxns:
            pp += int(vn2[c[0]]) * int(vn1[c[1]])
        return pp
    
    if ix < n:
        # For the first n iterations, add one line, starting from the right
        scene.add(lines[n-1-ix])
        show.append(n-1-ix)  # Append added line to the show list
        # Update line display.
        # Connections will be modified based on the show list
        _display(show)
    elif ix < nit:
        # After the first n iterations
        rx = ix-n
        # Remove one line, starting from the first added
        # (Last line added never gets removed)
        scene.remove(lines[n-1-rx])  
        show.pop(0)  # Remove line from show list
        # Update line display
        # Connections will be modified based on the show list
        _display(show)
    pp = _pp(show)
    return lines, show, pp
  

def find_Norm_form(scene, num):
    # converting to Normal form
    vinc = False
    frag = ""
    vincD = []
    dig_lef_dec = False
    for s in num:
        frag = frag + s
        if int(s) < 0:
            if vinc == False:
                vinc = True
                vincD.append(str(10 + int(s)))
            else:
                vincD.append(str(9 + int(s)))
        else:
            if (vinc == True):
                vincD.append(str(int(s) - 1))
                dig_lef_dec = True
                frag = ""
                vinc = False
            else:
                vincD.append(str(int(s)))
    if dig_lef_dec == False:
        vincD.append("1")

    return vincD

def find_vinc_form(scene, num):
    # converting to vinculum form  as fragments
    vinc = False
    frag = ""
    vincD = []
    dig_lef_inc = False

    for s in num[::-1]:
        frag = frag + s
        if int(s) > 5:
            if vinc == False:
                vinc = True
                vincD.append(str(-1 * (10 - int(s))))
            else:
                vincD.append(str(-1 * (9 - int(s))))
        if (int(s)< 6):
            if (vinc == True):
                vincD.append(str(int(s) + 1))
                dig_lef_inc = True
                frag = ""
                vinc = False
            else:
                vincD.append(str(int(s)))
    if dig_lef_inc == False:
        vincD.append("1")
    return vincD

def ToNormal(scene, num):
    # Displaying num in Normal form
    # find_Norm_form - converts the number to normal form

    vincD = find_vinc_form(scene,num)
    el1 = ["\overline{" + str(abs(int(x))) + "}" if (int(x) < 0) else x for x in reversed(vincD)]
    eg1 = MathTex(*el1, color="Cyan")
    eg1.move_to(UP*2)

    scene.play(AddTextLetterByLetter(eg1, time_per_letter=1))
    scene.wait(3)

    #normD = find_Norm_form(scene, vincD)
    el = [x for x in num]
    eg = MathTex(*el, color="Yellow")
    eg.next_to(eg1, DOWN*2, aligned_edge=RIGHT)
    for e in reversed(eg):
        scene.add(e)
        scene.wait(2)

    scene.play(FadeOut(eg,eg1))
    return eg

def Tovinculum(scene, num):
    # Displaying the vinculum form
    # find_vinc_form - converts the num to vinculum form  as fragments
    vincD = find_vinc_form(scene, num)

    el1 = [x for x in num]
    eg1 = MathTex(*el1, color="Yellow")
    eg1.move_to(UP*2)

    scene.play(AddTextLetterByLetter(eg1, time_per_letter=1))
    scene.wait(3)

    el = ["\overline{" + str(abs(int(x))) + "}" if (int(x) < 0) else x for x in reversed(vincD)]
    eg = MathTex(*el, color="Cyan")
    eg.next_to(eg1, DOWN*2, aligned_edge=RIGHT)

    for e in reversed(eg):
        scene.add(e)
        scene.wait(2)
    scene.wait(3)
    scene.play(FadeOut(eg,eg1))
    return eg


def ut_vinc3dig(scene,sn1,sn2):
    ''' UT 3 Digit multiplication of Vinculum Numbers '''

    res= str(int(sn1)*int(sn2))
    t = DisplayText(scene, "Multiplication Example", scale=0.7, wait=0, move=(-2, 0),
                    fade=False, font='Cambria Math')

    el1 = [MathTex(x) for x in sn1[::-1]]
    eg1 = VGroup(*el1).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg1.next_to(t, LEFT*2 + DOWN*2)

    for _el1 in el1:
        scene.play(AddTextLetterByLetter(_el1, time_per_letter=1))
    scene.wait(1)


    el2 = [MathTex(x) for x in sn2[::-1]]
    eg2 = VGroup(*el2).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg2.next_to(eg1, DOWN)

    for _el2 in el2:
        scene.play(AddTextLetterByLetter(_el2, time_per_letter=1))
    scene.wait(1)

    ln1 = Line(start=array([0, 4,0]), end=array([2, 4, 0])).set_color(YELLOW)
    l1 = VGroup(ln1).arrange(RIGHT, aligned_edge=RIGHT)
    l1.next_to(eg1, DOWN*4)
    scene.add(l1)
    scene.wait(1)

    ans1 = [MathTex(x) for x in res[::-1]]
    ans1g = VGroup(*ans1).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    ans1g.next_to(l1, DOWN*2)

    for _ans1 in ans1:
        scene.play(AddTextLetterByLetter(_ans1, time_per_letter=1))
    scene.wait(1)

    vincD1 = find_vinc_form(scene,sn1)

    el3 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in vincD1]
    eg3 = VGroup(*el3).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg3.next_to(eg1, RIGHT*14)

    for _el3 in el3:
        scene.play(AddTextLetterByLetter(_el3, time_per_letter=1))
    scene.wait(1)

    vincD2 = find_vinc_form(scene,sn2)
    el4 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in vincD2]
    eg4 = VGroup(*el4).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg4.next_to(eg3, DOWN)

    for _el4 in el4:
        scene.play(AddTextLetterByLetter(_el4, time_per_letter=1))
    scene.wait(1)

    ln2 = Line(start=array([0,4,0]), end=array([2,4, 0])).set_color(RED)
    l2 = VGroup(ln2).arrange(RIGHT, aligned_edge=RIGHT)
    l2.next_to(eg3, DOWN*4)
    scene.add(l2)
    scene.wait(1)

    ans =[]
    ans.append(str(int(vincD1[0]) * int(vincD2[0])))
    ans.append(str((int(vincD1[0]) * int(vincD2[1])) + ((int(vincD1[1]) * int(vincD2[0])))))
    ans.append(str((int(vincD1[0]) * int(vincD2[2])) + (int(vincD1[1]) * int(vincD2[1])) + (int(vincD1[2]) * int(vincD2[0]))))
    ans.append(str((int(int(vincD1[1]) * int(vincD2[2])) + (int(vincD1[2]) * int(vincD2[1])))))
    ans.append(str(int(vincD1[2]) * int(vincD2[2])))

    el5 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in ans]
    eg5 = VGroup(*el5).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg5.next_to(l2, DOWN*2)

    for _el5 in el5:
        scene.play(AddTextLetterByLetter(_el5, time_per_letter=1))
    scene.wait(1)

    vincD = find_Norm_form(scene,ans)

    el6 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in vincD]
    eg6 = VGroup(*el6).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg6.next_to(eg5, DOWN*2)

    for _el6 in el6:
        scene.play(AddTextLetterByLetter(_el6, time_per_letter=1))
    scene.wait(1)

    scene.play(FadeOut(t,eg1, eg2, eg3, eg4,eg5,eg6,ans1g, l1, l2))
    return eg1

class Rekhitasamkhyaa(Scene):
    def construct(self):
        # Vinculum numbers  24 06 2022
        # Title

        Title(self, "रेखितसङ्ख्याः", "Vinculum Numbers", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)
        # Introduction

        text = [
            f"We all are familiar with +ve and -ve numbers.",
            f"Have you seen a number in which ",
            f"<span color = 'CYAN'>some digits are +ve and some are -ve?</span>",
            f"After all, what is the use of such a representation?",
            f"Quite interesting right?",
            f"Yes! Today's lesson is all about such special numbers."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"A number that is represented ",
            f"<span color ='YELLOW'>as partly positive and partly negative </span> is called a ",
            f"<span color = 'CYAN'>Vinculum Number or रेखितसङ्ख्या. </span>",
            f"A <span color = 'LIGHTCORAL'>vinculum </span> (overbar) is used to indicate <span color='ORANGE'>negative digits.</span>",
            f"This gives the number an easier form to deal with ",
            f"using the techniques that we learned before."
        ]
        e = Explanation(self, text,wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"How do we understand the value of the number <span color='CYAN'>18</span>? ",
            f" <span color='ORANGE' >10</span> + <span color='ORANGE'> 8</span> = <span color='CYAN'> 18</span>",
            f"Is there any other way to represent the value <span color='CYAN'> 18</span>?",
            f"Yes, one way is <span color='ORANGE' > 20</span> - <span color='ORANGE'>2</span> = <span color='CYAN'> 18 </span>",
            f"So, how can write that? " ]

        e1 = Explanation(self, text,font = "Cambria Math", wait=2, fade=False , aligned_edge=LEFT)

        t = Tex("We can write it as $2\overline{2}$", color="Cyan")

        t.next_to(e1, DOWN, aligned_edge=LEFT)
        self.wait(1)
        self.add(t)
        self.wait(5)

        self.play(FadeOut(e1))
        self.remove(e1)
        self.remove(t)
        self.wait(2)

        # Sutra Scene
        t0 = Span("निखिलं नवतश्चरमं दशत:")
        t1 = [Span("निखिलं नव त:, चरमं दश त:")]
        t2 = [Span("All from 9, last from 10 ")]
        Sutra(self, t0, t1, t2, wait=0, scale=0.65, move=None, fade=True, font='Cambria Math', dir1=DOWN, dir2=DOWN)
        self.wait(2)

        text = [
            f"To convert a number to <span color = 'CYAN'> vinculum</span> notation:",
            f"For every sequence of digits greater than 5,  ",
            f"Transform every digit using <span color ='YELLOW'>Nikhilam</span> method.",
            f"Add a  <span color = 'CYAN'> vinculum  (Overbar) </span>  to the transformed digits.",
            f"Increase the previous digit by 1.",
        ]
        e = Explanation(self, text, font='Cambria Math',wait=2, fade=True, aligned_edge=LEFT)

        t = DisplayText(self, "Let's see some Examples - Normal to Vinculum", scale=0.7, wait=0, move=(-3, -1),
                        fade=False, font='Cambria Math')

        Tovinculum(self, "38")
        Tovinculum(self, "68")
        Tovinculum(self, "3768")
        Tovinculum(self, "278186")

        self.play(FadeOut(t))

        text = [
            f"To convert a Vinculum number to <span color = 'CYAN'>Normal</span> Notation: ",
            f"For every sequence of vinculum digits,",
            f"Transform every digit using <span color ='YELLOW'>Nikhilam</span> method.",
            f"Remove the <span color = 'CYAN'> vinculum  (Overbar) </span>.",
            f"Reduce the previous digit by 1.",
        ]
        e = Explanation(self, text, font='Cambria Math', wait=2, fade=True, aligned_edge=LEFT)

        t = DisplayText(self, "Let's see some Examples -  Vinculum to Normal", scale=0.7, wait=0, move=(-3, -1),
                        fade=False, font='Cambria Math')

        ToNormal(self, "38")
        ToNormal(self, "68")
        ToNormal(self, "3768")
        ToNormal(self, "278186")

        self.play(FadeOut(t))

        text = [
            f"Why do we need the  <span color = 'CYAN'>Vinculum</span> notation? ",
            f"Sometimes we feel that mathematical operations ",
            f"with digits like 6,7,8,9 are a bit hard.",
            f"Digits upto 5 are easier to handle, especially mentally.",
            f"So, in the  <span color = 'CYAN'>Vinculum</span> form of numbers, these <span color='YELLOW'>digits >5</span> ",
            f"<span color='YELLOW'>are converted to face values of 4,3,2,1. </span>"
        ]
        e = Explanation(self, text, font='Cambria Math',wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If we have a clear idea about  <span color = 'YELLOW'>negative number handling</span>,",
            f" <span color = 'CYAN'>Vinculum</span> Numbers can really help us."
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"And please note that,",
            f"this is  <span color = 'ORANGE'>not strictly necessary</span> for any of the ",
            f"Vedic Mathematics methods. ",
            f"But it does <span color = 'LIGHTCORAL'> make things easier</span> in some cases."
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"Again, <span color = 'CYAN'>Vinculum</span> notation is useful when there are  <span color = 'YELLOW'>large digits.</span> ",
            f"If we convert them into vinculum digits,",
            f"mathematical operations becomes really easy ",
            f"as the <span color = 'YELLOW'>face value of the digits are decreased.</span>",
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        #ut_vinc3dig(self, "189","197")

        ut_vinc(self, "189", "197")
        
        self.next_section
