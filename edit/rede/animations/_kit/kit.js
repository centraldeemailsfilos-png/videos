/* Ajudantes de motion compartilhados pelas 12 cenas.
 *
 * Tudo com easing cubico — linear parece robotico — e tudo preso a
 * tempos medidos na narracao, nunca a estimativa.
 */

/* Move o cursor ate (x,y) chegando no instante `em`, depois encolhe:
 * o encolhimento e o toque, entao `em` deve ser o tempo da palavra. */
function toque(tl, { x, y, em, vindoDe, aproxima = 0.55, rotulo }) {
  const c = "#cursor";
  if (vindoDe) tl.set(c, { x: vindoDe.x, y: vindoDe.y }, Math.max(0, em - aproxima - 0.2));
  tl.to(c, { opacity: 1, duration: 0.22, ease: "power2.out" }, Math.max(0, em - aproxima - 0.18));
  tl.to(c, { x, y, duration: aproxima, ease: "power3.inOut" }, em - aproxima);
  tl.to(c, { scale: 0.62, duration: 0.11, ease: "power2.in"  }, em);
  tl.to(c, { scale: 1.00, duration: 0.24, ease: "power2.out" }, em + 0.11);
  return { x, y };
}

/* Desenha o traco de pincel em volta de um botao e apaga depois. */
function pincel(tl, sel, em, dura = 1.9) {
  const p = document.querySelector(sel + " path");
  const L = p.getTotalLength();
  p.style.strokeDasharray = L;
  p.style.strokeDashoffset = L;
  tl.set(sel, { opacity: 1 }, em - 0.25);
  tl.fromTo(p, { strokeDashoffset: L },
                { strokeDashoffset: 0, duration: 0.62, ease: "power2.inOut" }, em - 0.25);
  tl.to(sel, { opacity: 0, duration: 0.45, ease: "power2.inOut" }, em - 0.25 + dura);
}

/* Aproximacao de ~130% centrada num ponto do celular (secao 6: "antes do
 * toque, faca um zoom de cerca de 130%"). */
function aproxima(tl, alvo, { em, fator = 1.3, px, py, dura = 0.75, segura = 2.2 }) {
  tl.to(alvo, { scale: fator, transformOrigin: `${px}% ${py}%`,
                duration: dura, ease: "power2.inOut" }, em - dura);
  tl.to(alvo, { scale: 1, duration: 0.8, ease: "power2.inOut" }, em + segura);
}

/* Entrada padrao de texto: sobe pouco e aparece. Nunca dois ao mesmo tempo. */
function entra(tl, sel, em, dur = 0.62) {
  tl.fromTo(sel, { opacity: 0, y: 26 },
                 { opacity: 1, y: 0, duration: dur, ease: "power3.out" }, em);
}
function sai(tl, sel, em, dur = 0.45) {
  tl.to(sel, { opacity: 0, y: -16, duration: dur, ease: "power2.inOut" }, em);
}
