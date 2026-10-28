#!/usr/bin/env python3
"""Extract a curated frequent-verb set from Apertium Catalan (GPL-2.0)."""
from __future__ import annotations
import argparse, json, unicodedata
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work/apertium-cat/apertium-cat.cat.metadix"
OUT = ROOT / "data/verbs.json"

# Approximate pedagogical frequency order. It is deliberately labelled as such:
# Apertium supplies morphology, not a ranked frequency corpus.
VERBS = """ser haver estar fer poder dir anar veure donar saber voler arribar passar comprendre posar semblar quedar creure parlar portar deixar trobar tornar prendre conèixer viure sentir mirar esperar sortir treballar escriure perdre entendre començar entrar tenir buscar morir recordar acabar convertir mantenir aconseguir explicar preguntar tocar continuar canviar presentar crear obrir considerar permetre comprar servir seguir llegir caure córrer aparèixer rebre viatjar ajudar jugar estudiar menjar beure dormir aprendre vendre pagar enviar caminar escoltar estimar guanyar utilitzar decidir intentar necessitar existir pujar baixar néixer dur cabre venir treure riure respondre tancar patir descobrir triar oblidar preparar compartir conduir acceptar abandonar admetre afirmar agafar afegir aixecar anunciar apagar aplicar atendre augmentar avançar ballar celebrar cercar complir construir contenir contestar créixer cuidar declarar defensar dependre descriure desenvolupar desaparèixer desitjar despertar dirigir discutir ensenyar escollir evitar formar fugir funcionar guardar imaginar impedir incloure indicar informar iniciar insistir interessar llançar llevar lluitar millorar mostrar moure observar oferir omplir organitzar parar participar pensar pertànyer plorar produir provar publicar reconèixer reduir repetir resultar salvar seure significar somriure succeir suposar tallar témer tirar tractar unir visitar votar acostar acompanyar actuar aguantar alçar aprofitar assegurar atacar avisar besar cantar cobrar col·locar comunicar conservar controlar cuinar descansar dibuixar""".split()

TRANSLATIONS = dict(zip(VERBS, """ser|haber|estar|hacer|poder|decir|ir|ver|dar|saber|querer|llegar|pasar|comprender|poner|parecer|quedar|creer|hablar|llevar|dejar|encontrar|volver|tomar|conocer|vivir|sentir|mirar|esperar|salir|trabajar|escribir|perder|entender|empezar|entrar|tener|buscar|morir|recordar|acabar|convertir|mantener|conseguir|explicar|preguntar|tocar|continuar|cambiar|presentar|crear|abrir|considerar|permitir|comprar|servir|seguir|leer|caer|correr|aparecer|recibir|viajar|ayudar|jugar|estudiar|comer|beber|dormir|aprender|vender|pagar|enviar|caminar|escuchar|amar o querer|ganar|utilizar|decidir|intentar|necesitar|existir|subir|bajar|nacer|llevar|caber|venir|sacar|reír|responder|cerrar|sufrir|descubrir|elegir|olvidar|preparar|compartir|conducir|aceptar|abandonar|admitir|afirmar|coger|añadir|levantar|anunciar|apagar|aplicar|atender|aumentar|avanzar|bailar|celebrar|buscar|cumplir|construir|contener|contestar|crecer|cuidar|declarar|defender|depender|describir|desarrollar|desaparecer|desear|despertar|dirigir|discutir|enseñar|escoger|evitar|formar|huir|funcionar|guardar|imaginar|impedir|incluir|indicar|informar|iniciar|insistir|interesar|lanzar|quitar|luchar|mejorar|mostrar|mover|observar|ofrecer|llenar|organizar|parar|participar|pensar|pertenecer|llorar|producir|probar|publicar|reconocer|reducir|repetir|resultar|salvar|sentarse|significar|sonreír|suceder|suponer|cortar|temer|tirar|tratar|unir|visitar|votar|acercar|acompañar|actuar|aguantar|alzar|aprovechar|asegurar|atacar|avisar|besar|cantar|cobrar|colocar|comunicar|conservar|controlar|cocinar|descansar|dibujar""".split("|")))
if len(TRANSLATIONS) != len(VERBS):
    raise RuntimeError("El nombre de traduccions no coincideix amb el de verbs")

