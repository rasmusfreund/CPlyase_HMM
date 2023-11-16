from manim import *
import os
import pandas as pd
import numpy as np


class TitlePage(Scene):
    def construct(self):
        # Title and subtitle
        title = Text("Carbon-Phosporus Lyase", font_size=48).to_edge(UP)
        sub_title = Text("gene sequence detection with HMMs", font_size=48).next_to(title, DOWN)
        author = Text("By: Rasmus Freund", font_size=36).next_to(sub_title, DOWN)
        supervisors = Text("Supervised by: Christian Storm Pedersen and Ditlev E. Brodersen", font_size=30).next_to(author, DOWN)

        # States of HMM
        start_state = Circle(color=WHITE).scale(0.5)
        hidden_state1 = Circle(color=WHITE).scale(0.5).next_to(start_state, RIGHT, buff=2)
        hidden_state2 = Circle(color=WHITE).scale(0.5).next_to(hidden_state1, RIGHT, buff=2)
        observable_state1 = Square(color=WHITE).scale(0.5).next_to(hidden_state1, DOWN, buff=1)
        observable_state2 = Square(color=WHITE).scale(0.5).next_to(hidden_state2, DOWN, buff=1)

        hmm_group = VGroup()
        hmm_group.add(start_state, hidden_state1, hidden_state2, observable_state1, observable_state2)

        # Labels for the states
        start_label = Text("Start", color=WHITE, font_size=24).move_to(start_state.get_center())
        hidden_label1 = Text("H1", color=WHITE, font_size=24).move_to(hidden_state1.get_center())
        hidden_label2 = Text("H2", color=WHITE, font_size=24).move_to(hidden_state2.get_center())
        observable_label1 = Text("O1", color=WHITE, font_size=24).move_to(observable_state1.get_center())
        observable_label2 = Text("O2", color=WHITE, font_size=24).move_to(observable_state2.get_center())

        labels_group = VGroup()
        labels_group.add(start_label, hidden_label1, hidden_label2, observable_label1, observable_label2)

        # Transition arrows
        transition_start_h1 = Arrow(start_state.get_right(), hidden_state1.get_left(), buff=0.1, color=BLUE)
        transition_h1_h2 = Arrow(hidden_state1.get_right(), hidden_state2.get_left(), buff=0.1, color=BLUE)
        transition_h1_o1 = Arrow(hidden_state1.get_bottom(), observable_state1.get_top(), buff=0.1, color=BLUE)
        transition_h2_o2 = Arrow(hidden_state2.get_bottom(), observable_state2.get_top(), buff=0.1, color=BLUE)

        arrows_group = VGroup()
        arrows_group.add(transition_start_h1, transition_h1_h2, transition_h1_o1, transition_h2_o2)

        # Move stuff
        hmm_group.next_to(supervisors, DOWN, buff=1.3)
        labels_group.move_to(hmm_group.get_center())
        arrows_group.move_to(hmm_group.get_center())

        labels_group.shift(LEFT*.1)
        arrows_group.shift(UP*.4)
        arrows_group.shift(RIGHT*.35)

        # Add elements to the scene
        self.add(title, sub_title, author, supervisors)
        self.add(hmm_group, labels_group, arrows_group)

        # Hold on screen
        self.wait(2)


class ProblemSolutionPage(Scene):
    def construct(self):
        problem_large = Text("Problem:", font_size=34)
        problem_text = Text(
            "Despite knowledge of protein structures in the C-P lyase pathway,\n"
            "the mechanisms of initial reactions remain elusive, lacking structures\n"
            "of enzyme complexes and substrate-bound states.",
            font_size=28
        )
        problem_large.to_edge(UP)
        problem_large.to_edge(LEFT)
        problem_text.to_edge(UP)
        problem_text.shift(DOWN*.9)
        problem_text.shift(RIGHT*.1)

        solution_large = Text("(Partial) solution:", font_size=34)
        solution_text = Text(
            "Employing Hidden Markov Models (HMMs) to detect these genes in\n"
            "bacterial genomes may provide the missing structural and\n"
            "functional insights.",
            font_size=28
        )

        solution_large.to_edge(LEFT)
        solution_text.next_to(problem_text, DOWN, buff=2.2)

        self.add(problem_large)
        self.wait(2)
        self.play(FadeIn(problem_text))
        self.wait(12)
        self.play(FadeIn(solution_large))
        self.wait(2)
        self.play(FadeIn(solution_text))
        self.wait(2)


