# Gera as figuras do notebook do Projeto 3 (canhão humano).
# Rodar com a pasta figuras/ como diretório atual: python gerar_figuras.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch, Arc

COR_FORCA = "#c2461b"
COR_ATRITO = "#5a49a8"
COR_VEL = "#0d6b73"
COR_AGUA = "#9fd3e6"


def seta(ax, p0, p1, cor, texto=None, desloc=(0, 0), lw=2.5):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=18,
                                 color=cor, lw=lw, zorder=5))
    if texto:
        ax.text(p1[0] + desloc[0], p1[1] + desloc[1], texto, color=cor,
                fontsize=13, ha="center", va="center", zorder=6)


# ---------------------------------------------------------------- esquema físico
fig, ax = plt.subplots(figsize=(9, 6))
a = np.radians(70)

# água e chão
ax.add_patch(Polygon([[-6, -1.5], [22, -1.5], [22, -4], [-6, -4]], color=COR_AGUA, zorder=0))
ax.plot([-6, 1.2], [0, 0], color="#8a7f6e", lw=3)
ax.plot([1.2, 1.2], [0, -1.5], color="#8a7f6e", lw=3)
ax.text(14, -2.8, "água", fontsize=12, color="#1d5d73")

# andaime
for xa in [-1.5, 0.6]:
    ax.plot([xa, xa], [0, 10], color="gray", lw=1.5)
for ya in np.arange(0, 10.1, 2):
    ax.plot([-1.5, 0.6], [ya, ya], color="gray", lw=1)
for ya in np.arange(0, 10, 2):
    ax.plot([-1.5, 0.6], [ya, ya + 2], color="gray", lw=0.8)

# trilho (fora de escala: base no chão, boca a 10 m)
xb, yb = -10 / np.tan(a), 0
ax.plot([xb, 0], [yb, 10], color="black", lw=5, solid_capstyle="butt", zorder=3)
ax.text(-3.4, 6.2, "trilho do canhão\nL = 12,5 m", fontsize=11, ha="right")

# carrinho com a pessoa no meio do trilho
s_c = 0.45
xc, yc = xb * (1 - s_c), 10 * s_c
u = np.array([np.cos(a), np.sin(a)])
nrm = np.array([-np.sin(a), np.cos(a)])
cant = [np.array([xc, yc]) + du * u + dn * nrm for du, dn in [(-0.5, 0), (0.5, 0), (0.5, 0.4), (-0.5, 0.4)]]
ax.add_patch(Polygon(cant, color="#e0efef", ec="black", zorder=4))
ax.plot(*zip(np.array([xc, yc]) + 0.2 * nrm, np.array([xc, yc]) + 0.2 * nrm + 1.6 * u), color="#c2461b", lw=4, zorder=4)
ax.text(xc - 0.9, yc - 0.3, "carrinho (M)\n+ pessoa (m)", fontsize=10, va="top", ha="right")

# elástico (puxa o carrinho para cima)
ax.plot([xc + 0.5 * np.cos(a), 0.15], [yc + 0.5 * np.sin(a), 10.6], color=COR_FORCA, lw=1.5, ls=(0, (4, 2)))
ax.text(0.7, 9.0, "elásticos", color=COR_FORCA, fontsize=10)

# ângulo
ax.add_patch(Arc((xb, yb), 3, 3, theta1=0, theta2=70, lw=1.2))
ax.text(xb + 1.9, 0.45, "α = 70°", fontsize=11)

# trajetória (ilustrativa)
v0 = 14.0
t = np.linspace(0, 4, 400)
xt = v0 * np.cos(a) * t
yt = 10 + v0 * np.sin(a) * t - 9.81 * t**2 / 2
ok = yt >= -1.5
ax.plot(xt[ok], yt[ok], ls="--", color=COR_VEL, lw=1.5)
seta(ax, (0, 10), (1.6 * np.cos(a) * 1.5, 10 + 1.6 * np.sin(a) * 1.5), COR_VEL, "$\\vec{V}_0$", (0.7, 0.2))
ax.plot([4.5, 9], [yt.max(), yt.max()], color="black", lw=0.8)
ax.annotate("", (8.4, yt.max()), (8.4, 0), arrowprops=dict(arrowstyle="<->", lw=1))
ax.text(8.6, yt.max() / 2, "$H_{max}$ (a partir do chão)", fontsize=11)

