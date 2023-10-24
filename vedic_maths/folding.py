from manim import *
from manim.camera.camera import Camera
from numpy import array
from common import *
from division import vinc_int, vinc_str, vinc_list, MT
import math

class FoldingOp:
    def __init__(self, scene, num, divisor, fold_gen=19, fold_multiplier=2) -> None:
        self.scene = scene
        self.num = num
        self.fold_t = num
        self.e_num = MT(num, color="Yellow")
        self.fold_gen = fold_gen
        self.og = MT(fold_gen, color="Yellow")
        self.multiplier = vinc_int(fold_multiplier)
        self.e_mult = MathTex(fold_multiplier, color="Yellow")
        self.divisor = divisor
        self.e_divisor = MT(divisor, color="Yellow")
        self.div_fact = int(fold_gen/divisor)
        self.n_folds = 0

    def idisplay(self, wait = 4):
        ''' Initial display of folding '''
        t00=MarkupText(f"Is {Span(self.num, color='yellow')} divisible by {Span(self.divisor, color='yellow')} ?")
        self.scene.add(t00)
        self.scene.wait(2)
        t01= MarkupText(f"We note that {self.divisor} x {self.div_fact} = {self.fold_gen}")
        t01.next_to(t00, DOWN, buff=1)
        self.scene.add(t01)
        self.scene.wait(wait)
        #g0 = VGroup(Text("Folding Generator = ").scale(0.7), self.og).arrange(RIGHT)
        g0 = VGroup(Text("Multiplier Generator = ").scale(0.7), self.og).arrange(RIGHT)
        t1 = Text(f"Folding Multiplier = ").scale(0.7)
        gm = VGroup(t1, self.e_mult).arrange(RIGHT)
        gd = VGroup(g0, gm).arrange(DOWN)
        t2 = Text("Fold: ").scale(0.7)
        gn = VGroup(t2, self.e_num).arrange(RIGHT)
        gt = VGroup(gn, gd).arrange(DOWN, buff=1)
        self.scene.play(ReplacementTransform(t00,gn))
        self.scene.play(t01.animate.become(g0))
        self.scene.play(FadeIn(gm, shift=DOWN))
        self.scene.wait(2)
        self.scene.play(FadeOut(t01))
        self.scene.play(gm.animate.shift(DOWN))
        self.scene.play(gn.animate.arrange(DOWN).shift(UP))
        self.scene.wait(2)
        self.g0 = gn
        self.g1 = gm
        return gn, gm
    
    def fold(self, wait=4):
        ''' One folding step '''

        nd = (self.fold_t % 10)* self.multiplier
        self.fold_t = int(self.fold_t/10) + nd
        o = Text("+")
        tl = [x for x in str(self.fold_t)]
        t = MathTex(*tl, color="Yellow")
        ndm = MathTex(nd)
        self.scene.play(self.g0[1][-1].animate.next_to(self.g0[1][-2], DOWN))
        t.next_to(self.g0[1][-1], DOWN, aligned_edge=RIGHT)
        o.next_to(self.g0[1][-2], RIGHT)
        ndm.next_to(t, UP, aligned_edge=RIGHT)
        self.scene.play(Indicate(self.g0[1][-1]))   
        self.scene.play(Indicate(self.g1[-1]))
        self.scene.play(Transform(self.g0[1][-1], ndm))
        self.scene.add(t, o)
        self.scene.wait(4)
        self.scene.remove(self.g0[1][-1], o)
        self.g0[1].become(t)
        self.scene.play(self.g0.animate.arrange(DOWN).shift(UP))
        self.scene.remove(t)
        self.scene.wait(wait)
        self.n_folds += 1

    def clear(self):
        self.scene.remove(self.g0, self.g1)

    def end(self):
        assert (((self.fold_t % self.divisor) == 0) == ((self.num % self.divisor) == 0))
        if self.n_folds == (self.divisor - 1):
            assert ((self.fold_t % self.divisor) == (self.num % self.divisor))
        self.scene.remove(self.g1)
        dp = Span("divisible by", color="springGreen") if (self.fold_t % self.divisor) == 0 else Span("not divisible by", color="Red")
        t = f"{Span(self.fold_t, color='Yellow')} is {dp} {Span(self.divisor, color='Yellow')}, and therefore so is {Span(self.num, color='Yellow')}"
        g = DisplayText(self.scene, t, scale=0.7, move=(2, 0), wait=2, fade=True)
        self.scene.remove(self.g0)