class GeneModularityScene(Scene):
    def construct(self):
        # Create representations for gene modules
        genes = VGroup(
            *[
                Rectangle(height=0.3, width=0.9, color=BLUE).set_fill(BLUE, opacity=0.5)
                for _ in range(14)  # Assuming 14 gene modules for illustration
            ]
        ).arrange_in_grid(cols=14, buff=0.1)  # Arrange gene modules in a row

        gene_labels = "CDEFGHIJKLMNOP"  # Label for each gene module
        for i, gene in enumerate(genes):
            gene.add(Text(gene_labels[i], color=WHITE).scale(0.5).move_to(gene))

        # Paths for genes C and D to follow
        arc_c = ArcBetweenPoints(genes[0].get_center(), genes[1].get_center(), angle=-TAU / 4)
        arc_d = ArcBetweenPoints(genes[1].get_center(), genes[0].get_center(), angle=TAU / 4)

        self.add(genes)  # Add the gene modules to the scene

        # Animate the genes to show modularity
        self.play(Circumscribe(genes[-2]))
        self.wait(1)
        self.play(FadeOut(genes[-2], shift=DOWN))  # fade gene O to show absence
        self.wait(2)
        # Animate the genes swapping positions
        self.play(
            MoveAlongPath(genes[0], arc_c),
            MoveAlongPath(genes[1], arc_d),
            run_time=2
        )
        self.wait(2)

        # Demonstrate gene duplication by copying a gene module
        duplicated_gene = genes[5].copy()
        self.play(
            FadeIn(duplicated_gene, scale=1.5),
            duplicated_gene.animate.next_to(duplicated_gene, DOWN, buff=0.3))
        self.play(duplicated_gene.animate.next_to(genes[-2], DOWN, buff=0.3))
        self.play(duplicated_gene.animate.move_to(genes[-2].get_center()))

        self.wait(2)


class DataPipelineScene(Scene):
    def construct(self):
        cwd = os.getcwd()
        media = os.path.join(cwd, 'media')
        images = os.path.join(media, 'images')
        image_path = os.path.join(images, 'project_presentation')

        # Icons/Symbols for each step
        ncbi_icon = ImageMobject(os.path.join(image_path, 'NCBI_logo.png')).scale(0.255)
        python_icon = ImageMobject(os.path.join(image_path, 'Python_logo.png')).scale(0.255)
        hmmer_icon = ImageMobject(os.path.join(image_path, 'HMMER_logo.png')).scale(0.255)
        plot_graph = ImageMobject(os.path.join(image_path, 'plot_logo.png')).scale(0.255)

        # Text for each icon
        ncbi_text = Text('Download', font_size=28)
        python_text = Text('Wrangle', font_size=28)
        hmmer_text = Text('Analyze', font_size=28)
        plot_text = Text('Visualize', font_size=28)

        # Position the icons
        total_width = ncbi_icon.get_width() + python_icon.get_width() + hmmer_icon.get_width() + plot_graph.get_width() + 3  # assuming 1 unit buff between each
        start_x = total_width / 2.5  # Starting x position for the first icon

        ncbi_icon.move_to(LEFT * start_x)
        python_icon.next_to(ncbi_icon, RIGHT, buff=1)
        hmmer_icon.next_to(python_icon, RIGHT, buff=1)
        plot_graph.next_to(hmmer_icon, RIGHT, buff=1)

        ncbi_text.next_to(ncbi_icon, DOWN, buff=0.5)
        python_text.next_to(python_icon, DOWN, buff=0.5)
        hmmer_text.next_to(hmmer_icon, DOWN, buff=0.5)
        plot_text.next_to(plot_graph, DOWN, buff=0.5)

        # Animate the NCBI download
        ncbi_duplicate = ncbi_icon.copy()
        self.play(FadeIn(ncbi_icon), FadeIn(ncbi_text))
        self.wait(1)
        self.add(ncbi_duplicate)
        self.bring_to_back(ncbi_duplicate)

        # Animate the data wrangling with Python
        self.play(Transform(ncbi_icon, python_icon), FadeIn(python_text))
        self.wait(1)

        # Animate the HMMER processing
        self.play(Transform(python_icon, hmmer_icon), FadeIn(hmmer_text))
        self.wait(1)

        # Show the resulting plot
        self.play(Transform(hmmer_icon, plot_graph), FadeIn(plot_text))
        self.wait(2)


