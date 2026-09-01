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
VERBS = """ser haver estar fer poder dir anar veure donar saber voler arribar passar comprendre posar semblar quedar creure parlar portar deixar trobar tornar prendre conèixer viure sentir mirar esperar sortir treballar escriure perdre entendre començar entrar tenir buscar morir recordar acabar convertir mantenir aconseguir explicar preguntar tocar continuar canviar presentar crear obrir considerar permetre comprar servir seguir llegir caure córrer aparèixer rebre viatjar ajudar jugar estudiar menjar beure dormir aprendre vendre pagar enviar caminar escoltar estimar guanyar utilitzar decidir intentar necessitar existir pujar baixar néixer dur cabre venir treure riure respondre tancar patir descobrir triar oblidar preparar compartir conduir acceptar""".split()

TRANSLATIONS = dict(zip(VERBS, """ser|haber|estar|hacer|poder|decir|ir|ver|dar|saber|querer|llegar|pasar|comprender|poner|parecer|quedar|creer|hablar|llevar|dejar|encontrar|volver|tomar|conocer|vivir|sentir|mirar|esperar|salir|trabajar|escribir|perder|entender|empezar|entrar|tener|buscar|morir|recordar|acabar|convertir|mantener|conseguir|explicar|preguntar|tocar|continuar|cambiar|presentar|crear|abrir|considerar|permitir|comprar|servir|seguir|leer|caer|correr|aparecer|recibir|viajar|ayudar|jugar|estudiar|comer|beber|dormir|aprender|vender|pagar|enviar|caminar|escuchar|amar o querer|ganar|utilizar|decidir|intentar|necesitar|existir|subir|bajar|nacer|llevar|caber|venir|sacar|reír|responder|cerrar|sufrir|descubrir|elegir|olvidar|preparar|compartir|conducir|aceptar""".split("|")))
if len(TRANSLATIONS) != len(VERBS):
    raise RuntimeError("El nombre de traduccions no coincideix amb el de verbs")

TAG_TO_TENSE = {
    "pri":"present", "pii":"imperfect", "ifi":"simplePast", "fti":"future",
    "cni":"conditional", "prs":"subjPresent", "pis":"subjImperfect", "imp":"imperative"
}
PERSON = {("p1","sg"):"1s",("p2","sg"):"2s",("p3","sg"):"3s",("p1","pl"):"1p",("p2","pl"):"2p",("p3","pl"):"3p"}

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
            if pe.attrib.get("r") == "LR": continue
            p=pe.find("p");
            if p is None: continue
            l,r=p.find("l"),p.find("r"); tags=tags_of(r); surface=(stem+text_of(l)).replace("  "," ").strip()
            if not surface: continue
            key=next((x for x in TAG_TO_TENSE if x in tags),None)
            if key:
                person=next((PERSON[x] for x in PERSON if x[0] in tags and x[1] in tags),None)
                if person: forms.setdefault(TAG_TO_TENSE[key],{}).setdefault(person,[]).append(surface)
            elif "ger" in tags: non.setdefault("gerund",[]).append(surface)
            elif "pp" in tags and ("m" in tags or not any(x in tags for x in ("f","pl"))): non.setdefault("participle",[]).append(surface)
            elif "inf" in tags: non.setdefault("infinitive",[]).append(surface)
        for group in (forms,non):
            for k,val in group.items():
                if isinstance(val,dict):
                    for p,a in val.items(): val[p]=list(dict.fromkeys(a))
                else: group[k]=list(dict.fromkeys(val))
        return par,forms,non

    # Auxiliary tables are the same traceable simple paradigms.
    _, haver_forms, _ = expand(entries["haver"][1])
    _, anar_forms, _ = expand(entries["anar"][1])
    aux_map={"perfect":"present","pluperfect":"imperfect","futurePerfect":"future","conditionalPerfect":"conditional","subjPerfect":"subjPresent","subjPluperfect":"subjImperfect"}
    result=[]
    for rank,v in enumerate(VERBS,1):
        model,simple,non=expand(entries[v][1]); part=(non.get("participle") or [None])[0]
        infinitive=(non.get("infinitive") or [v])[0]
        if part:
            for compound,aux_tense in aux_map.items():
                if aux_tense in haver_forms:
                    simple[compound]={p:[f"{a} {part}" for a in av] for p,av in haver_forms[aux_tense].items()}
            if "present" in haver_forms: non["perfectInfinitive"]=[f"haver {part}"]
            if "gerund" in non: non["perfectGerund"]=[f"havent {part}"]
        if "present" in anar_forms:
            simple["periphrasticPast"]={p:[f"{a} {infinitive}" for a in av] for p,av in anar_forms["present"].items()}
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
