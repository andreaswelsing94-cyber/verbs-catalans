export const PRONOUN_LEVELS=[
 {id:1,title:'EL, LA, ELS, LES',short:'Complement directe definit',rule:'Els pronoms el, la, els i les substitueixen un complement directe definit i concorden en gènere i nombre.',examples:['Compro el llibre → El compro.','Veig la Maria → La veig.','Tinc les claus → Les tinc.']},
 {id:2,title:'HO',short:'Idees i complements neutres',rule:'Ho substitueix una idea, una proposició o un complement neutre. No equival al masculí el.',examples:['No sé què passa → No ho sé.','Entens això? → Ho entens?','Saps que vindrà? → Ho saps?']},
 {id:3,title:'HI',short:'Llocs i complements preposicionals',rule:'Hi substitueix sovint un lloc o un complement introduït per a, en o amb. No substitueix indiscriminadament persones.',examples:['Vaig al mercat → Hi vaig.','Penso en això → Hi penso.','Treballo a Gràcia → Hi treballo.']},
 {id:4,title:'EN',short:'Quantitats i complements amb de',rule:'En substitueix noms indefinits, quantitats o complements introduïts per de. La quantitat es conserva.',examples:['Tens pa? → En tinc.','Vull tres pomes → En vull tres.','Parlo del problema → En parlo.']},
 {id:5,title:'Posició i apostrofació',short:'Abans i després del verb',rule:'Davant del verb el pronom pot apostrofar-se; darrere d’un infinitiu o imperatiu s’uneix amb apòstrof o guionet.',examples:["L’he comprat.","Compra’l.",'Vull comprar-ne.']},
 {id:6,title:'Combinacions',short:'Dos pronoms febles',rule:'Els pronoms segueixen un ordre fix i sovint s’apostrofen. En català central, li + el/la/els/les sol realitzar-se com l’hi, la hi, els hi, les hi.',examples:["T’ho dic.","Me’n recordo.","N’hi ha tres."]},
 {id:7,title:'Pràctica mixta',short:'Situacions quotidianes',rule:'Cal identificar la funció del complement, triar el pronom i col·locar-lo correctament sense cap pista.',examples:['No ho sé.','Hi vaig demà.','En voldria dos.']}
];

