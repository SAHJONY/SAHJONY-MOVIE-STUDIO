import { agents, systemLayers } from "@/lib/studio";

function StatusDot({ active }: { active: boolean }) {
  return <span className={active ? "dot dotLive" : "dot"} aria-hidden="true" />;
}

export default function Home() {
  const higgsfieldReady = Boolean(process.env.HF_API_KEY && process.env.HF_API_SECRET);
  const supabaseReady = Boolean(process.env.SUPABASE_URL && (process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY));

  return (
    <main>
      <section className="hero shell">
        <div>
          <p className="eyebrow">SAHJONY CAPITAL LLC · AUTONOMOUS PRODUCTION</p>
          <h1>Movie OS <span>V3</span></h1>
          <p className="lede">A state-centric studio where specialized AI departments direct, generate, inspect, repair, and assemble cinema from one canonical production graph.</p>
        </div>
        <div className="systemState">
          <span><StatusDot active /> ORCHESTRATOR ONLINE</span>
          <code>STATE / DEVELOPMENT</code>
        </div>
      </section>

      <section className="metrics shell">
        <article><small>AGENTS</small><strong>{agents.length}</strong><span>specialized departments</span></article>
        <article><small>FIRST MANIFEST</small><strong>09</strong><span>shots · 45 seconds</span></article>
        <article><small>QA IDENTITY GATE</small><strong>95%</strong><span>minimum acceptance</span></article>
        <article><small>AUTO RETRY</small><strong>02</strong><span>bounded repair cycles</span></article>
      </section>

      <section className="grid shell">
        <article className="panel agentsPanel">
          <header><div><p className="kicker">DEPARTMENT MESH</p><h2>Agent Command</h2></div><span className="badge">PERMISSIONED</span></header>
          <div className="agentList">
            {agents.map((agent) => (
              <div className="agent" key={agent.role}>
                <div><StatusDot active={agent.status !== "IDLE"} /><strong>{agent.role}</strong></div>
                <p>{agent.owner}</p>
                <code>{agent.status}</code>
              </div>
            ))}
          </div>
        </article>

        <article className="panel pipelinePanel">
          <header><div><p className="kicker">CANONICAL EXECUTION</p><h2>Production Graph</h2></div><span className="badge">EVENT DRIVEN</span></header>
          <div className="pipeline">
            {['BRIEF','SCRIPT','VISDEV','PREVIS','ASSETS','RENDER','QA','MASTER'].map((stage, index) => (
              <div className="stage" key={stage}><span>{String(index + 1).padStart(2, '0')}</span><strong>{stage}</strong></div>
            ))}
          </div>
          <div className="cameraCard">
            <p className="kicker">CURRENT CAMERA DSL</p>
            <code>orbit(subject="ARIA", lens=50mm, radius=4.5m, arc=110°, continuity=LOCKED)</code>
          </div>
        </article>
      </section>

      <section className="grid lower shell">
        <article className="panel">
          <header><div><p className="kicker">RUNTIME</p><h2>Provider Readiness</h2></div></header>
          <div className="provider"><span><StatusDot active={higgsfieldReady} />Higgsfield</span><code>{higgsfieldReady ? 'CONFIGURED' : 'MISSING ENV'}</code></div>
          <div className="provider"><span><StatusDot active={supabaseReady} />Supabase</span><code>{supabaseReady ? 'CONFIGURED' : 'MISSING ENV'}</code></div>
          <p className="fineprint">Health reports configuration presence only. Secret values are never returned to the browser.</p>
        </article>

        <article className="panel">
          <header><div><p className="kicker">MOVIE KERNEL</p><h2>System Layers</h2></div></header>
          <div className="layers">
            {systemLayers.map((layer, index) => <div key={layer}><span>{index + 1}</span>{layer}</div>)}
          </div>
        </article>
      </section>

      <footer className="shell">
        <span>SAHJONY MOVIE OS</span>
        <code>PROJECT → SCENE → SHOT → ASSET → RENDER → QA → MASTER</code>
      </footer>
    </main>
  );
}