class HMMERPlotScene(Scene):
    def construct(self):
        # Read data from CSV
        cwd = os.getcwd()
        data_path = os.path.join(cwd, 'data')
        validation_path = os.path.join(data_path, 'validation')
        csv_path = os.path.join(validation_path, 'hmmer_plot_data.csv')

        hmmer_data = pd.read_csv(csv_path)

        unique_queries = hmmer_data['query'].unique()
        query_to_x = {query: i for i, query in enumerate(unique_queries)}
        hmmer_data['x_pos'] = hmmer_data['query'].map(query_to_x)

        # Create axes
        axes = Axes(
            x_range=[0, len(unique_queries), 5],
            y_range=[0, 180, 25],
            axis_config={'color': BLUE},
            x_length=9,
            y_length=5.5,
            tips=False
        )

        # Custom colors
        STEEL_BLUE = np.array([70/255, 130/255, 180/255])
        SEAGREEN = np.array([46/255, 139/255, 87/255])

        # Create dots for each data point
        dots = VGroup()
        for _, row in hmmer_data.iterrows():
            x = row['x_pos'] + 2
            y = row['neg_log_e_value']
            color = SEAGREEN if not row['is_negative'] else STEEL_BLUE
            dot = Dot(axes.c2p(x,y), color=color)
            dots.add(dot)

        separation_y = 43.270303756120384

        separation_line = DashedLine(
            start=axes.c2p(0, separation_y),
            end=axes.c2p(len(unique_queries), separation_y),
            color=RED,
            dash_length=0.3,
            dashed_ratio=0.5,
        )

        # Axis labels
        x_axis_label = Text("Sequences", font_size=24).next_to(axes.x_axis, DOWN)
        y_axis_label = Text("-log(E-value)", font_size=24).next_to(axes.y_axis, LEFT, buff=-0.6).rotate(PI/2)

        true_pos_dot = Dot(color=SEAGREEN)
        true_neg_dot = Dot(color=STEEL_BLUE)

        true_pos_label = Text("True Positives", font_size=24)
        true_neg_label = Text("True Negatives", font_size=24)

        true_legend = VGroup()
        true_legend.add(true_pos_dot, true_pos_label)
        neg_legend = VGroup()
        neg_legend.add(true_neg_dot, true_neg_label)

        true_legend.arrange(RIGHT, aligned_edge=LEFT)
        neg_legend.arrange(RIGHT, aligned_edge=LEFT)

        legend = VGroup()
        legend.add(true_legend, neg_legend)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        legend.to_edge(RIGHT)

        plot = VGroup()
        plot.add(axes, dots, separation_line, x_axis_label, y_axis_label)
        plot.to_edge(LEFT)


        self.play(Create(axes), run_time=2)
        self.play(FadeIn(dots), run_time=3)
        self.play(Write(x_axis_label), Write(y_axis_label), run_time=1)
        self.play(FadeIn(legend))
        self.play(Create(separation_line))
        self.wait(2)
