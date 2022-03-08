from manim import *
from numpy import array, array_equal

# Helper Function for Title
def Title(scene, t0, t1, wait=5, scale=0.3, move=(3, 6)):
    # Title Scene
    t0 = Text(t0)
    t1 = Text(t1)
    tg = VGroup(t0, t1).arrange(direction=DOWN)
    scene.add(tg)
    scene.wait(wait)
    scene.play(tg.animate.scale(scale).move_to(move[0] * DOWN + move[1] * RIGHT))
    return tg


# Helper function for multi-line explanation
def Explanation(scene, text, font='', wait=3, fade=True, aligned_edge=ORIGIN):
    # Explanation

    el = [MarkupText(x, font=font) for x in text]
    eg = VGroup(*el).scale(0.7).arrange(DOWN, aligned_edge=aligned_edge)

    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
    if wait:
        scene.wait(wait)
    if fade:
        scene.play(FadeOut(eg))

    return eg


# Helper function to display text message
def DisplayText(scene, text, font='', scale=1, move=(0, 0), wait=5, fade=True):
    t = MarkupText(text, font=font).scale(scale)
    scene.play(FadeIn(t.move_to(move[0] * DOWN + move[1] * RIGHT)))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(t))
    return t


# Helper function for Sutra display
# Inputs
#     sutra     - Sutra string
#     viccheda  - List of sandhi split segments
#   translation - List of translation segments, matching viccheda
def Sutra(scene, sutra, viccheda, translation, font='', wait=3, scale=0.5, move=(3, 5), fade=False, dir1=RIGHT, dir2=RIGHT):
    sg = VGroup(Text("सूत्रम्"), Text("विच्छेदः"),
                Text("Translation")).arrange(direction=DOWN,
                                                                                aligned_edge=RIGHT).set_color(
        BLUE).set_opacity(0.5)
    t0 = MarkupText(sutra)
    t1 = [MarkupText(x) for x in viccheda]
    t2 = [MarkupText(x, font=font) for x in translation]
    assert len(viccheda) == len(translation), "Sandhi split (viccheda) and translation must be of equal length"
    a1 =  UP if array_equal(dir1, RIGHT) else LEFT
    a2 =  UP if array_equal(dir2, RIGHT) else LEFT
    t1g = VGroup(*t1).arrange(direction=dir1, aligned_edge=a1).set_opacity(0)
    t2g = VGroup(*t2).arrange(direction=dir2, aligned_edge=a2).set_opacity(0)
    tg = VGroup(t0, t1g, t2g).arrange(direction=DOWN, aligned_edge=LEFT)

    tg.move_to(UP + RIGHT)
    sg[0].next_to(t0, LEFT)
    sg[1].next_to(t1g, LEFT)
    sg[2].next_to(t2g, LEFT)

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
    scene.play(FadeOut(sg, t0))
    if move is not None:
        scene.play(t1g.set_color(WHITE).animate.scale(0.5).move_to(move[0] * UP + move[1] * RIGHT))
        scene.play(t2g.set_color(WHITE).animate.scale(0.5).move_to((move[0] - 0.5) * UP + move[1] * RIGHT))
        scene.wait(1)
    elif fade:
        scene.play(FadeOut(t1g, t2g))
    return (t1g, t2g)


def ShowOp(scene, sn1, sn2, sop, sr, move=(0, 0), wait=3, play=True, fade=True, oplen=0):
    ''' Helper function to display a single operation '''
    n1 = MarkupText(str(sn1))
    n2 = MarkupText(str(sn2))
    if oplen == 0:
        oplen = len(str(sn1))
    ln = Line(start=array([-1 * oplen / 2, 0, 0]), end=array([0, 0, 0])).set_color(YELLOW)
    op = MarkupText(str(sop))
    res = MarkupText(str(sr))
    g1 = VGroup(n1, n2, ln, res).arrange(DOWN, aligned_edge=RIGHT)
    g = VGroup(g1, op).arrange(RIGHT, aligned_edge=UP)
    if play:
        scene.play(Write(g.move_to(UP * move[0] + RIGHT * move[1])))
        if wait:
            scene.wait(wait)
        if fade:
            scene.play(FadeOut(g))
    return g

def Span(t, **kwargs):
    ''' Helper function for generating text with span tag '''
    return "<span " + ",".join([f"{k}='{v}'" for k,v in kwargs.items()]) + f">{t}</span>"
    