# cotas
ax.annotate("", (2.2, 10), (2.2, 0), arrowprops=dict(arrowstyle="<->", lw=1))
ax.text(2.4, 4.6, "10 m", fontsize=11)
ax.annotate("", (3.6, 0), (3.6, -1.5), arrowprops=dict(arrowstyle="<->", lw=1))
ax.text(3.8, -0.9, "1,5 m", fontsize=10)

# eixos
seta(ax, (-5.5, -3.4), (-3.5, -3.4), "black", "x", (0.3, 0), lw=1.5)
seta(ax, (-5.5, -3.4), (-5.5, -1.6), "black", "y", (0, 0.35), lw=1.5)
ax.text(-2.4, -3.75, "origem: chão, abaixo da boca do canhão", fontsize=8)

ax.set_xlim(-6, 22)
ax.set_ylim(-4, 22)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Esquema do sistema (fora de escala)", fontsize=13)
fig.tight_layout()
fig.savefig("esquema_fisico.png", dpi=110)
plt.close(fig)

# ---------------------------------------------------------------- DCL
# eixos t (tangente, sentido da velocidade) e n (normal) que andam com o corpo
COR_EIXO = "#333333"
COR_COMP = "#d9895f"


def comp(ax, p0, p1, texto, desloc):
    # componente do peso (tracejada)
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=14,
                                 color=COR_COMP, lw=1.6, ls="--", zorder=4))
    ax.text(p1[0] + desloc[0], p1[1] + desloc[1], texto, color=COR_COMP,
            fontsize=11, ha="center", va="center", zorder=6)


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5.6))

# instante 1: parado no canhão, preso pelo elástico (s = 0)
p_b = np.array([0, 0])
p_t = p_b + 9 * u
ax1.plot(*zip(p_b, p_t), color="black", lw=5)
ax1.plot([-1, 5], [0, 0], color="gray", ls="--", lw=1)
ax1.add_patch(Arc(tuple(p_b), 2.4, 2.4, theta1=0, theta2=70, lw=1.2))
ax1.text(1.45, 0.4, "α", fontsize=13)
c = p_b + 4.6 * u + 0.45 * nrm
bloco = [c + du * u + dn * nrm for du, dn in [(-0.7, -0.45), (0.7, -0.45), (0.7, 0.45), (-0.7, 0.45)]]
ax1.add_patch(Polygon(bloco, color="#e0efef", ec="black", zorder=3))
ax1.plot(*zip(c + 0.7 * u, p_t + 0.3 * nrm), color=COR_FORCA, lw=1.2, ls=(0, (4, 2)))
ax1.text(*(p_t + 0.7 * nrm + np.array([0, -0.6])), "elásticos", color=COR_FORCA, fontsize=9, ha="right")
seta(ax1, c, c + 2.8 * u, COR_FORCA, "$F_{el}$", (-0.55, 0.1))
seta(ax1, c - 0.4 * nrm, c - 0.4 * nrm - 1.3 * u, COR_ATRITO, "$F_{at}$", (0.75, 0.2))
seta(ax1, c + 0.35 * nrm, c + 0.35 * nrm - 1.0 * u, COR_FORCA, "$F_{ar}$", (-0.55, 0.0))
seta(ax1, c, c + 1.9 * nrm, COR_FORCA, "$N$", (-0.3, 0.25))
seta(ax1, c, c + np.array([0, -2.4]), COR_FORCA, "$P$", (0.4, -0.1))
comp(ax1, c, c - 2.4 * np.sin(a) * u, "$P\\,\\mathrm{sen}\\,\\alpha$", (-1.0, 0.1))
comp(ax1, c, c - 2.4 * np.cos(a) * nrm, "$P\\cos\\alpha$", (0.9, 0.05))
o = np.array([4.2, 2.6])
seta(ax1, o, o + 1.4 * u, COR_EIXO, "t", (0.25, 0.1), lw=1.5)
seta(ax1, o, o + 1.4 * nrm, COR_EIXO, "n", (-0.15, 0.25), lw=1.5)
ax1.text(2.2, -1.4, "em n: $N - P\\cos\\alpha = 0$  →  $N = P\\cos\\alpha$\n"
                    "em t: $F_{el} - P\\,\\mathrm{sen}\\,\\alpha - F_{at} - F_{ar} = (m+M)\\,a_t$\n"
                    "($F_{ar} = 0$ no repouso e cresce com $v^2$)",
         fontsize=10.5, ha="center", va="top")
ax1.set_xlim(-2, 6.5)
ax1.set_ylim(-2.6, 9.5)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("1) No canhão: sai do repouso e sobe o trilho\ncorpo = pessoa + carrinho (m + M)", fontsize=12)

