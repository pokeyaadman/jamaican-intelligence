"use strict";

/* Jamaican Intelligence v0.9: offline, in-memory research annotation pilot.
 * Reviewers follow official YouTube links. No media fetching, caption scraping,
 * personal identifiers, transcript capture or network submission is performed.
 */
(() => {
  const SOURCES = [
    {id:"YT-0001", video:"xLas9oA1SFw", title:"Jamaican Farmer speaking Patois", channel:"Karl", type:"Candidate informal speech", rights:"Not confirmed"},
    {id:"YT-0002", video:"k7Earnq8sHw", title:"WIKITONGUES: Tajaun speaking Jamaican Creole English", channel:"Wikitongues", type:"Language documentation", rights:"Publisher description: CC BY-NC 4.0; extra rights and participant consent unconfirmed"},
    {id:"YT-0003", video:"hNM-BE4xAyo", title:"Jamaican Patois (NOT English!)", channel:"Langfocus", type:"Educational commentary", rights:"Not confirmed"},
    {id:"YT-0004", video:"pypNXPy80Ys", title:"Jamaican Patois: Chat Patwah Intro", channel:"Chat Patwah", type:"Language lesson", rights:"Permission requested; not granted"},
    {id:"YT-0005", video:"JAe4Fxd8ZqI", title:"Jamaican Patois: Me You I Them & Us", channel:"Chat Patwah", type:"Language lesson", rights:"Permission requested; not granted"},
    {id:"YT-0006", video:"1M4xbzivRUo", title:"Why Jamaican Schools Need to Teach Patois — interview", channel:"Irie Jam Radio", type:"Interview", rights:"Not confirmed; YouTube source ID requires human confirmation"}
  ];
  const HEADERS = [
    "observation_id","source_id","video_id","timestamp_seconds",
    "observed_lexeme_or_feature","original_nonverbatim_note","usage_register",
    "code_switching_observed","reviewer_role","reviewed_date",
    "actual_playback_confirmed","transcript_reuse_permission",
    "original_audio_permission","ai_training_permission",
    "second_source_reference","independent_linguistic_review",
    "privacy_assessment","release_decision","restricted_evidence_reference",
    "linguistic_category","reviewer_code"
  ];
  const byId = id => document.getElementById(id);
  const queue = [];
  const source = byId("source");
  const status = byId("status");
  const banner = (text, error = false) => {
    status.textContent = text;
    status.className = error ? "status error" : "status";
  };
  const selected = () => SOURCES.find(x => x.id === source.value) || SOURCES[0];
  const validSeconds = () => {
    const raw = byId("timestamp").value;
    if (!/^\d+$/.test(raw)) return null;
    const seconds = Number(raw);
    return Number.isInteger(seconds) && seconds >= 0 && seconds <= 86400 ? seconds : null;
  };
  const videoLink = (item, seconds = 0) => {
    const root = "https://www.youtube.com/watch?v=" + item.video;
    return seconds ? root + "&t=" + seconds + "s" : root;
  };
  const renderSource = () => {
    const s = selected();
    byId("sourceDetails").textContent =
      s.id + " · " + s.channel + " · " + s.type +
      " · Rights: " + s.rights +
      ". Public source listing does not establish recorded speech, speaker origin, licence for reuse or permission for AI training.";
    byId("watch").href = videoLink(s);
    byId("seek").href = videoLink(s, validSeconds() ?? 0);
  };
  SOURCES.forEach(s => {
    const option = document.createElement("option");
    option.value = s.id;
    option.textContent = s.id + " — " + s.title + " (" + s.channel + ")";
    source.appendChild(option);
  });
  source.addEventListener("change", renderSource);
  byId("timestamp").addEventListener("input", renderSource);
  byId("note").addEventListener("input", () => {
    byId("chars").textContent = byId("note").value.length + " / 240";
  });
  const isoLocal = () => {
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2,"0");
    const d = String(now.getDate()).padStart(2,"0");
    return y + "-" + m + "-" + d;
  };
  const noIdentifiers = (value) =>
    !/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/i.test(value) &&
    !/(?:\+?\d[\s().-]*){8,}/.test(value);
  const observationId = () =>
    "OBS-" + Date.now().toString(36).toUpperCase() + "-" +
    Math.random().toString(36).slice(2,8).toUpperCase();
  const appendText = (parent, tag, value) => {
    const element = document.createElement(tag);
    element.textContent = value;
    parent.appendChild(element);
    return element;
  };
  const renderQueue = () => {
    const body = byId("items");
    body.replaceChildren();
    byId("count").textContent = String(queue.length);
    byId("export").disabled = queue.length === 0;
    byId("clear").disabled = queue.length === 0;
    if (!queue.length) {
      const tr=document.createElement("tr");
      const td=appendText(tr,"td","No observations entered.");
      td.colSpan=6; td.className="muted"; body.appendChild(tr); return;
    }
    queue.forEach((item,index)=>{
      const tr = document.createElement("tr");
      appendText(tr,"td",item.observation_id + " / " + item.source_id);
      appendText(tr,"td",item.timestamp_seconds + "s");
      appendText(tr,"td",item.observed_lexeme_or_feature);
      appendText(tr,"td",item.original_nonverbatim_note);
      appendText(tr,"td","HOLD · Pending human and rights review");
      const td=document.createElement("td");
      const remove=document.createElement("button");
      remove.type="button";remove.className="btn danger";remove.textContent="Remove";
      remove.setAttribute("aria-label","Remove observation " + item.observation_id);
      remove.addEventListener("click",()=>{queue.splice(index,1);renderQueue();banner("Observation discarded from this browser session.");});
      td.appendChild(remove);tr.appendChild(td);body.appendChild(tr);
    });
  };
  byId("reviewForm").addEventListener("submit",(event)=>{
    event.preventDefault();
    const t=validSeconds();
    const feature=byId("feature").value.trim();
    const note=byId("note").value.trim();
    const reviewer=byId("reviewer").value.trim();
    const external=byId("secondary").value.trim();
    if (t===null){banner("Enter a whole-second timestamp from 0 to 86400.",true);return;}
    if (feature.length<2 || feature.length>100 || note.length<20 || note.length>240){
      banner("Use a short feature name (2–100 chars) and an original explanatory note (20–240 chars).",true);return;
    }
    if(!/^[A-Za-z0-9_-]{2,16}$/.test(reviewer)){
      banner("Use a pseudonymous reviewer code: 2–16 letters, numbers, hyphens or underscores.",true);return;
    }
    if(!noIdentifiers(feature+" "+note+" "+reviewer)){
      banner("Possible email address or phone number detected. Remove personal information.",true);return;
    }
    if(external && !/^https:\/\/[^ ]+$/i.test(external)){
      banner("Second source must be a public HTTPS link, or leave it blank.",true);return;
    }
    if (!byId("listened").checked || !byId("safe").checked) {
      banner("Confirm actual listening and that the note contains no copied or sensitive material.",true);return;
    }
    const s=selected();
    queue.push({
      observation_id:observationId(),source_id:s.id,video_id:s.video,
      timestamp_seconds:String(t),observed_lexeme_or_feature:feature,
      original_nonverbatim_note:note,usage_register:byId("register").value,
      code_switching_observed:byId("switching").value,
      reviewer_role:byId("role").value,reviewed_date:isoLocal(),
      actual_playback_confirmed:"yes",transcript_reuse_permission:"not_granted",
      original_audio_permission:"not_granted",ai_training_permission:"not_granted",
      second_source_reference:external,independent_linguistic_review:"pending",
      privacy_assessment:"pending_manual_review",release_decision:"hold_review_pending",
      restricted_evidence_reference:"",linguistic_category:byId("category").value,
      reviewer_code:reviewer
    });
    renderQueue();banner("Observation added locally. Not verified or published.");
    byId("feature").value="";byId("note").value="";byId("chars").textContent="0 / 240";
    byId("listened").checked=false;byId("safe").checked=false;
  });
  const csvCell = input => {
    let value = String(input ?? "").replace(/\r?\n/g," ");
    // Prevent spreadsheet formula evaluation when opened in Excel.
    if (/^[\s]*[=+\-@]/.test(value)) value = "'" + value;
    return '"' + value.replace(/"/g,'""') + '"';
  };
  byId("export").addEventListener("click",()=>{
    if(!queue.length)return;
    const csv = "\uFEFF" + HEADERS.map(csvCell).join(",") + "\r\n" +
      queue.map(item=>HEADERS.map(k=>csvCell(item[k])).join(",")).join("\r\n") + "\r\n";
    const file=new Blob([csv],{type:"text/csv;charset=utf-8"});
    const url=URL.createObjectURL(file);
    const link=document.createElement("a");
    link.href=url;link.download="jamaican_intelligence_review_only_"+isoLocal()+".csv";
    document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    banner("Review-only CSV exported. Keep it private; do not commit it to the public repository.");
  });
  byId("clear").addEventListener("click",()=>{
    if(queue.length && window.confirm("Discard all unsaved local review notes?")){
      queue.length=0;renderQueue();banner("Local notes discarded.");
    }
  });
  renderSource();renderQueue();
})();