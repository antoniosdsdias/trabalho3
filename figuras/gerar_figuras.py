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
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2))

# fase 1: pessoa + carrinho no trilho
p_b = np.array([0, 0])
p_t = p_b + 9 * u
ax1.plot(*zip(p_b, p_t), color="black", lw=5)
ax1.plot([-1, 5], [0, 0], color="gray", ls="--", lw=1)
ax1.add_patch(Arc(tuple(p_b), 3, 3, theta1=0, theta2=70, lw=1.2))
ax1.text(1.75, 0.5, "α", fontsize=13)
c = p_b + 5 * u + 0.45 * nrm
bloco = [c + du * u + dn * nrm for du, dn in [(-0.7, -0.45), (0.7, -0.45), (0.7, 0.45), (-0.7, 0.45)]]
ax1.add_patch(Polygon(bloco, color="#e0efef", ec="black", zorder=4))
seta(ax1, c, c + 2.6 * u, COR_FORCA, "$F_{el}$", (-0.6, 0.15))
seta(ax1, c, c - 1.8 * u, COR_ATRITO, "$F_{at}$", (-0.6, -0.2))
seta(ax1, c, c + 2.0 * nrm, COR_FORCA, "$N$", (-0.35, 0.2))
seta(ax1, c, c + np.array([0, -2.8]), COR_FORCA, "$P$", (0.45, -0.1))
seta(ax1, np.array([4.0, 1.0]), np.array([4.0, 1.0]) + 1.5 * u, COR_VEL, "s", (0.3, 0.1), lw=1.5)
ax1.set_xlim(-1.5, 6)
ax1.set_ylim(-0.5, 10)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("Fase 1: dentro do canhão\ncorpo = pessoa + carrinho (m + M)", fontsize=12)

# fase 2: pessoa em voo
t = np.linspace(0, 1, 100)
ax2.plot(8 * t, 6 * t - 6 * t**2 + 1, color="gray", ls="--", lw=1.2)
p = np.array([2.0, 6 * 0.25 - 6 * 0.25**2 + 1])
dv = np.array([8, 6 - 12 * 0.25])
dv = dv / np.linalg.norm(dv)
ax2.plot(*p, "o", ms=14, color="#e0efef", mec="black", zorder=4)
seta(ax2, p, p + 1.8 * dv, COR_VEL, "$\\vec{v}$", (0.3, 0.15))
seta(ax2, p, p - 1.5 * dv, COR_FORCA, "$F_{ar}$", (-0.1, -0.45))
seta(ax2, p, p + np.array([0, -2.2]), COR_FORCA, "$P$", (0.4, 0))
seta(ax2, (5.5, -0.6), (7, -0.6), "black", "x", (0.3, 0), lw=1.5)
seta(ax2, (5.5, -0.6), (5.5, 0.9), "black", "y", (0, 0.3), lw=1.5)
ax2.set_xlim(-0.5, 8.5)
ax2.set_ylim(-1, 3.5)
ax2.set_aspect("equal")
ax2.axis("off")
ax2.set_title("Fase 2: em voo\ncorpo = pessoa (m)", fontsize=12)

fig.tight_layout()
fig.savefig("dcl.png", dpi=110)
plt.close(fig)
print("figuras geradas")
