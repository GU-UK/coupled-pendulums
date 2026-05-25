import numpy as np
import plotly.graph_objects as go


def spring_points(x1, y1, x2, y2, coils=12):

    t = np.linspace(0, 1, 120)

    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t

    dx = x2 - x1
    dy = y2 - y1

    length = np.sqrt(dx**2 + dy**2)

    if length == 0:
        return x, y

    nx = -dy / length
    ny = dx / length

    amp = 0.05

    x += amp * np.sin(t * coils * 2 * np.pi) * nx
    y += amp * np.sin(t * coils * 2 * np.pi) * ny

    return x, y


def create_animation(result, L, L1):

    frames = []

    for i in range(len(result["phi1"])):

        phi1 = result["phi1"][i]
        phi2 = result["phi2"][i]

        x1 = -1 + L * np.sin(phi1)
        y1 = -L * np.cos(phi1)

        x2 = 1 + L * np.sin(phi2)
        y2 = -L * np.cos(phi2)

        sx1 = -1 + L1 * np.sin(phi1)
        sy1 = -L1 * np.cos(phi1)

        sx2 = 1 + L1 * np.sin(phi2)
        sy2 = -L1 * np.cos(phi2)

        xs, ys = spring_points(
            sx1,
            sy1,
            sx2,
            sy2
        )

        frames.append(

            go.Frame(

                data=[

                    go.Scatter(
                        x=[-1, x1],
                        y=[0, y1],
                        mode="lines",
                        line=dict(
                            width=6
                        ),
                        showlegend=False
                    ),

                    go.Scatter(
                        x=[1, x2],
                        y=[0, y2],
                        mode="lines",
                        line=dict(
                            width=6
                        ),
                        showlegend=False
                    ),

                    go.Scatter(
                        x=xs,
                        y=ys,
                        mode="lines",
                        line=dict(
                            width=3
                        ),
                        showlegend=False
                    ),

                    go.Scatter(
                        x=[x1],
                        y=[y1],
                        mode="markers",
                        marker=dict(
                            size=35
                        ),
                        showlegend=False
                    ),

                    go.Scatter(
                        x=[x2],
                        y=[y2],
                        mode="markers",
                        marker=dict(
                            size=35
                        ),
                        showlegend=False
                    )
                ]
            )
        )

    fig = go.Figure(
        data=frames[0].data,
        frames=frames
    )

    fig.update_layout(
        height=750,

        margin=dict(
            l=20,
            r=20,
            t=80,
            b=20
        ),

    xaxis=dict(
        visible=True,
        range=[-2.2, 2.2],
        showgrid=True,
        zeroline=True,
        title="x, м"
    ),

    yaxis=dict(
        visible=True,
        range=[-1.5 * L, 0.3],
        showgrid=True,
        zeroline=True,
        scaleanchor="x",
        title="y, м"
    ),

        showlegend=False,

        updatemenus=[

            dict(

                type="buttons",

                direction="left",

                x=0,

                y=1.02,
                
                pad=dict(
                    t=0,
                    r=0
                ),

                showactive=False,

                buttons=[

                    dict(

                        label="▶ Запуск",

                        method="animate",

                        args=[

                            None,

                            {

                                "frame": {
                                    "duration": 20
                                },

                                "transition": {
                                    "duration": 0
                                },

                                "fromcurrent": True
                            }
                        ]
                    )
                ]
            )
        ]
    )

    return fig