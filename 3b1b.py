# divergence, kolecko uprostred, slow in, fast out

class DivergenceAtSlowFastPoint(Scene):
    CONFIG = {
        "vector_field_config": {
            "length_func": lambda norm: 0.1 + 0.4 * norm / 4.0,
            "min_magnitude": 0,
            "max_magnitude": 3,
        },
        "stream_lines_config": {
            "start_points_generator_config": {
                "delta_x": 0.125,
                "delta_y": 0.125,
            },
            "virtual_time": 1,
            "min_magnitude": 0,
            "max_magnitude": 3,
        },
    }

    def construct(self):
        def func(point):
            return 3 * sigmoid(point[0]) * RIGHT
        vector_field = self.vector_field = VectorField(
            func, **self.vector_field_config
        )

        circle = Circle(color=WHITE)
        slow_words = TexText("Slow flow in")
        fast_words = TexText("Fast flow out")
        words = VGroup(slow_words, fast_words)
        for word, vect in zip(words, [LEFT, RIGHT]):
            word.add_background_rectangle()
            word.next_to(circle, vect)

        div_tex = Tex(
            "\\text{div}\\,\\textbf{F}(x, y) > 0"
        )
        div_tex.add_background_rectangle()
        div_tex.next_to(circle, UP)

        self.add(vector_field)
        self.add_foreground_mobjects(circle, div_tex)
        self.begin_flow()
        self.wait(2)
        for word in words:
            self.add_foreground_mobjects(word)
            self.play(Write(word))
        self.wait(8)

    def begin_flow(self):
        stream_lines = StreamLines(
            self.vector_field.func,
            **self.stream_lines_config
        )
        stream_line_animation = AnimatedStreamLines(stream_lines)
        stream_line_animation.update(3)
        self.add(stream_line_animation)



        
        
#         kolecko okolo bodu a DivergenceAtSlowFastPoint



