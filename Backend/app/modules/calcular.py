from scipy.integrate import solve_ivp
import numpy as np

def simular_epidemia(N, I0, p_vac, dias, beta, gamma, dia_intervencion, factor_intervencion):

    # ── Intervención
    dia_int   = int(dia_intervencion)
    beta_post = beta * factor_intervencion

    # ── Condiciones iniciales
    R_init = N * p_vac
    S_init = N - I0 - R_init
    I_init = I0

    # ── Validación
    if S_init < 0:
        raise ValueError('Infectados iniciales + vacunados superan la población total')

    # ── Modelo SIR con beta variable por intervención
    def sir(t, y):
        S, I, R = y
        b  = beta if t < dia_int else beta_post
        dS = -b * S * I / N
        dI =  b * S * I / N - gamma * I
        dR =  gamma * I
        return [dS, dI, dR]

    # ── Resolución numérica RK45
    t_eval = np.arange(0, dias + 1, dtype=float)

    sol = solve_ivp(
        fun=sir,
        t_span=(0.0, float(dias)),
        y0=[S_init, I_init, R_init],
        method='RK45',
        t_eval=t_eval,
        dense_output=False,
        rtol=1e-6,
        atol=1e-8,
    )

    if not sol.success:
        raise RuntimeError('La simulación no convergió: ' + sol.message)

    # ── Resultado como diccionario puro (sin Flask)
    return {
        't': sol.t.tolist(),
        'S': [round(v) for v in sol.y[0]],
        'I': [round(v) for v in sol.y[1]],
        'R': [round(v) for v in sol.y[2]],
    }