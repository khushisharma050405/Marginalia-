import os, time, secrets, hashlib, hmac, json, io, re, datetime, jwt, psycopg
from typing import Any, Optional
from psycopg.rows import dict_row
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Header, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .seed import seed, CLASSES
from .solver import solve_text
from .curriculum_generator import generate_topic_questions, validate_question_topic
from .solve_pipeline import router as solve_router, _load_env
_load_env()

DB = os.getenv("DATABASE_URL", "postgresql://marginalia:marginalia@localhost:5432/marginalia")
if DB.startswith("postgres://"):
    DB = DB.replace("postgres://", "postgresql://", 1)
SECRET = os.getenv("JWT_SECRET", "dev-secret")

app = FastAPI(title="Marginalia API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    err_str = str(exc)
    if "Connection refused" in err_str or "could not connect to server" in err_str or "server closed the connection" in err_str:
        detail_msg = "Database connection failed. Please ensure DATABASE_URL is configured with a valid PostgreSQL instance on Render."
    else:
        detail_msg = f"Server error: {err_str}"
    return JSONResponse(
        status_code=500,
        content={"detail": detail_msg},
        headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Methods": "*"}
    )

def db() -> Any:
    return psycopg.connect(DB, row_factory=dict_row, autocommit=True)  # type: ignore

def init_db(c):
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY,email TEXT UNIQUE NOT NULL,name TEXT NOT NULL,pw TEXT NOT NULL,board TEXT,class_level TEXT,stream TEXT,created TIMESTAMPTZ DEFAULT now());
        CREATE TABLE IF NOT EXISTS reset_tokens(token TEXT PRIMARY KEY,user_id INT REFERENCES users(id),expires TIMESTAMPTZ);
        CREATE TABLE IF NOT EXISTS subjects(id SERIAL PRIMARY KEY,board TEXT,class_level TEXT,stream TEXT,name TEXT);
        CREATE TABLE IF NOT EXISTS chapters(id SERIAL PRIMARY KEY,subject_id INT REFERENCES subjects(id),name TEXT,ord INT);
        CREATE TABLE IF NOT EXISTS topics(id SERIAL PRIMARY KEY,chapter_id INT REFERENCES chapters(id),name TEXT);
        CREATE TABLE IF NOT EXISTS questions(id SERIAL PRIMARY KEY,topic_id INT REFERENCES topics(id),prompt TEXT,options JSONB,answer INT,explanation TEXT,difficulty TEXT,is_sample BOOL DEFAULT true);
        CREATE TABLE IF NOT EXISTS attempts(id SERIAL PRIMARY KEY,user_id INT REFERENCES users(id),question_id INT REFERENCES questions(id),correct BOOL,seconds INT DEFAULT 0,created TIMESTAMPTZ DEFAULT now());
        CREATE TABLE IF NOT EXISTS solves(id SERIAL PRIMARY KEY,user_id INT REFERENCES users(id),question TEXT,subject TEXT,topic TEXT,qtype TEXT,difficulty TEXT,confidence INT,steps JSONB,created TIMESTAMPTZ DEFAULT now());
        CREATE TABLE IF NOT EXISTS notes(id SERIAL PRIMARY KEY,user_id INT REFERENCES users(id),kind TEXT,title TEXT,body TEXT,created TIMESTAMPTZ DEFAULT now());
        CREATE TABLE IF NOT EXISTS solver_cache(cache_key TEXT PRIMARY KEY,response_json JSONB NOT NULL,created_at TIMESTAMPTZ DEFAULT now());
    """)
    try:
        c.execute("""
            DO $$
            BEGIN
                CREATE EXTENSION IF NOT EXISTS vector;
                CREATE TABLE IF NOT EXISTS rag_chunks (
                    id SERIAL PRIMARY KEY,
                    board VARCHAR(32) NOT NULL,
                    class_level VARCHAR(32) NOT NULL,
                    subject VARCHAR(128) NOT NULL,
                    chapter VARCHAR(256) NOT NULL,
                    chunk_index INT NOT NULL DEFAULT 0,
                    content TEXT NOT NULL,
                    embedding vector(768),
                    created_at TIMESTAMPTZ DEFAULT now()
                );
                CREATE INDEX IF NOT EXISTS rag_chunks_meta_idx ON rag_chunks(board, class_level, subject, chapter);
            EXCEPTION WHEN OTHERS THEN
                NULL;
            END $$;
        """)
    except Exception:
        pass

def Q(sql: Any, a: Any = (), one: bool = False) -> Any:
    with db() as c:
        r = c.execute(sql, a)
        if r.description is None:
            return None
        return r.fetchone() if one else r.fetchall()

@app.on_event("startup")
def _s():
    for attempt in range(10):
        try:
            with db() as c:
                init_db(c)
                seed(c)
            print("Database initialized and verified successfully.", flush=True)
            break
        except Exception as e:
            print(f"Database connection attempt {attempt+1}/10 failed: {e}. Retrying in 2s...", flush=True)
            time.sleep(2)

@app.get("/")
@app.get("/health")
def health():
    return {"status": "ok", "app": "Marginalia API", "version": "1.0.0"}

def hp(p,salt=None):
    salt=salt or secrets.token_hex(8); return salt+"$"+hashlib.pbkdf2_hmac("sha256",p.encode(),salt.encode(),120000).hex()
def chk(p,h): return hmac.compare_digest(hp(p,h.split("$")[0]),h)
def tok(uid): return jwt.encode({"sub":str(uid),"exp":int(time.time())+60*60*24*30},SECRET,"HS256")
def me(authorization:str=Header(None)):
    try: uid=int(jwt.decode((authorization or "").replace("Bearer ",""),SECRET,["HS256"])["sub"])
    except Exception: raise HTTPException(401,"Not signed in")
    u=Q("select id,email,name,board,class_level,stream from users where id=%s",(uid,),True)
    if not u: raise HTTPException(401,"Not signed in")
    return u
class Reg(BaseModel): email:str; name:str; password:str
class Login(BaseModel): email:str; password:str
class Prof(BaseModel): board:str; class_level:str; stream:str|None=None
class Att(BaseModel): question_id:int; choice:int; seconds:int=0
class Note(BaseModel): kind:str="note"; title:str; body:str=""
class Rst(BaseModel): token:str; password:str
@app.post("/auth/register")
def reg(b:Reg):
    if not re.match(r"[^@]+@[^@]+\.[^@]+",b.email) or len(b.password)<8: raise HTTPException(422,"Valid email and 8+ character password required")
    if Q("select 1 from users where email=%s",(b.email.lower(),),True): raise HTTPException(409,"Email already registered")
    u=Q("insert into users(email,name,pw) values(%s,%s,%s) returning id",(b.email.lower(),b.name,hp(b.password)),True); return {"token":tok(u["id"])}
@app.post("/auth/login")
def login(b:Login):
    u=Q("select id,pw from users where email=%s",(b.email.lower(),),True)
    if not u or not chk(b.password,u["pw"]): raise HTTPException(401,"Wrong email or password")
    return {"token":tok(u["id"])}
@app.post("/auth/forgot")
def forgot(b:dict):
    u=Q("select id from users where email=%s",(str(b.get("email","")).lower(),),True)
    if u:
        t=secrets.token_urlsafe(24); Q("insert into reset_tokens values(%s,%s,now()+interval '1 hour')",(t,u["id"])); print("PASSWORD RESET TOKEN:",t,flush=True)
    return {"ok":True,"note":"If the account exists, a reset token was written to the server log."}
@app.post("/auth/reset")
def reset(b:Rst):
    r=Q("select user_id from reset_tokens where token=%s and expires>now()",(b.token,),True)
    if not r or len(b.password)<8: raise HTTPException(400,"Invalid token or weak password")
    Q("update users set pw=%s where id=%s",(hp(b.password),r["user_id"])); Q("delete from reset_tokens where token=%s",(b.token,)); return {"ok":True}
@app.get("/me")
def getme(u=Depends(me)): return u
@app.put("/me/profile")
def setprof(p:Prof,u=Depends(me)):
    if p.board not in("CBSE","ICSE") or p.class_level not in CLASSES: raise HTTPException(422,"Invalid board/class")
    hi=p.class_level in("11","12")
    if hi and p.stream not in("Science","Commerce","Humanities"): raise HTTPException(422,"Stream required for 11–12")
    Q("update users set board=%s,class_level=%s,stream=%s where id=%s",(p.board,p.class_level,p.stream if hi else None,u["id"])); return {"ok":True}
def scope(u):
    if not u["board"]: raise HTTPException(409,"Complete setup first")
    return (u["board"],u["class_level"],u["stream"])
@app.get("/subjects")
def subjects(u=Depends(me)): return Q("select id,name from subjects where board=%s and class_level=%s and stream is not distinct from %s order by id",scope(u))
@app.get("/subjects/{sid}")
def subject(sid:int,u=Depends(me)):
    ch=Q("select id,name from chapters where subject_id=%s order by ord",(sid,))
    for c in ch: c["topics"]=Q("select id,name from topics where chapter_id=%s order by id",(c["id"],))
    return {"chapters":ch}
@app.get("/practice")
def practice(topic_id:int|None=None,chapter_id:int|None=None,subject_id:int|None=None,difficulty:str|None=None,mode:str="mixed",u=Depends(me)):
    diff_filter = difficulty.capitalize() if difficulty and difficulty.capitalize() in ("Easy", "Medium", "Hard") else None

    if topic_id:
        t_info = Q("select t.id, t.name as topic_name, c.name as chapter_name, s.name as subject_name, s.class_level from topics t join chapters c on c.id=t.chapter_id join subjects s on s.id=c.subject_id where t.id=%s", (topic_id,), True)
        if not t_info:
            raise HTTPException(404, "Topic not found")
        
        w_diff = " and q.difficulty=%s" if diff_filter else ""
        args = [topic_id, diff_filter] if diff_filter else [topic_id]
        existing = Q("select q.id, q.prompt, q.options, q.difficulty, t.name as topic from questions q join topics t on t.id=q.topic_id where q.topic_id=%s" + w_diff, args)
        
        # Validate existing questions for curriculum accuracy
        valid_existing = []
        invalid_ids = []
        for q in existing:
            if validate_question_topic(q["prompt"], t_info["topic_name"], t_info["chapter_name"], t_info["subject_name"], t_info["class_level"]):
                valid_existing.append(q)
            else:
                invalid_ids.append(q["id"])
                
        if invalid_ids:
            for qid in invalid_ids:
                Q("delete from attempts where question_id=%s", (qid,))
                Q("delete from questions where id=%s", (qid,))

        # Check if existing questions include True/False and Fill-in-the-blank variety
        has_variety = any(len(q["options"]) == 2 for q in valid_existing) and any("_____" in q["prompt"] for q in valid_existing)
        if not has_variety or len(valid_existing) < 10:
            for q in valid_existing:
                Q("delete from attempts where question_id=%s", (q["id"],))
                Q("delete from questions where id=%s", (q["id"],))
            valid_existing = []

            gen = generate_topic_questions(
                topic_id=t_info["id"],
                topic_name=t_info["topic_name"],
                chapter_name=t_info["chapter_name"],
                subject_name=t_info["subject_name"],
                class_level=t_info["class_level"],
                difficulty=diff_filter or "Medium",
                count=10
            )
            for p, o, a, exp, q_diff in gen:
                Q("insert into questions(topic_id, prompt, options, answer, explanation, difficulty, is_sample) values(%s, %s, %s, %s, %s, %s, false)",
                  (t_info["id"], p, json.dumps(o), a, exp, q_diff))
            
            valid_existing = Q("select q.id, q.prompt, q.options, q.difficulty, t.name as topic from questions q join topics t on t.id=q.topic_id where q.topic_id=%s" + w_diff + " order by id desc limit 10", args)
            
        return valid_existing[:10]

    base = "select q.id,q.prompt,q.options,q.difficulty,t.name topic, c.name as chapter_name, s.name as subject_name, s.class_level from questions q join topics t on t.id=q.topic_id join chapters c on c.id=t.chapter_id join subjects s on s.id=c.subject_id where s.board=%s and s.class_level=%s and s.stream is not distinct from %s"
    a = list(scope(u)); w = ""
    if chapter_id:
        w += " and c.id=%s"; a.append(chapter_id)
    elif subject_id:
        w += " and s.id=%s"; a.append(subject_id)
    elif mode == "weak":
        w += " and t.id in (select q2.topic_id from attempts a2 join questions q2 on q2.id=a2.question_id where a2.user_id=%s group by q2.topic_id having avg(a2.correct::int)<0.7)"; a.append(u["id"])
    elif mode == "revision":
        w += " and q.id in (select question_id from attempts where user_id=%s and not correct)"; a.append(u["id"])

    if diff_filter:
        w += " and q.difficulty=%s"; a.append(diff_filter)

    qs = Q(base + w + " order by random() limit 20", a)
    valid_qs = []
    for q in qs:
        if validate_question_topic(q["prompt"], q["topic"], q.get("chapter_name", ""), q.get("subject_name", ""), q.get("class_level", "")):
            valid_qs.append({"id": q["id"], "prompt": q["prompt"], "options": q["options"], "difficulty": q["difficulty"], "topic": q["topic"]})
        else:
            Q("delete from attempts where question_id=%s", (q["id"],))
            Q("delete from questions where id=%s", (q["id"],))
        if len(valid_qs) == 10:
            break

    # If fewer than 10 valid questions in mixed/chapter mode, dynamically generate authentic questions in scope
    if len(valid_qs) < 10:
        scope_topics_sql = "select t.id, t.name as topic_name, c.name as chapter_name, s.name as subject_name, s.class_level from topics t join chapters c on c.id=t.chapter_id join subjects s on s.id=c.subject_id where s.board=%s and s.class_level=%s and s.stream is not distinct from %s"
        t_a = list(scope(u)); t_w = ""
        if chapter_id:
            t_w += " and c.id=%s"; t_a.append(chapter_id)
        elif subject_id:
            t_w += " and s.id=%s"; t_a.append(subject_id)
        target_topics = Q(scope_topics_sql + t_w + " order by random() limit 10", t_a)
        
        for t_info in target_topics:
            if len(valid_qs) >= 10:
                break
            gen = generate_topic_questions(
                topic_id=t_info["id"],
                topic_name=t_info["topic_name"],
                chapter_name=t_info["chapter_name"],
                subject_name=t_info["subject_name"],
                class_level=t_info["class_level"],
                difficulty=diff_filter or "Medium",
                count=2
            )
            for p, o, ans_i, exp, q_diff in gen:
                if validate_question_topic(p, t_info["topic_name"], t_info["chapter_name"], t_info["subject_name"], t_info["class_level"]):
                    new_q = Q("insert into questions(topic_id, prompt, options, answer, explanation, difficulty, is_sample) values(%s, %s, %s, %s, %s, %s, false) returning id",
                      (t_info["id"], p, json.dumps(o), ans_i, exp, q_diff), True)
                    valid_qs.append({"id": new_q["id"], "prompt": p, "options": o, "difficulty": q_diff, "topic": t_info["topic_name"]})
                    if len(valid_qs) >= 10:
                        break

    return valid_qs[:10]
@app.post("/practice/attempt")
def attempt(b:Att,u=Depends(me)):
    q=Q("select answer,explanation from questions where id=%s",(b.question_id,),True)
    if not q: raise HTTPException(404,"No such question")
    ok=q["answer"]==b.choice; Q("insert into attempts(user_id,question_id,correct,seconds) values(%s,%s,%s,%s)",(u["id"],b.question_id,ok,b.seconds)); return {"correct":ok,"answer":q["answer"],"explanation":q["explanation"]}
def stats(uid):
    s=Q("select count(*) n,coalesce(sum(correct::int),0) c,coalesce(sum(seconds),0) secs from attempts where user_id=%s",(uid,),True)
    days=[r["d"] for r in Q("select distinct d from (select created::date d from attempts where user_id=%s union all select created::date from solves where user_id=%s) x order by d desc",(uid,uid))]
    streak=0; d=datetime.date.today()
    if days and days[0]==d-datetime.timedelta(days=1): d-=datetime.timedelta(days=1)
    for x in days:
        if x==d: streak+=1; d-=datetime.timedelta(days=1)
        else: break
    weak=Q("select t.name,round(100*avg(a.correct::int)) acc from attempts a join questions q on q.id=a.question_id join topics t on t.id=q.topic_id where a.user_id=%s group by t.name having avg(a.correct::int)<0.7 order by acc limit 5",(uid,))
    for w in weak: w["acc"]=int(w["acc"])
    return {"attempted":s["n"],"correct":int(s["c"]),"accuracy":round(100*s["c"]/s["n"]) if s["n"] else 0,"study_minutes":round(s["secs"]/60),"streak":streak,"weak":weak,"solved":Q("select count(*) n from solves where user_id=%s",(uid,),True)["n"]}
@app.get("/growth")
def growth(u=Depends(me)): return stats(u["id"])
@app.get("/dashboard")
def dash(u=Depends(me)):
    s=stats(u["id"]); today=Q("select count(*) n from attempts where user_id=%s and created::date=current_date",(u["id"],),True)["n"]
    return {
        **s,
        "user": u,
        "goal": {"target": 10, "done": today},
        "recent": Q("select id,question,subject,topic,to_char(created,'Mon DD, HH12:MI AM') as created_at from solves where user_id=%s order by created desc limit 6",(u["id"],)),
        "recommend": Q("select c.id,c.name,s.name as subject_name from chapters c join subjects s on s.id=c.subject_id where s.board=%s and s.class_level=%s and s.stream is not distinct from %s order by random() limit 3",scope(u))
    }
app.include_router(solve_router)

@app.post("/extract-file")
async def extract_file(file: UploadFile = File(...)):
    """Extracts problem text from uploaded PDF or Image."""
    try:
        content = await file.read()
        filename = (file.filename or "").lower()
        extracted_text = ""

        # 1. High-speed local PDF text extraction via pypdf
        if filename.endswith(".pdf") or file.content_type == "application/pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(content))
                pages = []
                for p in reader.pages:
                    txt = p.extract_text()
                    if txt and txt.strip():
                        pages.append(txt.strip())
                extracted_text = "\n\n".join(pages).strip()
            except Exception:
                pass

        # 2. Image / fallback multimodal extraction
        if not extracted_text:
            gemini_key = os.getenv("GEMINI_API_KEY")
            if gemini_key:
                import base64, httpx
                mime = file.content_type or ("application/pdf" if filename.endswith(".pdf") else "image/jpeg")
                b64 = base64.b64encode(content).decode("utf-8")
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
                headers = {"x-goog-api-key": gemini_key, "Content-Type": "application/json"}
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Extract all questions, math equations, problem statements, and numerical values from this image or document. Return ONLY the clean extracted question text without any markdown commentary."},
                            {"inline_data": {"mime_type": mime, "data": b64}}
                        ]
                    }]
                }
                try:
                    async with httpx.AsyncClient(timeout=25) as client:
                        res = await client.post(url, headers=headers, json=payload)
                        if res.status_code == 200:
                            data = res.json()
                            extracted_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                except Exception:
                    pass

        return {
            "ok": True,
            "filename": file.filename,
            "extracted": extracted_text,
            "has_text": bool(extracted_text.strip())
        }
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")

@app.get("/notes")
def notes(u=Depends(me)): return Q("select id,kind,title,body from notes where user_id=%s order by created desc",(u["id"],))
@app.post("/notes")
def addnote(n:Note,u=Depends(me)): return Q("insert into notes(user_id,kind,title,body) values(%s,%s,%s,%s) returning id",(u["id"],n.kind,n.title,n.body),True)
@app.delete("/notes/{i}")
def delnote(i:int,u=Depends(me)): Q("delete from notes where id=%s and user_id=%s",(i,u["id"])); return {"ok":True}
@app.get("/history")
def hist(u=Depends(me)):
    return Q("select id,question,subject,topic,qtype,difficulty,confidence,to_char(created,'Mon DD, YYYY · HH12:MI AM') as created_at from solves where user_id=%s order by created desc limit 50",(u["id"],))