def lastscene(self):
    
    titleL1 = DisplayText(self,
            Span("Thank you for watching this video.", color="yellow"), scale=0.7, wait=1,
            move=(-2.5, -1), fade=False)
    titleL2 = DisplayText(self,
                Span("Please let us know your feedback by your Likes and Comments.", color="yellow"),
                        scale=0.6, wait=2, move=(-1.5, -1),fade=False)
    titleL2 = DisplayText(self,
            Span("Share the video with your friends too.",
            color="yellow"),scale=0.6,wait=3, move=(-1, -1), fade=False)

    titleL3 = DisplayText(self,
                              Span("Do Subscribe to our Channel and press the Bell Icon!", color="yellow"),
                              scale=0.6, wait=2, move=(0, -1),
                              fade=False)

    self.wait(3)
    self.play(FadeOut(titleL3, titleL2, titleL1))

class Folding(Scene):
    def construct(self):


        Title(self, "वेष्टनम्", "Folding", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)

        text = [
            f"The term <span color='yellow'>Divisibility Test</span> is very familiar to us.",
            f"We are proficient in performing",
            f"divisibility tests of any number by 2, 3 and 5.",
            f"In our previous videos we used <span color='yellow'>Digitsum</span> " ,
            f"to check whether a number is  <span color='cyan'>divisible by 9.</span>",
            f"We also learned that  <span color='yellow'>ekadasha shesha</span> can be used ",
            f"to check whether a number is  <span color='cyan'>divisible by 11.</span>"
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"Today we learn a new technique, <span color='cyan'>Folding,</span>",
            f"to check the  <span color='yellow'>divisibility</span> by <span color='yellow'>any number.</span>",
            f"We will learn to check whether or not",
            f"a number, called <span color='cyan'>Dividend</span>, <span color='yellow'> is divisible by</span>",
            f"another number, called the<span color='cyan'> Divisor</span>."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)


        text = [
            f"Let's see the procedure in detail.",
            f"To begin with, we find a  <span color='yellow'>multiple</span> of the <span color='yellow'>Divisor</span>",
            f"that is <span color='yellow'>less or greater by 1</span> than a <span color='yellow'>multiple of 10.</span>",
            f"We will call this the <span color='cyan'>Multiplier Generator.</span>"
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        title_h1 = DisplayText(self, Span("Examples for ", color="white") + Span("Multiplier Generator:", color="yellow"),
                               scale=0.8, wait=0, move=(-3, -1), fade=False)

        text = [
            f"If the Divisor is <span color='cyan'>7</span>, the Multiplier Generator can be<span color='cyan'> 21 or 49.</span>"
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If the Divisor is <span color='cyan'>9</span>, the Multiplier Generator is <span color='cyan'>9.</span>"
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If the Divisor is <span color='cyan'>11</span>, the Multiplier Generator is <span color='cyan'>11.</span>"
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If the Divisor is <span color='cyan'>13</span>, the Multiplier Generator is <span color='cyan'>39.</span>"
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        self.play(FadeOut(title_h1))

        text = [
            f"The next step is finding the <span color='cyan'>Folding Multiplier</span>",
            f"For this, the <span color='cyan'>multiple of 10</span> that is adjacent to",
            f"the <span color='yellow'>mutiplier generator,</span> <span color='cyan'>is divided by 10.</span>",
            f"If the <span color='yellow'>multiplier generator ends in 1</span>,",
            f"the Folding multiplier is the <span color='yellow'>negative</span> of this result.",
            f"If the <span color='yellow'>multiplier generator ends in 9</span> ",
            f"the result itself is the Folding multiplier."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        title_h1 = DisplayText(self, Span("Examples for ", color="white") + Span("Folding multiplier:", color="yellow"),
                               scale=0.8, wait=0, move=(-3, -1), fade=False)

        text = [
            f"If the Multiplier Generator is <span color='cyan'>21</span>, the Folding Multiplier is <span color='cyan'>-2</span>."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If the Multiplier Generator is <span color='cyan'>49</span>, the Folding Multiplier is <span color='cyan'>5</span>."
                ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If the Multiplier Generator is <span color='cyan'>9</span>, the Folding Multiplier is <span color='cyan'>1</span>."
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If the Multiplier Generator is <span color='cyan'>11</span>, the Folding Multiplier is <span color='cyan'>-1</span>.",
             ]

        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If the Multiplier Generator is <span color='cyan'>39</span>, the Folding Multiplier is <span color='cyan'>4</span>."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        self.play(FadeOut(title_h1))
         

        text = [
            f"Now we can start <span color='yellow'>Folding</span> the number:",
            f"We take out the <span color='yellow'>last digit</span> of the dividend.",
            f"This digit is <span color='cyan'>multiplied</span> by the <span color='yellow'>Folding Multiplier</span>",
            f"and the <span color='cyan'>product is added</span> with rest of the digits."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

         
        text = [
            f"We repeat this Folding process",
            f"until we obtain a <span color='cyan'>single digit</span>",
            f"or a <span color='cyan'>number already seen</span> is obtained(a loop),",
            f"or a <span color='cyan'>known multiple of the Divisor</span> is found."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)
        

        """
        text = [
            f"At any stage of Folding process,",
            f"the Divisor, or its multiples ",
            f"may be <span color='cyan'>“cast out” (subtracted)</span> from the result",
            f"if it makes the process easy."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)
        """

        text = [
            f"So, how does our divisibility test conclude?",
            f"If a <span color='yellow'>multiple of the divisor</span> (positive or negative)",
            f"or <span color='yellow'>zero</span> is found in the process,",
            f"then the Dividend is <span color='springgreen'>divisible</span> by the Divisor.",
            f"Otherwise, <span color='red'>it is not.</span>",
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"Does this work for any Divisor?",
            f"<span color='springgreen'>It does</span> for any <span color='yellow'>Odd Divisor</span> that is not a multiple of 5.",
            f"If the <span color='yellow'>Divisor</span> is a multiple of <span color='yellow'>2 or 5</span>,",
            f"we can divide both Divisor and Dividend by those,",
            f"and perform the same folding process to check the divisibility."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)
        self.wait(2)
         
        n = 533
        d = 13
        f = FoldingOp(self, n, d, d*3, 4)
        t0, t1 = f.idisplay(4)
        self.wait(1)
        f.fold()
        self.wait(1)
        f.fold()
        f.end()
        self.wait(1)

        n = 948
        d = 7
        f = FoldingOp(self, n, d, d*3, -2)
        t0, t1 = f.idisplay(4)
        self.wait(1)
        f.fold()
        self.wait(1)
        f.fold()
        f.end()
        self.wait(1)

        """
        n = 1712
        d = 13
        f = FoldingOp(self, n, d, d*3, 4)
        t0, t1 = f.idisplay(4)
        self.wait(1)
        f.fold()
        self.wait(1)
        f.fold()
        self.wait(1)
        f.fold()
        f.end()
        self.wait(1)
        """

        self.next_section()
        lastscene(self)






class Reciprocal():
    ''' Class for Reciprocal calculation'''
    def __init__(self, scene, numerator, denominator, multiplier = None) -> None:
        self.scene = scene
        assert numerator<10
        self.numerator = numerator
        self.denominator = denominator
        if multiplier is None:
            multiplier = int((denominator+1)/10)
        self.multiplier = multiplier
        self.last_digit = self.numerator
        self.carry = 0

    def display(self, wait=5):
        '''Initial display'''
        frac = MathTex("\\frac{"+str(self.numerator)+"}{"+str(self.denominator)+"}", color="Yellow")
        e = Text(" = ")
        z = MathTex("0.", color="Yellow")
        t = Text("...")
        n = MathTex(str(self.numerator), color="Yellow")
        ng = VGroup(n).arrange(LEFT)
        self.cg = VGroup(MathTex("0", color="Black")).arrange(LEFT)   # Carry Group
        self.tg = VGroup(frac, e, z, t, ng).arrange(RIGHT)

        self.mg = VGroup(VGroup(Text("Multiplier:").scale(0.6), MathTex(self.multiplier, color="cyan")).arrange(RIGHT))
        self.tg.shift(UP)
        self.mg.next_to(self.tg, DOWN, buff=1)
        self.cg.next_to(self.tg[-1], UP, aligned_edge=RIGHT)
        self.scene.play(FadeIn(self.tg))
        self.scene.wait(5)
        self.scene.play(FadeIn(self.mg))
        self.scene.add(self.cg)
        self.scene.wait(6)
        return self.tg, self.mg
    
    def end(self, wait=5):
        '''We are done, remove the ... symbol'''
        self.scene.play(Indicate(self.tg[-1][0]))
        self.scene.play(Indicate(self.tg[-1][-1]))
        self.tg[-1][-1].set_color(GREY)
        self.scene.remove(self.cg)
        self.scene.wait(2)
        self.tg1 = VGroup(*self.tg[0:3].copy(), self.tg[4][0:-1].copy(), self.tg[3].copy()).arrange(RIGHT)
        self.tg1.shift(UP)
        self.scene.play(Transform(self.tg, self.tg1))
        self.scene.wait(wait)
        self.scene.wait(6)

    def step(self, wait=3):
        '''Single Step
        
           Calculate current digit * multiplier + carry
           The LSB of this becomes the next digit and the rest become the 
           next carry
        '''
        if len(self.mg) == 1:
            self.mg.add(MathTex(str(self.last_digit), color="Yellow"))
            self.mg.add(MathTex(str(self.multiplier*self.last_digit), color="Yellow"))
            self.mg.arrange(DOWN, aligned_edge=RIGHT)
            self.x = Text("×").scale(0.7)
            self.eq = Text("=").scale(0.7)
            #self.scene.play(self.mg.animate.next_to(self.tg, RIGHT, buff=2))
            self.mg.next_to(self.tg, DOWN, buff=1)
            self.x.next_to(self.mg[0], RIGHT)
            self.eq.next_to(self.mg[2], LEFT)
            self.scene.add(self.x, self.eq)
            self.scene.wait(3)
        else:
            self.mg[-2].become(self.tg[-1][-1])
            self.scene.wait(4)
            t = MathTex(str(self.multiplier*self.last_digit), color="Yellow")
            self.mg[-1].become(t)
            self.mg.arrange(DOWN, aligned_edge=RIGHT)
            self.mg.next_to(self.tg, DOWN, buff=1)
            self.x.next_to(self.mg[0], RIGHT)
            self.eq.next_to(self.mg[2], LEFT)
        self.scene.wait(4)
        self.last_digit = self.multiplier * self.last_digit + self.carry
        self.carry = int(self.last_digit/10)
        self.last_digit = self.last_digit % 10
        self.tg[-1].add(MathTex(str(self.last_digit), color="Yellow"))
        self.tg[-1].arrange(LEFT)
        self.tg.arrange(RIGHT)
        self.tg.shift(UP)
        self.mg.next_to(self.tg, DOWN, buff=1)
        self.x.next_to(self.mg[0], RIGHT)
        self.eq.next_to(self.mg[2], LEFT)
        # Carries
        # Zeros are not shown but kept for alignment
        cm = MathTex(self.carry, color="Grey" if self.carry else "Black")   
        self.cg.add(cm)
        self.cg.arrange(LEFT)
        for ix, _c in enumerate(self.cg):
            _c.next_to(self.tg[-1][ix], UP, aligned_edge=RIGHT)
        self.scene.play(Indicate(self.mg[2]))
        self.scene.play(Indicate(self.tg[-1][-1]))
        if self.carry:
            self.scene.play(Indicate(self.cg[-1]))
        self.scene.wait(wait)
        end_p = ((self.last_digit == self.numerator) and (self.carry == 0))
        return end_p
    
    def clear(self): 
        ''' Clear the scene'''
        self.scene.remove(self.tg, self.mg, self.x, self.eq)

    def step_all(self, wait = 3):
        ''' Run all necessary steps after initiation'''
        self.display(wait) 
        # Max steps = denominator - 1
        for i in range(self.denominator-1):
            e = self.step(wait)
            # End detected, break
            if e:
                break    
        self.end(wait)
        self.clear()

class Reciprocals(Scene):
    def construct(self):

        Title(self, "विपर्यस्तगणनम्", "Reciprocals", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)

        text = [
            f"In this video,",
            f"we are learning a simple technique to write the",
            f"<span color='cyan'>Decimal Form</span> of the <span color='yellow'>reciprocal of any number</span> that <span color='yellow'>ends in 9.</span>",
            f"We use the sutra <span color='cyan'>एकाधिकेन पूर्वेण</span> for this."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"The <span color='cyan'>decimal form</span> of the <span color='yellow'>reciprocal of any number</span> that <span color='yellow'>end in 9</span>",
            f"will always be a <span color='yellow'>repeating sequence of digits.</span>",
            f"In this process, we start with <span color='yellow'>last digit</span> of the answer",
            f"and calculate the <span color='yellow'>previous digits</span> and continue the process",
            f"until we identify a <span color='yellow'>repeat of the sequence.</span>"
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)


        text = [
            f"Before going to the procedure, ",
            f"let's look at the two <span color='cyan'>initial steps.</span>",
            f"First is finding the <span color='yellow'>last digit of the answer.</span>",
            f"Second is finding the <span color='yellow'>multiplier</span> to write the <span color='yellow'>previous digits.</span>",
            ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"To write the <span color='cyan'>decimal form of 1/9:</span>",
            f"Number in numerator is <span color='yellow'>1.</span> So last digit of the answer is <span color='yellow'>1.</span>",
            f"Number in Denominator is <span color='yellow'>9.</span> There is no digit before <span color='yellow'>9.</span>",
            f"so, let's take it as <span color='yellow'>Zero.</span> By <span color='yellow'>एकाधिकेन पूर्वेण</span> we get <span color='yellow'>0+1=1.</span>",
            f"This <span color='yellow'>1</span> is the <span color='yellow'>multiplier</span> in the process."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"To write the <span color='cyan'>decimal form of 3/39:</span>",
            f"Number in numerator is <span color='yellow'>3.</span> So last digit of the answer is <span color='yellow'>3.</span>",
            f"Number in Denominator is <span color='yellow'>39.</span> Digit before 9 is <span color='yellow'>3.</span>",
            f"By <span color='yellow'>एकाधिकेन पूर्वेण</span> we get <span color='yellow'>3+1=4</span>",
            f"This <span color='yellow'>4</span> is the <span color='yellow'>multiplier</span> in the process."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"Now we have the <span color='yellow'>last digit</span> of the answer ",
            f"and the <span color='yellow'>multiplier</span> to find the <span color='yellow'>previous digits.</span>",
            f"Rest of the process is really easy.",
            f"<span color='yellow'>Multiply</span> the <span color='yellow'>last digit</span> with <span color='yellow'>multiplier.</span>",
            f"We write the <span color='yellow'>unit digit</span> of this product before the <span color='yellow'>last digit</span>",
            f"and <span color='yellow'>rest of the digits</span> are treated as <span color='yellow'>carry</span> for next step."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"Now, <span color='yellow'>second last digit</span> is <span color='yellow'>multiplied</span> with <span color='yellow'>multiplier</span>",
            f"and the <span color='yellow'>result</span> is added with any <span color='yellow'>carry</span> from <span color='yellow'>previous step.</span>",
            f"Again, we write the <span color='yellow'>unit digit</span> of this answer ",
            f"before the <span color='yellow'>second last digit</span>",
            f"and <span color='yellow'>rest of the digits</span> are treated as <span color='yellow'>carry</span> for next step."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"This process is continued until the <span color='yellow'>repeat</span> of ",
            "<span color='yellow'>any digit</span> in the series with <span color='yellow'>same carry</span> for next step.",
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"Some <span color='cyan'>Interesting facts!</span>",
            f"Every reciprocal <span color='yellow'>1/x</span> has a <span color='yellow'>*maximum*</span> of ",
            f"<span color='yellow'>x-1</span> repeating digits. When this is true,",
            f"all <span color='yellow'>multiples</span> with <span color='yellow'>different numerators</span> less than <span color='yellow'>x</span> are",
            f"<span color='cyan'>Cyclic Permutations!</span>"
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        title_fact = DisplayText(self,
                              Span("This property makes it easy to compute many fractions.", color="cyan"), scale=0.7, wait=1,
                              move=(-2.5, -1), fade=False)
        title_fact1 = DisplayText(self, Span("2/7 = 0.285714...", color="yellow"),
                                  scale=0.6, wait=4, move=(-1.5, -1), fade=False)
        title_fact2 = DisplayText(self, Span("3/7 = 0.428571...", color="yellow"),
                                  scale=0.6, wait=4, move=(-1.0, -1), fade=False)
        title_fact3 = DisplayText(self, Span("4/7 = 0.571428...", color="yellow"),
                              scale=0.6, wait=4, move=(-0.5, -1), fade=False)
        title_fact4 = DisplayText(self, Span("5/7 = 0.714285...", color="yellow"),
                                 scale=0.6, wait=4, move=(0, -1),fade=False)
        title_fact5 = DisplayText(self, Span("6/7 = 0.857142...", color="yellow"),
                                 scale=0.6, wait=4, move=(0.5, -1), fade=False)

        self.wait(3)
        self.play(FadeOut(title_fact, title_fact1, title_fact2, title_fact3,title_fact4 ,title_fact5 ))



        r = Reciprocal(self, 1, 19, 2)
        r.step_all()
        r = Reciprocal(self, 7, 49, 5)
        r.step_all()
        r = Reciprocal(self, 6, 39, 4)
        r.step_all()

        lastscene(self)


        #t = Text("Bye")
        #self.play(FadeIn(t))