# instante 2: em voo, subindo
tt = np.linspace(0, 1, 100)
ax2.plot(8 * tt, 7 * tt - 7 * tt**2 + 1, color="gray", ls="--", lw=1.2)
tp = 0.18
p = np.array([8 * tp, 7 * tp - 7 * tp**2 + 1])
dv = np.array([8, 7 - 14 * tp])
dv = dv / np.linalg.norm(dv)
dn = np.array([dv[1], -dv[0]])          # normal para o lado de dentro da curva
teta = np.arctan2(dv[1], dv[0])
ax2.plot([p[0], p[0] + 1.6], [p[1], p[1]], color="gray", lw=0.8)
ax2.add_patch(Arc(tuple(p), 2.2, 2.2, theta1=0, theta2=np.degrees(teta), lw=1.1))
ax2.text(p[0] + 1.25, p[1] + 0.3, "θ", fontsize=12)
ax2.plot(*p, "o", ms=14, color="#e0efef", mec="black", zorder=3)
seta(ax2, p, p + 2.0 * dv, COR_VEL, "$\\vec{v}$", (0.1, 0.3))
seta(ax2, p - 0.3 * dn, p - 0.3 * dn - 1.3 * dv, COR_FORCA, "$F_{ar}$", (-0.2, 0.3))
seta(ax2, p, p + np.array([0, -2.2]), COR_FORCA, "$P$", (-0.35, -0.1))
comp(ax2, p, p - 2.2 * np.sin(teta) * dv, "$P\\,\\mathrm{sen}\\,\\theta$", (-0.6, -0.4))
comp(ax2, p, p + 2.2 * np.cos(teta) * dn, "$P\\cos\\theta$", (0.75, -0.1))
o = np.array([5.6, 2.7])
seta(ax2, o, o + 1.2 * dv, COR_EIXO, "t", (0.2, 0.1), lw=1.5)
seta(ax2, o, o + 1.2 * dn, COR_EIXO, "n", (0.25, -0.1), lw=1.5)
ax2.text(4.0, -1.6, "$\\cos\\theta = v_x / v$     $\\mathrm{sen}\\,\\theta = v_y / v$\n"
                    "em t: $-F_{ar} - P\\,\\mathrm{sen}\\,\\theta = m\\,a_t$\n"
                    "em n: $P\\cos\\theta = m\\,v^2 / r$ (curva a trajetória)",
         fontsize=10.5, ha="center", va="top")
ax2.set_xlim(-1.5, 8.5)
ax2.set_ylim(-3.6, 3.6)
ax2.set_aspect("equal")
ax2.axis("off")
ax2.set_title("2) Em voo, subindo\ncorpo = pessoa (m)", fontsize=12)

# instante 3: altura máxima (θ = 0)
p = np.array([4.0, 2.75])
ax3.plot(8 * tt, 7 * tt - 7 * tt**2 + 1, color="gray", ls="--", lw=1.2)
ax3.plot(*p, "o", ms=14, color="#e0efef", mec="black", zorder=3)
seta(ax3, p, p + np.array([2.0, 0]), COR_VEL, "$\\vec{v} = v_x$", (0.3, 0.35))
seta(ax3, p, p + np.array([-1.3, 0]), COR_FORCA, "$F_{ar}$", (-0.2, 0.3))
seta(ax3, p, p + np.array([0, -2.2]), COR_FORCA, "$P$", (0.35, -0.1))
o = np.array([6.6, 0.4])
seta(ax3, o, o + np.array([1.2, 0]), COR_EIXO, "t", (0.2, 0.1), lw=1.5)
seta(ax3, o, o + np.array([0, -1.2]), COR_EIXO, "n", (0.25, -0.1), lw=1.5)
ax3.text(4.0, -1.6, "$\\theta = 0$  →  $v_y = 0$: velocidade toda horizontal\n"
                    "em t: $-F_{ar} = m\\,a_t$ (peso sem parte tangente)\n"
                    "em n: $P = m\\,v^2 / r$ (peso todo na normal)",
         fontsize=10.5, ha="center", va="top")
ax3.set_xlim(-1.5, 8.5)
ax3.set_ylim(-3.6, 3.6)
ax3.set_aspect("equal")
ax3.axis("off")
ax3.set_title("3) Na altura máxima\ncorpo = pessoa (m)", fontsize=12)

fig.tight_layout()
fig.savefig("dcl.png", dpi=110)
plt.close(fig)
print("figuras geradas")
