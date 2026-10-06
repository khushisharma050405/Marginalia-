"use client";
import {Shell,useApi} from "@/lib/api";
export default function G(){const{d}=useApi("/growth");
  return<Shell title="Growth" sub="Your progress at a glance.">{d&&<div className="grid md:grid-cols-3 gap-4">{[["Accuracy",d.accuracy+"%"],["Practice attempted",d.attempted],["Correct",d.correct],["Questions solved",d.solved],["Study time",d.study_minutes+" min"],["Streak",d.streak+" days"]].map(([a,b])=><div key={a} className="card"><div className="text-ink/50 text-sm">{a}</div><div className="font-serif text-3xl">{b}</div></div>)}
  <div className="card md:col-span-3"><h3 className="font-serif text-lg">Needs revision</h3>{d.weak.length?d.weak.map((w:any)=><p key={w.name}>{w.name} — {w.acc}% accuracy</p>):<p className="text-ink/60">No weak topics yet.</p>}</div></div>}</Shell>}