class DivergenceAsNewFunction(Scene):
    def construct(self):
        self.add_plane()
        self.show_vector_field_function()
        self.show_divergence_function()

    def add_plane(self):
        plane = self.plane = NumberPlane()
        plane.add_coordinates()
        self.add(plane)

    def show_vector_field_function(self):
        func = self.func
        unscaled_vector_field = VectorField(
            func,
            length_func=lambda norm: norm,
            colors=[BLUE_C, YELLOW, RED],
            delta_x=np.inf,
            delta_y=np.inf,
        )

        in_dot = Dot(color=PINK)
        in_dot.move_to(3.75 * LEFT + 1.25 * UP)

        def get_input():
            return in_dot.get_center()

        def get_out_vect():
            return unscaled_vector_field.get_vector(get_input())

        # Tex
        func_tex = Tex(
            "\\textbf{F}(", "+0.00", ",", "+0.00", ")", "=",
        )
        dummy_in_x, dummy_in_y = func_tex.get_parts_by_tex("+0.00")
        func_tex.add_background_rectangle()
        rhs = DecimalMatrix(
            [[0], [0]],
            element_to_mobject_config={
                "num_decimal_places": 2,
                "include_sign": True,
            },
            include_background_rectangle=True
        )
        rhs.next_to(func_tex, RIGHT)
        dummy_out_x, dummy_out_y = rhs.get_mob_matrix().flatten()

        VGroup(func_tex, rhs).to_corner(UL, buff=MED_SMALL_BUFF)

        VGroup(
            dummy_in_x, dummy_in_y,
            dummy_out_x, dummy_out_y,
        ).set_fill(BLACK, opacity=0)

        # Changing decimals
        in_x, in_y, out_x, out_y = [
            DecimalNumber(0, include_sign=True)
            for x in range(4)
        ]
        VGroup(in_x, in_y).set_color(in_dot.get_color())
        VGroup(out_x, out_y).set_color(get_out_vect().get_fill_color())
        in_x_update = ContinualChangingDecimal(
            in_x, lambda a: get_input()[0],
            position_update_func=lambda m: m.move_to(dummy_in_x)
        )
        in_y_update = ContinualChangingDecimal(
            in_y, lambda a: get_input()[1],
            position_update_func=lambda m: m.move_to(dummy_in_y)
        )
        out_x_update = ContinualChangingDecimal(
            out_x, lambda a: func(get_input())[0],
            position_update_func=lambda m: m.move_to(dummy_out_x)
        )
        out_y_update = ContinualChangingDecimal(
            out_y, lambda a: func(get_input())[1],
            position_update_func=lambda m: m.move_to(dummy_out_y)
        )

        self.add(func_tex, rhs)
        # self.add(Mobject.add_updater(
        #     rhs, lambda m: m.next_to(func_tex, RIGHT)
        # ))

        # Where those decimals actually change
        self.add(in_x_update, in_y_update)

        in_dot.save_state()
        in_dot.move_to(ORIGIN)
        self.play(in_dot.restore)
        self.wait()
        self.play(*[
            ReplacementTransform(
                VGroup(mob.copy().fade(1)),
                VGroup(out_x, out_y),
            )
            for mob in (in_x, in_y)
        ])
        out_vect = get_out_vect()
        VGroup(out_x, out_y).match_style(out_vect)
        out_vect.save_state()
        out_vect.move_to(rhs)
        out_vect.set_fill(opacity=0)
        self.play(out_vect.restore)
        self.out_vect_update = Mobject.add_updater(
            out_vect,
            lambda ov: Transform(ov, get_out_vect()).update(1)
        )

        self.add(self.out_vect_update)
        self.add(out_x_update, out_y_update)

        self.add(Mobject.add_updater(
            VGroup(out_x, out_y),
            lambda m: m.match_style(out_vect)
        ))
        self.wait()

        for vect in DOWN, 2 * RIGHT, UP:
            self.play(
                in_dot.shift, 3 * vect,
                run_time=3
            )
            self.wait()

        self.in_dot = in_dot
        self.out_vect = out_vect
        self.func_equation = VGroup(func_tex, rhs)
        self.out_x, self.out_y = out_x, out_y
        self.in_x, self.in_y = out_x, out_y
        self.in_x_update = in_x_update
        self.in_y_update = in_y_update
        self.out_x_update = out_x_update
        self.out_y_update = out_y_update

    def show_divergence_function(self):
        vector_field = VectorField(self.func)
        vector_field.remove(*[
            v for v in vector_field
            if v.get_start()[0] < 0 and v.get_start()[1] > 2
        ])
        vector_field.set_fill(opacity=0.5)
        in_dot = self.in_dot

        def get_neighboring_points(step_sizes=[0.3], n_angles=12):
            point = in_dot.get_center()
            return list(it.chain(*[
                [
                    point + step_size * step
                    for step in compass_directions(n_angles)
                ]
                for step_size in step_sizes
            ]))

        def get_vector_ring():
            return VGroup(*[
                vector_field.get_vector(point)
                for point in get_neighboring_points()
            ])

        def get_stream_lines():
            return StreamLines(
                self.func,
                start_points_generator=get_neighboring_points,
                start_points_generator_config={
                    "step_sizes": np.arange(0.1, 0.5, 0.1)
                },
                virtual_time=1,
                stroke_width=3,
            )

        def show_flow():
            stream_lines = get_stream_lines()
            random.shuffle(stream_lines.submobjects)
            self.play(LaggedStartMap(
                ShowCreationThenDestruction,
                stream_lines,
                remover=True
            ))

        vector_ring = get_vector_ring()
        vector_ring_update = Mobject.add_updater(
            vector_ring,
            lambda vr: Transform(vr, get_vector_ring()).update(1)
        )

        func_tex, rhs = self.func_equation
        out_x, out_y = self.out_x, self.out_y
        out_x_update = self.out_x_update
        out_y_update = self.out_y_update
        div_tex = Tex("\\text{div}")
        div_tex.add_background_rectangle()
        div_tex.move_to(func_tex, LEFT)
        div_tex.shift(2 * SMALL_BUFF * RIGHT)

        self.remove(out_x_update, out_y_update)
        self.remove(self.out_vect_update)
        self.add(self.in_x_update, self.in_y_update)
        self.play(
            func_tex.next_to, div_tex, RIGHT, SMALL_BUFF,
            {"submobject_to_align": func_tex[1][0]},
            Write(div_tex),
            FadeOut(self.out_vect),
            FadeOut(out_x),
            FadeOut(out_y),
            FadeOut(rhs),
        )
        # This line is a dumb hack around a Scene bug
        self.add(*[
            Mobject.add_updater(
                mob, lambda m: m.set_fill(None, 0)
            )
            for mob in (out_x, out_y)
        ])
        self.add_foreground_mobjects(div_tex)
        self.play(
            LaggedStartMap(GrowArrow, vector_field),
            LaggedStartMap(GrowArrow, vector_ring),
        )
        self.add(vector_ring_update)
        self.wait()

        div_func = divergence(self.func)
        div_rhs = DecimalNumber(
            0, include_sign=True,
            include_background_rectangle=True
        )
        div_rhs_update = ContinualChangingDecimal(
            div_rhs, lambda a: div_func(in_dot.get_center()),
            position_update_func=lambda d: d.next_to(func_tex, RIGHT, SMALL_BUFF)
        )

        self.play(FadeIn(div_rhs))
        self.add(div_rhs_update)
        show_flow()

        for vect in 2 * RIGHT, 3 * DOWN, 2 * LEFT, 2 * LEFT:
            self.play(in_dot.shift, vect, run_time=3)
            show_flow()
        self.wait()

    def func(self, point):
        x, y = point[:2]
        return np.sin(x + y) * RIGHT + np.sin(y * x / 3) * 



class ShearCurl(IntroduceCurl):
    def construct(self):
        self.show_vector_field()
        self.begin_flow()
        self.wait(2)
        self.comment_on_relevant_region()

    def show_vector_field(self):
        vector_field = self.vector_field = VectorField(
            self.func, **self.vector_field_config
        )
        vector_field.submobjects.key=sort(
            key=lambda a: a.get_length()
        )
        self.play(LaggedStartMap(GrowArrow, vector_field))

    def comment_on_relevant_region(self):
        circle = Circle(color=WHITE, radius=0.75)
        circle.next_to(ORIGIN, UP, LARGE_BUFF)
        self.play(ShowCreation(circle))

        slow_words, fast_words = words = [
            TexText("Slow flow below"),
            TexText("Fast flow above")
        ]
        for word, vect in zip(words, [DOWN, UP]):
            word.add_background_rectangle(buff=SMALL_BUFF)
            word.next_to(circle, vect)
            self.add_foreground_mobjects(word)
            self.play(Write(word))
            self.wait()

        twig = Rectangle(
            height=0.8 * 2 * circle.radius,
            width=SMALL_BUFF,
            stroke_width=0,
            fill_color=GREY_BROWN,
            fill_opacity=1,
        )
        twig.add(Dot(twig.get_center()))
        twig.move_to(circle)
        always_rotate(
            twig, rate=-90 * DEGREES,
        )

        self.play(FadeIn(twig, UP))
        self.add(twig_rotation)
        self.wait(16)

    # Helpers
    def func(self, point):
        return 0.5 * point[1] * RIGHT        