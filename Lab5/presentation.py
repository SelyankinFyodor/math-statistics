import matplotlib.pyplot as plt


def draw_table(title, cell_text):
    plt.title(title)
    plt.axis('off')
    plt.table(colLabels=["pearson", "spearman", "selective_quadrant"],
              rowLabels=["E(z)", "E(z^2)", "D(z)"],
              cellText=cell_text, loc="center")
    plt.show()


def draw_ellipse(title, ellipse, dots, subplot):
    subplot.set_title(title)
    subplot.plot(dots[0], dots[1], 'ro')
    subplot.add_patch(ellipse)
