from flask import Flask, render_template, request
import math

#  Gemini API 相关导入
from google import genai
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in Render environment variables.")

client = genai.Client(api_key=GOOGLE_API_KEY)




app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    return render_template("main.html")

# 常见物理公式数据库（按主题分类）
FORMULAS_DB = {
    "Mechanics": [
        {"name": "Newton's Second Law", "latex": r"F = ma"},
        {"name": "Kinetic Energy", "latex": r"E_k = \tfrac{1}{2}mv^2"},
        {"name": "Gravitational Potential Energy", "latex": r"E_p = mgh"},
        {"name": "Momentum", "latex": r"p = mv"},
        {"name": "Pendulum Period", "latex": r"T = 2\pi \sqrt{\tfrac{L}{g}}"}
    ],
    "Kinematics": [
        {"name": "SUVAT Equation 1", "latex": r"s = ut + \tfrac{1}{2}at^2"},
        {"name": "SUVAT Equation 2", "latex": r"v = u + at"},
        {"name": "SUVAT Equation 3", "latex": r"v^2 = u^2 + 2as"}
    ],
    "Electricity": [
        {"name": "Ohm's Law", "latex": r"V = IR"},
        {"name": "Electrical Power", "latex": r"P = VI"},
        {"name": "Energy in Circuits", "latex": r"E = VIt"}
    ],
    "Waves": [
        {"name": "Wave Speed", "latex": r"v = f\lambda"},
        {"name": "Snell's Law", "latex": r"n_1 \sin \theta_1 = n_2 \sin \theta_2"}
    ],
    "Thermal Physics": [
        {"name": "Heat Energy", "latex": r"Q = mc\Delta T"},
        {"name": "Ideal Gas Law", "latex": r"pV = nRT"}
    ]
}

@app.route("/formulas", methods=["GET"])
def formulas():
    return render_template("formulas.html", formulas=FORMULAS_DB)




# 单摆公式 T = 2π√(L/g)
@app.route("/pendulum", methods=["POST"])
def pendulum():
    L = request.form.get("L")
    g = request.form.get("g")

    try:
        L_val = float(L)
        g_val = float(g)
        if L_val <= 0 or g_val <= 0:
            result = "Error: L and g must be positive numbers."
        else:
            T = 2 * math.pi * math.sqrt(L_val / g_val)
            result = f"Pendulum period T = {T:.2f} seconds"
    except ValueError:
        result = "Error: Invalid input."

    return render_template("main.html", r=result, L=L, g=g)

# SUVAT s = ut + 0.5at^2
@app.route("/suvat", methods=["POST"])
def suvat():
    u = request.form.get("u")
    a = request.form.get("a")
    t = request.form.get("t")

    try:
        u_val = float(u)
        a_val = float(a)
        t_val = float(t)
        s = u_val * t_val + 0.5 * a_val * t_val**2
        result = f"Displacement s = {s:.2f} meters"
    except ValueError:
        result = "Error: Invalid input."

    return render_template("main.html", r=result, u=u, a=a, t=t)

# Ohm's law I = V/R
@app.route("/ohm", methods=["POST"])
def ohm():
    V = request.form.get("V")
    R = request.form.get("R")

    try:
        V_val = float(V)
        R_val = float(R)
        if R_val == 0:
            result = "Error: Resistance cannot be zero."
        else:
            I = V_val / R_val
            result = f"Current I = {I:.2f} A"
    except ValueError:
        result = "Error: Invalid input."

    return render_template("main.html", r=result, V=V, R=R)

# Gemini API 路由保留
@app.route("/makersuite_gen", methods=["POST"])
def makersuite_gen():
    q = request.form.get("q")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=q
        )
        reply = response.text
    except Exception as e:
        reply = f"Error: {str(e)}"
    return render_template("main.html", r=reply)

if __name__ == "__main__":
    app.run(debug=True)
