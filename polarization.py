#Usage usage: polarization.py [-h] [--l L] [--w W] [--Ax AX] [--Ay AY] [--duration DURATION] [--dt DT] [--elev ELEV] [--azim AZIM]

#Animate a 3D quiver wave with adjustable parameters and camera.

#options:
#  -h, --help           show this help message and exit 
#  --l L                Wave length ℓ (default=1.0)
#  --w W                Angular frequency ω (default=1.0)
#  --Ax AX              Amplitude Aₓ (default=0.02)
#  --Ay AY              Amplitude Aᵧ (default=0.02)
#  --duration DURATION  Total animation time (s) (default=10.0)
#  --dt DT              Time step between frames (s) (default=0.1)
#  --elev ELEV          Camera elevation angle (deg) (default=None)
#  --azim AZIM          Camera azimuth angle (deg) (default=None)
#
#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def parse_args():
    p = argparse.ArgumentParser(
        description="Animate a 3D quiver wave with adjustable parameters and camera."
    )
    # wave parameters
    p.add_argument("--l",      type=float, default=1.0, help="Wave length ℓ")
    p.add_argument("--w",      type=float, default=1.0, help="Angular frequency ω")
    p.add_argument("--Ax",     type=float, default=0.02, help="Amplitude Aₓ")
    p.add_argument("--Ay",     type=float, default=0.02, help="Amplitude Aᵧ")
    p.add_argument("--duration", type=float, default=10.0,
                   help="Total animation time (s)")
    p.add_argument("--dt",      type=float, default=0.1,
                   help="Time step between frames (s)")

    # camera controls
    p.add_argument("--elev", type=float, default=None,
                   help="Camera elevation angle (deg)")
    p.add_argument("--azim", type=float, default=None,
                   help="Camera azimuth angle (deg)")

    return p.parse_args()

def main():
    args = parse_args()

    # unpack
    l, w, Ax, Ay = args.l, args.w, args.Ax, args.Ay
    zp     = np.linspace(0, 5, 150)
    frames = np.arange(0, args.duration + 1e-8, args.dt)

    # figure & 3D axes
    fig = plt.figure(figsize=(8,6))
    ax  = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    # initial camera: just set vertical_axis='y'
    ax.view_init(vertical_axis='y')

    artists = []
    def update(i):
        nonlocal artists
        # remove previous arrows
        for art in artists:
            art.remove()
        artists = []

        t = frames[i]
        dx = Ax * np.cos(w*t - zp*2*np.pi/l)
        dy = Ay * np.sin(w*t - zp*2*np.pi/l)
        dz = np.zeros_like(zp)

        # draw quivers
        for j, z in enumerate(zp):
            lbl = 'wave' if j == 0 else None
            q = ax.quiver(
                0, 0, z,
                dx[j], dy[j], dz[j],
                color='r', arrow_length_ratio=0.1,
                linewidth=1, alpha=0.7,
                label=lbl
            )
            artists.append(q)

        # update title
        ax.set_title(f'3D Wave (t = {t:.1f} s)')
        ax.view_init(vertical_axis='y')
        # apply camera angles, keep y vertical
        ax.view_init(
            elev=args.elev,
            azim=args.azim,
        )

        # legend only once
        if i == 0:
            ax.legend()

        return artists

    anim = FuncAnimation(
        fig, update,
        frames=len(frames),
        interval=100,  # ms
        blit=False
    )

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