// Vuit situacions revisades per nivell. Cada situació genera cinc activitats
// pedagògiques (selecció, substitució, diàleg, traducció i construcció): 280 en total.
const S={
 1:[['Compro el llibre.','El compro.','el','Compro el libro.'],['Veig la Maria.','La veig.','la','Veo a María.'],['Tinc els documents.','Els tinc.','els','Tengo los documentos.'],['Rento les pomes.','Les rento.','les','Lavo las manzanas.'],['Porto el bitllet.','El porto.','el','Llevo el billete.'],['Veig la Júlia.','La veig.','la','Veo a Júlia.'],['Necessito els diners.','Els necessito.','els','Necesito el dinero.'],['Busco les claus.','Les busco.','les','Busco las llaves.']],
 2:[["No sé què passa.",'No ho sé.','ho','No lo sé.'],['Entens això?','Ho entens?','ho','¿Lo entiendes?'],['Sé que vindrà.','Ho sé.','ho','Sé que vendrá.'],['Puc fer això.','Ho puc fer.','ho','Lo puedo hacer.'],['Crec que tens raó.','Ho crec.','ho','Lo creo.'],['Recordo el que vas dir.','Ho recordo.','ho','Lo recuerdo.'],['Explico tot això.','Ho explico.','ho','Lo explico.'],['Veurem què passa.','Ho veurem.','ho','Lo veremos.']],
 3:[['Vaig al mercat.','Hi vaig.','hi','Voy allí.'],['Treballo a Barcelona.','Hi treballo.','hi','Trabajo allí.'],['Penso en el problema.','Hi penso.','hi','Pienso en ello.'],['Confio en el projecte.','Hi confio.','hi','Confío en ello.'],['Visc a Gràcia.','Hi visc.','hi','Vivo allí.'],['Participo en el curs.','Hi participo.','hi','Participo en ello.'],['Assisteixo a la reunió.','Hi assisteixo.','hi','Asisto.'],['Compto amb la teva ajuda.','Hi compto.','hi','Cuento con ella.']],
 4:[['Tinc pa.','En tinc.','en','Tengo.'],['Vull tres pomes.','En vull tres.','en','Quiero tres.'],['Parlo del problema.','En parlo.','en','Hablo de ello.'],['Vinc de Girona.','En vinc.','en','Vengo de allí.'],['Compro cinc llibres.','En compro cinc.','en','Compro cinco.'],['Necessito aigua.','En necessito.','en','Necesito.'],['Recordo una part del viatge.','En recordo una part.','en','Recuerdo una parte.'],['Surto de casa.','En surto.','en','Salgo de allí.']],
 5:[["He comprat el llibre.","L’he comprat.","l’",'Lo he comprado.'],['Compra el llibre.',"Compra’l.","’l",'Cómpralo.'],['Vull comprar el llibre.','Vull comprar-lo.','lo','Quiero comprarlo.'],['Vull comprar pa.','Vull comprar-ne.','ne','Quiero comprar.'],["He vist la pel·lícula.","L’he vista.","l’",'La he visto.'],['Porta el document.',"Porta’l.","’l",'Tráelo.'],['Podem visitar el museu.','Podem visitar-lo.','lo','Podemos visitarlo.'],['He comprat pomes.',"N’he comprat.","n’",'He comprado.']],
 6:[["Dic això a tu.","T’ho dic.","t’ho",'Te lo digo.'],['Dono el llibre a tu.','Te’l dono.',"te’l",'Te lo doy.'],['Em recordo del nom.',"Me’n recordo.","me’n",'Me acuerdo de ello.'],['Hi ha tres cadires.',"N’hi ha tres.","n’hi",'Hay tres.'],['Explico això a ella.',"Li ho explico.",'li ho','Se lo explico.'],['Dono el paquet a ell.',"L’hi dono.","l’hi",'Se lo doy.'],['Et recordes del carrer?',"Te’n recordes?","te’n",'¿Te acuerdas?'],['Hi ha molt cafè.',"N’hi ha molt.","n’hi",'Hay mucho.']],
 7:[['Compro les entrades.','Les compro.','les','Las compro.'],["No sé què vol.",'No ho sé.','ho','No lo sé.'],['Vaig a la feina.','Hi vaig.','hi','Voy allí.'],['Vull dos cafès.','En vull dos.','en','Quiero dos.'],['Porto el mòbil a casa.','El porto a casa.','el','Lo llevo a casa.'],['Entenc el que dius.','Ho entenc.','ho','Lo entiendo.'],['Anem al Born amb metro.','Hi anem amb metro.','hi','Vamos allí en metro.'],['Demano dues aigües.','En demano dues.','en','Pido dos.']]
};
const OPTIONS=['el','la','els','les','ho','hi','en',"l’","’l",'lo','ne',"t’ho","te’l","me’n","n’hi"];
const explanation={1:'El pronombre concuerda con el complemento directo definido.',2:'Ho sustituye una idea o un complemento neutro; no es el artículo masculino el.',3:'Hi sustituye aquí un lugar o un complemento preposicional.',4:'En sustituye un nombre indefinido o un complemento con de; la cantidad se conserva.',5:'La forma cambia según la posición y el sonido siguiente: apóstrofo o guion.',6:'Los pronombres siguen un orden fijo y se apostrofan cuando corresponde.',7:'Primero identifica la función del complemento; después elige y coloca el pronombre.'};
const types=['select','substitute','dialogue','translate','build'];
export const PRONOUN_EXERCISES=[];
for(const [level,items] of Object.entries(S))for(const [i,x] of items.entries())for(const [j,type] of types.entries()){
 let question;
 if(type==='select')question=`Tria el pronom per completar: ${x[1].replace(new RegExp(`^${x[2]}`,'i'),'___')}`;
 else if(type==='substitute')question=`Substitueix el complement: ${x[0]}`;
 else if(type==='dialogue')question=`Respon amb un pronom: ${x[0]}`;
 else if(type==='translate')question='Tradueix al català.';
 else question=`Ordena: ${x[1].replace(/[.!?]/g,'').split(' ').reverse().join(' / ')}`;
 PRONOUN_EXERCISES.push({id:`p${level}-${i+1}-${type}`,level:+level,exerciseType:type,difficulty:j<2?1:j<4?2:3,context:type==='translate'?x[3]:x[0],question,options:type==='select'?[x[2],...OPTIONS.filter(o=>o!==x[2]).slice((i+j)%8,(i+j)%8+3)]:[],correctAnswers:type==='dialogue'?[x[1],x[2]]:[x[1]],shortAnswer:x[2],explanation:explanation[level],grammarRule:PRONOUN_LEVELS[level-1].rule,tags:[PRONOUN_LEVELS[level-1].short]});
}

export function normalizePronounAnswer(s){return String(s??'').trim().replace(/[.!?¡¿]+$/g,'').replace(/['´]/g,'’').replace(/\s+/g,' ').toLocaleLowerCase('ca')}
export function pronounCorrect(input,q){const answers=q.exerciseType==='select'?[q.shortAnswer]:q.correctAnswers,n=normalizePronounAnswer(input);return answers.some(a=>normalizePronounAnswer(a)===n)}
export function pronounPool(level='all'){return PRONOUN_EXERCISES.filter(x=>level==='all'||level==='mixed'||x.level===+level)}
export function duePronouns(state,now=Date.now()){return PRONOUN_EXERCISES.filter(x=>state.pronouns.review[x.id]&&(state.pronouns.review[x.id].due||0)<=now)}
export function recordPronoun(state,q,correct,now=Date.now()){
 const p=state.pronouns,r=p.review[q.id]||{streak:0};p.completed++;(p.byLevel[q.level]??={correct:0,incorrect:0})[correct?'correct':'incorrect']++;p[correct?'correct':'incorrect']++;
 if(correct){r.streak++;r.due=now+[1,3,7,14,30][Math.min(r.streak-1,4)]*86400000;delete p.errors[q.id]}else{r.streak=0;r.due=now+86400000;p.errors[q.id]=(p.errors[q.id]||0)+1}
 r.last=now;p.review[q.id]=r;return r;
}
