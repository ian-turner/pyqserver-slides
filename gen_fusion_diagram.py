"""Generate a gate fusion diagram for the slides.

Shows three qubits, each with two consecutive single-qubit gates, being
fused into a single multi-qubit unitary U, illustrating the gate fusion
optimization enabled by instruction queuing.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Vertical positions for the three qubit wires
WIRE_YS = [2.0, 1.0, 0.0]
WIRE_LABELS = [r'$|q_0\rangle$', r'$|q_1\rangle$', r'$|q_2\rangle$']
# Gates on each wire (before fusion)
GATE_COLS = [[('H', 1.1), ('S', 2.1)],
             [('T', 1.1), ('H', 2.1)],
             [('S', 1.1), ('T', 2.1)]]

GW = 0.46   # gate box width
GH = 0.46   # gate box height


def draw_gate(ax, x, y, label, width=GW, height=GH, fontsize=13,
              facecolor='white', edgecolor='black'):
    rect = mpatches.FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.04",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=1.4,
        zorder=3,
    )
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=fontsize, fontfamily='serif', zorder=4)


def draw_wire(ax, x0, x1, y, lw=1.5):
    ax.plot([x0, x1], [y, y], color='black', linewidth=lw, zorder=1)


def setup_ax(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')


def make_before(ax):
    setup_ax(ax, (0, 3.5), (-0.55, 2.55))

    for wire_y, label, gates in zip(WIRE_YS, WIRE_LABELS, GATE_COLS):
        # input label
        ax.text(0.05, wire_y, label, ha='center', va='center',
                fontsize=11, fontfamily='serif')
        # wire segments
        xs = [g[1] for g in gates]
        seg_starts = [0.35] + [x + GW/2 for x in xs[:-1]]
        seg_ends   = [xs[0] - GW/2] + [xs[1] - GW/2]
        seg_ends.append(3.2)
        seg_starts.append(xs[-1] + GW/2)
        for x0, x1 in zip(seg_starts, seg_ends):
            draw_wire(ax, x0, x1, wire_y)
        # gates
        for lbl, gx in gates:
            draw_gate(ax, gx, wire_y, lbl)
        # output label
        ax.text(3.45, wire_y, label, ha='center', va='center',
                fontsize=11, fontfamily='serif')

    ax.set_title('Before fusion', fontsize=11, pad=4)


def make_after(ax):
    setup_ax(ax, (0, 3.5), (-0.55, 2.55))

    # big fused unitary box spanning all wires
    top_y    = WIRE_YS[0]
    bot_y    = WIRE_YS[-1]
    box_x    = 1.75
    box_w    = 1.1
    box_h    = (top_y - bot_y) + GH + 0.1
    box_cy   = (top_y + bot_y) / 2

    fused = mpatches.FancyBboxPatch(
        (box_x - box_w/2, box_cy - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.06",
        facecolor='#dce8f5', edgecolor='black', linewidth=1.6,
        zorder=3,
    )
    ax.add_patch(fused)
    ax.text(box_x, box_cy, r'$U$', ha='center', va='center',
            fontsize=16, fontfamily='serif', zorder=4)

    for wire_y, label in zip(WIRE_YS, WIRE_LABELS):
        ax.text(0.05, wire_y, label, ha='center', va='center',
                fontsize=11, fontfamily='serif')
        draw_wire(ax, 0.35, box_x - box_w/2, wire_y)
        draw_wire(ax, box_x + box_w/2, 3.2, wire_y)
        ax.text(3.45, wire_y, label, ha='center', va='center',
                fontsize=11, fontfamily='serif')

    ax.set_title('After fusion', fontsize=11, pad=4)


fig = plt.figure(figsize=(7.5, 2.6))

gs = fig.add_gridspec(1, 3, width_ratios=[2.8, 0.35, 2.8],
                      left=0.01, right=0.99, top=0.88, bottom=0.04,
                      wspace=0.0)

ax_before = fig.add_subplot(gs[0])
ax_arrow  = fig.add_subplot(gs[1])
ax_after  = fig.add_subplot(gs[2])

make_before(ax_before)
make_after(ax_after)

# Arrow panel — vertically centred on the wire span
ax_arrow.set_xlim(0, 1)
ax_arrow.set_ylim(0, 1)
ax_arrow.axis('off')
mid = 0.52
ax_arrow.annotate(
    '', xy=(0.88, mid), xytext=(0.12, mid),
    arrowprops=dict(arrowstyle='->', color='black', lw=2.0),
)
ax_arrow.text(0.5, mid + 0.14, 'fuse', ha='center', va='bottom',
              fontsize=10, color='#444444')

fig.savefig('images/gate_fusion.pdf', bbox_inches='tight',
            dpi=200, transparent=True)
fig.savefig('images/gate_fusion.png', bbox_inches='tight',
            dpi=200, transparent=True)
print("Saved images/gate_fusion.pdf and images/gate_fusion.png")
