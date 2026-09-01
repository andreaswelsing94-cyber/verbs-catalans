import test from'node:test';import assert from'node:assert/strict';import{migrate,load,save,VERSION,STORAGE_KEY}from'../js/storage.js';
test('crea estat per defecte amb 3a plural',()=>assert.deepEqual(migrate(null).settings.persons,['3p']));
test('migra dades v1 i conserva favorits',()=>{const x=migrate({version:1,favorites:['ser'],settings:{questionCount:20}});assert.equal(x.version,VERSION);assert.deepEqual(x.favorites,['ser']);assert.deepEqual(x.pendingErrors,{})});
test('persistència serialitzada',()=>{const m=new Map(),store={getItem:k=>m.get(k)||null,setItem:(k,v)=>m.set(k,v)};const x=migrate(null);x.favorites=['anar'];save(x,store);assert.deepEqual(load(store).favorites,['anar']);assert.ok(m.has(STORAGE_KEY))});