TAG_TO_TENSE = {
    "pri":"present", "pii":"imperfect", "ifi":"simplePast", "fti":"future",
    "cni":"conditional", "prs":"subjPresent", "pis":"subjImperfect", "imp":"imperative"
}
PERSON = {("p1","sg"):"1s",("p2","sg"):"2s",("p3","sg"):"3s",("p1","pl"):"1p",("p2","pl"):"2p",("p3","pl"):"3p"}

# Apertium's lexical entry for ``haver`` represents the existential construction
# ``haver-hi``.  Compound tenses need the personal auxiliary instead, so keep
# this small normative table separate from the lexical paradigm.
AUX_HAVER = {
    "present": {"1s":["he"], "2s":["has"], "3s":["ha"], "1p":["hem"], "2p":["heu"], "3p":["han"]},
    "imperfect": {"1s":["havia"], "2s":["havies"], "3s":["havia"], "1p":["havíem"], "2p":["havíeu"], "3p":["havien"]},
    "future": {"1s":["hauré"], "2s":["hauràs"], "3s":["haurà"], "1p":["haurem"], "2p":["haureu"], "3p":["hauran"]},
    "conditional": {"1s":["hauria"], "2s":["hauries"], "3s":["hauria"], "1p":["hauríem"], "2p":["hauríeu"], "3p":["haurien"]},
    "subjPresent": {"1s":["hagi"], "2s":["hagis"], "3s":["hagi"], "1p":["hàgim"], "2p":["hàgiu"], "3p":["hagin"]},
    "subjImperfect": {"1s":["hagués"], "2s":["haguessis"], "3s":["hagués"], "1p":["haguéssim"], "2p":["haguéssiu"], "3p":["haguessin"]},
}

# The periphrastic past uses auxiliary forms of ``anar``, not the lexical
# present *anem/aneu* in the first and second persons plural.
AUX_ANAR = {
    "1s":["vaig"], "2s":["vas"], "3s":["va"],
    "1p":["vam", "vàrem"], "2p":["vau", "vàreu"], "3p":["van", "varen"],
}

def text_of(el):
    out=[]
    def walk(node):
        if node.text: out.append(node.text)
        for child in node:
            if child.tag == "b": out.append(" ")
            elif child.tag not in {"s","j","a"}: walk(child)
            if child.tail: out.append(child.tail)
    walk(el)
    return "".join(out).strip()

def tags_of(r): return [x.attrib.get("n") for x in r.findall("s")]

