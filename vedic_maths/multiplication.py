from manim import *
from numpy import array
from common import *


def EkadhikenaSquare(scene, num, wait=5, fade=True):
    snum = str(num)
    inum = int(num)
    sprev = snum[:-1]
    prev = int(sprev)
    assert snum[-1] == "5", "Only works with numbers ending in 5"
    text= [
        f"Find the Square of <span color='yellow'>{snum}</span>",
        f"Digit(s) before 5 are <span color='yellow'>{sprev}</span>",
        f"One more than that is  <span color='yellow'>{prev+1}</span>",
        f"Our answer is simply <span color='yellow'>{prev} times {prev+1}, suffixed with 25</span>",
        f"Which is <span color='yellow'>{prev*(prev+1)}{25}</span>"]
    Explanation(scene, text, font='Cambria Math', aligned_edge=LEFT)
    scene.next_section()
    ans = inum**2
    assert ans == prev*(prev+1)*100+25
    snum2 = snum
    f1 = f2 = 5
    return EkCom(scene, snum, snum2, prev, f1, f2, ans, wait, fade)

def EkCom(scene, snum, snum2, prev, f1, f2, ans, wait=5, fade=True):
    g   = ShowOp(scene, snum, snum2, "×", "?", wait=1, fade=False)
    g11   = ShowOp(scene, prev, "<span color='red'>"+str(prev+1)+"</span>", "×", prev*(prev+1), play=False)
    g12   = ShowOp(scene, f1, f2, "×", f1*f2, play=False)
    g12.move_to(RIGHT*2)
    scene.play(Transform(g, g11))
    scene.add(g12)
    scene.wait(2)
    scene.play(FadeOut(g[1]))
    scene.play(g12.animate.next_to(g[0], RIGHT, aligned_edge=UP))
    scene.wait(2)
    g2  = ShowOp(scene, snum, snum2, "×", ans, play=False)
    scene.remove(g12)
    scene.play(Transform(g, g2))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(g))
    return g

def EkadhikenaMult(scene, num, num2, wait=5, fade=True):
    snum = str(num)
    inum = int(num)
    sprev = snum[:-1]
    fin = int(snum[-1])
    prev = int(sprev)
    snum2 = str(num2)
    sprev2 = snum2[:-1]
    inum2 = int(num2)
    fin2 = int(snum2[-1])

    assert (int(snum[-1]) + int(snum2[-1])) == 10, "Only works with numbers with last digits ending in 10"
    assert sprev == sprev2, "Only works with numbers with previous digits the same"

    ans = inum*inum2
    assert ans == prev*(prev+1)*100+fin*fin2

    text= [
        f"Find the product of <span color='yellow'>{snum} and {snum2}</span>",
        f"Final digits are <span color='yellow'>{snum[-1]} and {snum2[-1]}</span>",
        f"Their product is <span color='yellow'>{int(snum[-1])*int(snum2[-1])}</span>",
        f"Pre-final Digit(s) are <span color='yellow'>{sprev}</span>",
        f"One more than that is  <span color='yellow'>{prev+1}</span>",
        f"As before, our answer begins with <span color='yellow'>{prev} times {prev+1}</span>",
        f"It is now suffixed with <span color='yellow'>{int(snum[-1])*int(snum2[-1])}</span>",
        f"Which leads us to <span color='yellow'>{inum*inum2}</span>"]
    Explanation(scene, text, font='Cambria Math', aligned_edge=LEFT)
    scene.next_section()
    return EkCom(scene, snum, snum2, prev, fin, fin2, ans, wait, fade)



class Ekadhikena(Scene):
    ''' Ekadhikena Purvena '''
    def construct(self):
        # Title
        Title(self, "एकाधिकेन पूर्वेण", "Squares and Multiplication with Ekadhikena",
              move=(3, 5), wait=1)
        self.next_section()

        # Introduction
        text = ["Simple multiplication and squares",
                "Before we introduce a general method for multiplication",
                "We will look at special cases which are easier"]
        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        # Introduction
        text = ["Our first method works for ",
                "1. Squares of numbers ending in 5",
                "2. Products of numbers with last digits adding to 10",
                "and other digits identical"]
        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()


        # Sutra Scene
        t0 = "एकाधिकेन पूर्वेण"
        t1 = ["एकाधिकेन", "पूर्वेणः"]
        t2 = ["<span size='smaller'>By one more than</span>", "<span size='smaller'>the previous</span>"]
        Sutra(self, t0, t1, t2, wait=3, scale=0.5, move=None, fade=True, font='Cambria Math')
        self.next_section()

        EkadhikenaSquare(self, 35)
        self.next_section()

        EkadhikenaSquare(self, 85)
        self.next_section()

        # Sutra Scene
        t0 = "अन्त्ययोर्दशकेऽपि"
        t1 = ["अन्त्ययोः", "दशके अपि"]
        t2 = ["<span size='smaller'>When the last</span>", "<span size='smaller'>sum to 10</span>"]
        Sutra(self, t0, t1, t2, wait=3, scale=0.5, move=None, fade=True, font='Cambria Math')
        self.next_section()

        # Introduction
        text = ["We can use this to multiply numbers that",
                "1. have identical digits barring the final one",
                "2. have thier final digits adding up to 10"]
        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        EkadhikenaMult(self, 33, 37)
        self.next_section()
        
        EkadhikenaMult(self, 72, 78)
        self.next_section()
