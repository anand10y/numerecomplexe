# Fișier complet Streamlit: numere_complexe_lectie.py
# Lecție interactivă numere complexe (bază)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages

st.set_page_config(page_title="Numere complexe — lecție interactivă", layout="wide")


# ======= CSS pentru mărirea textului în toată aplicația =======
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 20px !important;  /* mărime text general */
    }
    h1, h2, h3, h4 {
        font-size: 26px !important;  /* titluri mai mari */
    }
    .stMarkdown p, .stMarkdown li {
        font-size: 20px !important;  /* paragrafe și liste */
    }
    .stRadio label, .stCheckbox label, .stTextInput label {
        font-size: 20px !important;  /* etichete inputuri */
    }
    .stButton button {
        font-size: 20px !important;  /* butoane */
    }
    </style>
""", unsafe_allow_html=True)



# --- Helper functions ---
def format_complex(z):
    a = int(z.real) if z.real.is_integer() else z.real
    b = int(z.imag) if z.imag.is_integer() else z.imag
    if b >= 0:
        return f"{a}+{b}i"
    else:
        return f"{a}{b}i"

def parse_answer(ans: str):
    try:
        s = ans.strip().replace(' ', '').replace('i','j')
        return complex(s)
    except:
        return None

def plot_complex_points(points, vectors=None, title="Planul complex"):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    xs = [p.real for p in points]
    ys = [p.imag for p in points]
    ax.scatter(xs, ys)
    for i,p in enumerate(points):
        ax.annotate(f"z_{i} = {format_complex(p)}", (p.real, p.imag))
    if vectors:
        for v in vectors:
            ax.arrow(0,0, v.real, v.imag, head_width=0.1, length_includes_head=True)
    lim = max(1.5, max(np.abs(xs+ys))) if xs or ys else 2
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.set_title(title)
    ax.set_aspect('equal', 'box')
    return fig

# --- UI ---
st.title("Numere complexe — lecție interactivă")
page = st.sidebar.radio("Secțiune", ["Teorie", "Vizualizare", "Exerciții", "Recapitulare", "Vizualizare LaTeX/PDF"]) 

# --- Teorie ---
if page == "Teorie":
    st.header("Teorie — Numere complexe")
    st.subheader("Definiție")
   # st.latex(r"z = a + bi, \\quad a,b \in \mathbb{R}, \\ i^2 = -1")
    st.latex(r"z = a + bi, \; a,b \in \mathbb{R}, \; i^2 = -1")
    st.markdown("**Partea reală:** $\\Re z = a$  ")
    st.markdown("**Partea imaginară:** $\\Im z = b$")
    st.subheader("Operații")
    st.latex(r"(a+bi) + (c+di) = (a+c) + (b+d)i")
    st.latex(r"(a+bi)(c+di) = (ac - bd) + (ad+bc)i")
    st.latex(r"\overline{z} = a - bi")
    st.latex(r"|z| = \sqrt{a^2 + b^2}")
    st.subheader("Exemple")
    st.latex(r"(2+3i) + (1-4i) = 3 - i")
    st.latex(r"(2+3i)(1-4i) = 14 - 5i")

# --- Vizualizare plan complex ---
elif page == "Vizualizare":
    a1 = st.number_input('Re z1', value=1, key='a1')
    b1 = st.number_input('Im z1', value=1, key='b1')
    a2 = st.number_input('Re z2', value=0, key='a2')
    b2 = st.number_input('Im z2', value=0, key='b2')
    show_sum = st.checkbox('Arată suma z1+z2', value=True)
    show_product = st.checkbox('Arată produsul z1*z2', value=True)
    show_vectors = st.checkbox('Arată vectori', value=True)
    z1 = complex(a1,b1)
    z2 = complex(a2,b2)
    points = [z1]
    if a2!=0 or b2!=0: points.append(z2)
    vectors = points if show_vectors else None
    ops_text = []
    if show_sum and len(points)>1:
        s = z1+z2
        ops_text.append(f"z1 + z2 = {format_complex(s)}")
        points.append(s)
    if show_product and len(points)>1:
        p = z1*z2
        ops_text.append(f"z1 * z2 = {format_complex(p)}")
        points.append(p)
    fig = plot_complex_points(points, vectors=vectors)
    st.pyplot(fig)
    for t in ops_text: st.write(t)

# --- Exerciții ---
elif page == "Exerciții":
    if 'exercise_set' not in st.session_state:
        z1 = complex(np.random.randint(-3,4), np.random.randint(-3,4))
        z2 = complex(np.random.randint(-3,4), np.random.randint(-3,4))
        st.session_state.exercise_set = {
            'z1': z1,
            'z2': z2,
            'sum': z1+z2,
            'prod': z1*z2,
            'mod_z1': abs(z1),
            'conj_z2': np.conjugate(z2),
            'lin_comb': 2*z1 + 3*z2
        }

    ex = st.session_state.exercise_set
    z1, z2 = ex['z1'], ex['z2']

    st.markdown(f"**Exercițiu cu z1 = {format_complex(z1)}, z2 = {format_complex(z2)}**")

    ans_sum = st.text_input('Răspuns — z1+z2', key='s1')
    ans_prod = st.text_input('Răspuns — z1*z2', key='p1')
    ans_mod = st.text_input('Răspuns — |z1|', key='m1')
    ans_conj = st.text_input('Răspuns — conjugatul lui z2', key='c1')
    ans_lin = st.text_input('Răspuns — 2z1+3z2', key='l1')

    show_steps = st.checkbox('Arată pași', key='steps')

    if st.button('Verifică') or show_steps:
        # verificare sumă
        if ans_sum:
            user = parse_answer(ans_sum)
            st.info(f"z1+z2: {'Corect' if user and abs(user-ex['sum'])<1e-6 else 'Greșit'}, corect = {format_complex(ex['sum'])}")
        # verificare produs
        if ans_prod:
            user = parse_answer(ans_prod)
            st.info(f"z1*z2: {'Corect' if user and abs(user-ex['prod'])<1e-6 else 'Greșit'}, corect = {format_complex(ex['prod'])}")
        # verificare modul
        if ans_mod:
            try:
                user = float(ans_mod.replace(',', '.'))
                st.info(f"|z1|: {'Corect' if abs(user-ex['mod_z1'])<1e-6 else 'Greșit'}, corect = {round(ex['mod_z1'],3)}")
            except:
                st.error("Modulul trebuie introdus ca număr real (ex. 2.236)")
        # verificare conjugat
        if ans_conj:
            user = parse_answer(ans_conj)
            st.info(f"Conjugatul lui z2: {'Corect' if user and abs(user-ex['conj_z2'])<1e-6 else 'Greșit'}, corect = {format_complex(ex['conj_z2'])}")
        # verificare combinație liniară
        if ans_lin:
            user = parse_answer(ans_lin)
            st.info(f"2z1+3z2: {'Corect' if user and abs(user-ex['lin_comb'])<1e-6 else 'Greșit'}, corect = {format_complex(ex['lin_comb'])}")

        if show_steps:
            st.latex(rf"z_1 = {format_complex(z1)}, \quad z_2 = {format_complex(z2)}")
            st.latex(rf"z_1 + z_2 = {format_complex(ex['sum'])}")
            st.latex(rf"z_1 z_2 = {format_complex(ex['prod'])}")
            st.latex(rf"|z_1| = {round(ex['mod_z1'],3)}")
            st.latex(rf"\overline{{z_2}} = {format_complex(ex['conj_z2'])}")
            st.latex(rf"2z_1 + 3z_2 = {format_complex(ex['lin_comb'])}")



# --- Recapitulare ---
elif page == "Recapitulare":
    st.header("Recapitulare – mini-test")
    
    if 'recap_list' not in st.session_state:
        # Generăm 3 exerciții random
        st.session_state.recap_list = [
            {'z1': complex(np.random.randint(-3,4), np.random.randint(-3,4)),
             'z2': complex(np.random.randint(-3,4), np.random.randint(-3,4))}
            for _ in range(3)
        ]
    
    answers = []
    for i, ex in enumerate(st.session_state.recap_list):
        z1, z2 = ex['z1'], ex['z2']
        st.markdown(f"**Exercițiu {i+1}:** Calculați suma și produsul lui {format_complex(z1)} și {format_complex(z2)}")
        ans_sum = st.text_input(f"Sumă z1+z2", key=f"recap_sum_{i}")
        ans_prod = st.text_input(f"Produs z1*z2", key=f"recap_prod_{i}")
        answers.append({'z1': z1, 'z2': z2, 'ans_sum': ans_sum, 'ans_prod': ans_prod})
    
    if st.button("Verifică răspunsuri recapitulare"):
        for i, a in enumerate(answers):
            correct_sum = a['z1'] + a['z2']
            correct_prod = a['z1'] * a['z2']
            user_sum = parse_answer(a['ans_sum'])
            user_prod = parse_answer(a['ans_prod'])
            
            st.markdown(f"**Exercițiu {i+1}:**")
            if user_sum is not None:
                st.success(f"Sumă corect? {'Da' if abs(user_sum-correct_sum)<1e-6 else 'Nu'}, răspuns corect: {format_complex(correct_sum)}")
            if user_prod is not None:
                st.success(f"Produs corect? {'Da' if abs(user_prod-correct_prod)<1e-6 else 'Nu'}, răspuns corect: {format_complex(correct_prod)}")

# --- Vizualizare LaTeX/PDF ---
elif page == "Vizualizare LaTeX/PDF":
    st.header("Vizualizare lecție în LaTeX")
    st.latex(r"z = a + bi, \quad a,b \in \mathbb{R}, \quad i^2 = -1")
    st.markdown("**Partea reală:** $\\Re z = a$")
    st.markdown("**Partea imaginară:** $\\Im z = b$")
    st.latex(r"(a+bi) + (c+di) = (a+c) + (b+d)i")
    st.latex(r"(a+bi)(c+di) = (ac-bd) + (ad+bc)i")
    st.latex(r"\overline{z} = a - bi")
    st.latex(r"|z| = \sqrt{a^2 + b^2}")
    st.latex(r"(2+3i) + (1-4i) = 3 - i")
    st.latex(r"(2+3i)(1-4i) = 14 - 5i")

    LATEX_LESSON = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,amsthm}
\title{Numere complexe — Lecție (bază)}
\begin{document}
\maketitle
\section*{Definiție}
z = a + bi, a,b \in \mathbb{R}, i^2 = -1
\section*{Operații}
(a+bi) + (c+di) = (a+c) + (b+d)i
(a+bi)(c+di) = (ac-bd) + (ad+bc)i
Conjugat: \overline{z} = a-bi
Modul: |z| = \sqrt{a^2+b^2}
\section*{Exemple}
(2+3i) + (1-4i) = 3 - i
(2+3i)(1-4i) = 14 - 5i
\end{document}"""
    st.download_button('Descarcă .tex', data=LATEX_LESSON.encode('utf-8'), file_name='lectie_numere_complexe.tex', mime='text/x-tex')

    buf = BytesIO()
    with PdfPages(buf) as pdf:
        fig, ax = plt.subplots(figsize=(8,10))
        ax.axis('off')
        lesson_text = (
            "Numere complexe – Lecție (bază)\n\n"
            "Definiție:\n"
            "z = a + bi, a,b ∈ R, i^2 = -1\n"
            "Partea reală: Re z = a\n"
            "Partea imaginară: Im z = b\n\n"
            "Operații:\n"
            "(a+bi) + (c+di) = (a+c) + (b+d)i\n"
            "(a+bi)(c+di) = (ac-bd) + (ad+bc)i\n"
            "Conjugat: z̄ = a - bi\n"
            "Modul: |z| = sqrt(a^2 + b^2)\n\n"
            "Exemple:\n"
            "(2+3i) + (1-4i) = 3 - i\n"
            "(2+3i)(1-4i) = 14 - 5i"
        )
        ax.text(0.01, 0.99, lesson_text, verticalalignment='top', fontsize=12)
        pdf.savefig(fig)
        plt.close()

    st.download_button('Descarcă PDF lecție', data=buf.getvalue(), file_name='lectie_numere_complexe.pdf', mime='application/pdf')
