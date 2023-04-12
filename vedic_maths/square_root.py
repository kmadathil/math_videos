from manim import *
from numpy import array
from common import *
import math

# No need for vinculum digits in sq roots
def MT(snum, color="Yellow"):
    ''' Wrapper - MathTex((snum)) '''
    el = [s for s in snum]
    eg = MathTex(*el, color=color)
    return eg

def DOpVal(n):
    'D Operator on integer n'
    # blast into digits
    nl = [int(s) for s in str(n)]
    d = 0
    # Multiply each digit with
    # counterpart in reversed number
    # Sum to get result
    for z in zip(nl, reversed(nl)):
        d += z[0]*z[1]
    return d

def DOp(scene, num,  wait=0):
    ''' Display a D Operator '''
    n1 = MT(str(num))    # Initial number
    sr = DOpVal(num)     # D Operator result
    # Arrange number and lines
    g1, lines = DOp_(n1, sr)   
    # Add to scene
    scene.add(g1)
    scene.add(*lines)
    if wait:
        scene.wait(wait)
    return g1, lines


def DOp_(n1, sr):
    ''' D Operator Internal (num)
       
        Copies num MathTex object, places the copy below original object
        Copy is colored gray
        Generates lines connecting first digit to the last digit of the copy etc
        Returns the copy object and the lines
    '''
    # Copy original number in grey
    n2 = n1.copy()   
    n2.set_color(GREY)
    oplen = len(n2)
    # Dividing line
    ln = Line(start=array([-1 * oplen / 2, 0, 0]), end=array([0, 0, 0])).set_color(GRAY)
    # Result
    res = MT(str(sr), color=GRAY)
    # Arrange in group
    g1 = VGroup(n1, n2, ln, res).arrange(DOWN, aligned_edge=RIGHT)
    # Generate connecting lines _after_ the group has been
    # arranged
    lines = doplines(scene, n1, n2)
    return g1, lines

# Display D Operator lines pattern.
# This is a stripped down version of utlines from multiply
def doplines(scene, n1, n2, color=GRAY):
    n = len(n1) # Length of inputs
    lines =  [Line(n2[i].get_top(), [n2[-1].get_top()[0], n1[-1].get_bottom()[1], n1[-1].get_bottom()[2]]).set_color(color) for i in range(n)]
    
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

    # Display all the lines
    show = list(range(n))
    _display(show)
    return lines

class DOpTest(Scene):
    def construct(self):
        num = 345
        g1, lines = DOp(self, 345, wait=5)
        self.remove(g1[1], g1[2], g1[3])
        self.remove(*lines)
        self.wait(1)
        self.next_section() 
