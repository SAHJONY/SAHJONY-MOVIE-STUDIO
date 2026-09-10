export type AgentStatus = "ACTIVE" | "READY" | "IDLE";

export const agents = [
  { role: "Master Director", owner: "Scope · approvals · conflicts", status: "ACTIVE" as AgentStatus },
  { role: "Continuity", owner: "Canon · character/world state", status: "READY" as AgentStatus },
  { role: "Art Director", owner: "Style · visual bible · assets", status: "READY" as AgentStatus },
  { role: "Cinematographer", owner: "Camera · lens · blocking", status: "READY" as AgentStatus },
  { role: "Lighting", owner: "Lighting · exposure", status: "READY" as AgentStatus },
  { role: "Render Worker", owner: "Provider execution", status: "READY" as AgentStatus },
  { role: "QA", owner: "Identity · continuity · artifacts", status: "READY" as AgentStatus },
  { role: "Editor", owner: "Timeline · cuts · master", status: "IDLE" as AgentStatus },
];

export const systemLayers = [
  "Canonical Project State",
  "Cinematic Memory",
  "Agent Permission Kernel",
  "Production DAG + Scheduler",
  "Cinematography DSL",
  "Provider Governor",
  "QA + Auto-Remediation",
  "Provenance Ledger",
];
