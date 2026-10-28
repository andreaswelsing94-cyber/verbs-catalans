export const STORAGE_KEY='verbs-catalans-progress';
export const VERSION=3;
export const DEFAULTS={version:VERSION,settings:{questionCount:10,persons:['3p'],frequency:100,regular:true,irregular:true,favoritesOnly:false,errorsOnly:false,repeatErrors:true,tenses:['present','imperfect','periphrasticPast','simplePast','perfect','pluperfect','future','futurePerfect','conditional','conditionalPerfect','subjPresent','subjImperfect','subjPerfect','subjPluperfect','imperative']},favorites:[],history:[],stats:{correct:0,incorrect:0,byVerb:{},byTense:{}},pendingErrors:{},pronouns:{completed:0,correct:0,incorrect:0,byLevel:{},errors:{},review:{}}};
const clone=x=>JSON.parse(JSON.stringify(x));
export function migrate(raw){if(!raw||typeof raw!=='object')return clone(DEFAULTS);let x=clone(raw);if(!x.version)x={...clone(DEFAULTS),...x,version:1};if(x.version===1){x.pendingErrors=x.pendingErrors||{};x.version=2}if(x.version===2){x.pronouns=clone(DEFAULTS.pronouns);x.version=3}return {...clone(DEFAULTS),...x,settings:{...DEFAULTS.settings,...x.settings},stats:{...DEFAULTS.stats,...x.stats},pronouns:{...clone(DEFAULTS.pronouns),...x.pronouns},version:VERSION}}
export function load(store=localStorage){try{return migrate(JSON.parse(store.getItem(STORAGE_KEY)))}catch{return clone(DEFAULTS)}}
export function save(state,store=localStorage){store.setItem(STORAGE_KEY,JSON.stringify({...state,version:VERSION}))}
export function clear(store=localStorage){store.removeItem(STORAGE_KEY)}