def load():
    if not SOURCE.exists(): raise SystemExit("Falta work/apertium-cat. Consulteu README.md.")
    tree=ET.parse(SOURCE); root=tree.getroot()
    pardefs={p.attrib["n"]:p for p in root.findall(".//pardef")}
    entries={}
    for e in root.findall(".//section/e"):
        lm=e.attrib.get("lm")
        par=e.find("par")
        if lm in VERBS and par is not None and ("__vb" in par.attrib.get("n", "")):
            score=("__vblex" not in par.attrib["n"], "__vbmod" in par.attrib["n"])
            if lm not in entries or score < entries[lm][0]: entries[lm]=(score,e)
    missing=[v for v in VERBS if v not in entries]
    if missing: raise SystemExit("Verbs no trobats a Apertium: "+", ".join(missing))

    def expand(e):
        stem=text_of(e.find("i")) if e.find("i") is not None else (text_of(e.find("p/l")) if e.find("p/l") is not None else "")
        par=e.find("par").attrib["n"]; pd=pardefs[par]; forms={}; non={}
        for pe in pd.findall("e"):
            p=pe.find("p");
            if p is None: continue
            l,r=p.find("l"),p.find("r"); tags=tags_of(r)
            # Apertium marks the literary simple past as analysis-only (LR),
            # but those normative forms are valid output for this teaching app.
            if pe.attrib.get("r") == "LR" and "ifi" not in tags: continue
            surface=(stem+text_of(l)).replace("  "," ").strip()
            if not surface: continue
            key=next((x for x in TAG_TO_TENSE if x in tags),None)
            if key:
                person=next((PERSON[x] for x in PERSON if x[0] in tags and x[1] in tags),None)
                if person: forms.setdefault(TAG_TO_TENSE[key],{}).setdefault(person,[]).append(surface)
            elif "ger" in tags: non.setdefault("gerund",[]).append(surface)
            elif "pp" in tags and "f" not in tags and "pl" not in tags: non.setdefault("participle",[]).append(surface)
            elif "inf" in tags: non.setdefault("infinitive",[]).append(surface)
        for group in (forms,non):
            for k,val in group.items():
                if isinstance(val,dict):
                    for p,a in val.items(): val[p]=list(dict.fromkeys(a))
                else: group[k]=list(dict.fromkeys(val))
        return par,forms,non

    # Auxiliary tables are the same traceable simple paradigms.
    aux_map={"perfect":"present","pluperfect":"imperfect","futurePerfect":"future","conditionalPerfect":"conditional","subjPerfect":"subjPresent","subjPluperfect":"subjImperfect"}
    result=[]
    for rank,v in enumerate(VERBS,1):
        model,simple,non=expand(entries[v][1]); part=(non.get("participle") or [None])[0]
        infinitive=(non.get("infinitive") or [v])[0]
        if part:
            for compound,aux_tense in aux_map.items():
                simple[compound]={p:[f"{a} {part}" for a in av] for p,av in AUX_HAVER[aux_tense].items()}
            non["perfectInfinitive"]=[f"haver {part}"]
            if "gerund" in non: non["perfectGerund"]=[f"havent {part}"]
        simple["periphrasticPast"]={p:[f"{a} {infinitive}" for a in av] for p,av in AUX_ANAR.items()}
        # Conservative irregular label: paradigm name differs from productive endings or core irregular list.
        regular_markers=("/ar__vblex","/er__vblex","/re__vblex","/ir__vblex")
        irregular=v in {"ser","haver","estar","fer","poder","dir","anar","veure","donar","saber","voler","tenir","venir","dur","cabre","néixer","prendre","escriure","viure","treure","riure","caure"} or not any(x in model for x in regular_markers)
        group="1a conjugació (-ar)" if v.endswith("ar") else "3a conjugació (-ir)" if v.endswith("ir") else "2a conjugació (-er/-re)"
        conj=f"Traducció orientativa: {TRANSLATIONS[v]} · {group}"
        result.append({"id":unicodedata.normalize("NFD",v).encode("ascii","ignore").decode().replace(" ","-"),"infinitive":v,"translationEs":TRANSLATIONS[v],"rank":rank,"conjugation":conj,"model":model,"irregular":irregular,"forms":simple,"nonPersonal":non,"source":"Apertium Catalan 2.12.0"})
    return {"schemaVersion":1,"generatedFrom":"apertium/apertium-cat@2.12.0","license":"GPL-2.0-or-later","verbCount":len(result),"verbs":result}

def validate(data):
    errors=[]; ids=set(); infs=set(); persons=set(PERSON.values())
    for v in data["verbs"]:
        if v["id"] in ids: errors.append("ID duplicat: "+v["id"])
        if v["infinitive"] in infs: errors.append("Infinitiu duplicat: "+v["infinitive"])
        ids.add(v["id"]); infs.add(v["infinitive"])
        for tense,forms in v["forms"].items():
            expected=persons if tense!="imperative" else {"2s","3s","1p","2p","3p"}
            extra=set(forms)-expected
            if extra: errors.append(f"{v['infinitive']} {tense}: persones no vàlides {extra}")
            if any(not x.strip() for a in forms.values() for x in a): errors.append(f"{v['infinitive']} {tense}: forma buida")
        for tense in ("perfect","pluperfect","futurePerfect","conditionalPerfect","subjPerfect","subjPluperfect"):
            forms=v["forms"].get(tense)
            if forms:
                if set(forms) != persons: errors.append(f"{v['infinitive']} {tense}: falten persones")
                if any(" hi " in f" {form} " for variants in forms.values() for form in variants):
                    errors.append(f"{v['infinitive']} {tense}: auxiliar haver-hi incorrecte")
    if len(data["verbs"]) != len(VERBS): errors.append("Recompte incorrecte")
    return errors

if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); args=ap.parse_args()
    data=load(); errors=validate(data)
    if errors: raise SystemExit("\n".join(errors))
    encoded=json.dumps(data,ensure_ascii=False,separators=(",",":"))+"\n"
    if args.check:
        if not OUT.exists() or OUT.read_text()!=encoded: raise SystemExit("data/verbs.json no està actualitzat")
    else:
        OUT.parent.mkdir(exist_ok=True); OUT.write_text(encoded)
        forms=sum(len(a) for v in data["verbs"] for t in v["forms"].values() for a in t.values())+sum(len(a) for v in data["verbs"] for a in v["nonPersonal"].values())
        print(f"Generats {len(data['verbs'])} verbs i {forms} formes/variants.")
