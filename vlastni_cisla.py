from manim import *

class Pokus(Scene):
    def construct(self):
        title = Title(r"Odvození rovnice pro transformaci tenzorů").to_edge(UP)
        self.add(title)
        # Formalni odvozeni transformacni rovnice pro tenzory
        lines = MathTex(
            r"{{V}} &= {{A}} {{U}}\\",
            r"{{RV'}} &= {{A}} {{R U'}}\\",
            r"{{V'}} &= {{ R^{-1} }} {{A}} {{R U'}}\\",
            r"{{V'}} &= (R^{-1} A R) {{U'}}"
        )
        print(len(lines))
        groups = [
            lines[:5],
            lines[5:11],
            lines[11:19],
            lines[19:]
            ]

        self.play(FadeIn(groups[0]))
        for i in [0,1,2]:
            self.play(
            TransformMatchingShapes(
                groups[i].copy(), 
                groups[i+1], 
                path_arc=90 * DEGREES)
            ),
            self.wait(.5)           

        self.wait()