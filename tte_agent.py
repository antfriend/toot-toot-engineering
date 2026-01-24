import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

# ---------------------------
# Sandbox + file helpers
# ---------------------------

WORKSPACE = Path(__file__).resolve().parent
README_CANDIDATES = [
    "README.md",
]


def _safe_path(rel_path: str) -> Path:
    """
    Resolve rel_path inside WORKSPACE and prevent escaping via .. or absolute paths.
    """
    p = (WORKSPACE / rel_path).resolve()
    if not str(p).startswith(str(WORKSPACE)):
        raise ValueError(f"Path escapes workspace: {rel_path}")
    return p


def tool_list_dir(path: str = ".", max_entries: int = 200) -> Dict[str, Any]:
    p = _safe_path(path)
    if not p.exists():
        return {"ok": False, "error": f"Path does not exist: {path}"}
    if not p.is_dir():
        return {"ok": False, "error": f"Not a directory: {path}"}

    entries = []
    for i, child in enumerate(sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))):
        if i >= max_entries:
            entries.append({"name": "...", "type": "truncated"})
            break
        entries.append(
            {
                "name": child.name,
                "type": "dir" if child.is_dir() else "file",
                "size": child.stat().st_size if child.is_file() else None,
            }
        )
    return {"ok": True, "path": str(p.relative_to(WORKSPACE)), "entries": entries}


def tool_read_file(path: str, max_bytes: int = 200_000) -> Dict[str, Any]:
    p = _safe_path(path)
    if not p.exists():
        return {"ok": False, "error": f"File does not exist: {path}"}
    if not p.is_file():
        return {"ok": False, "error": f"Not a file: {path}"}

    data = p.read_bytes()
    if len(data) > max_bytes:
        data = data[:max_bytes]
        truncated = True
    else:
        truncated = False

    try:
        text = data.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        # fall back, still useful for many Windows files
        text = data.decode("utf-8", errors="replace")
        encoding = "utf-8 (with replacement)"

    return {
        "ok": True,
        "path": str(p.relative_to(WORKSPACE)),
        "encoding": encoding,
        "truncated": truncated,
        "content": text,
    }


def tool_write_file(path: str, content: str, overwrite: bool = True) -> Dict[str, Any]:
    p = _safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    if p.exists() and (not overwrite):
        return {"ok": False, "error": f"File exists and overwrite=False: {path}"}

    p.write_text(content, encoding="utf-8")
    return {"ok": True, "path": str(p.relative_to(WORKSPACE)), "bytes": len(content.encode("utf-8"))}


def tool_run_shell(command: str, timeout_ms: int = 60_000) -> Dict[str, Any]:
    """
    Runs a command in WORKSPACE. This is powerful: keep your workspace clean.
    """
    # Basic "safety bumper": deny a few obviously destructive commands.
    # You can expand this list later.
    lowered = command.strip().lower()
    deny = ["rm -rf", "del /s", "format ", "diskpart", "bcdedit", "cipher /w", "rd /s", "rmdir /s"]
    if any(d in lowered for d in deny):
        return {"ok": False, "error": "Command denied by safety policy."}

    try:
        completed = subprocess.run(
            command,
            cwd=str(WORKSPACE),
            shell=True,
            capture_output=True,
            text=True,
            timeout=max(1, timeout_ms // 1000),
        )
        return {
            "ok": True,
            "command": command,
            "exit_code": completed.returncode,
            "stdout": completed.stdout[-20000:],  # keep last chunk
            "stderr": completed.stderr[-20000:],
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "command": command, "error": f"Timeout after {timeout_ms}ms"}


# ---------------------------
# OpenAI tool schemas
# ---------------------------

TOOLS = [
    {
        "type": "function",
        "name": "list_dir",
        "description": "List files/folders within the workspace directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative path inside workspace (default '.')"},
                "max_entries": {"type": "integer", "description": "Max entries to return", "default": 200},
            },
            "required": [],
        },
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "Read a text file within the workspace directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative file path inside workspace"},
                "max_bytes": {"type": "integer", "description": "Max bytes to read", "default": 200000},
            },
            "required": ["path"],
        },
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "Write a text file within the workspace directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Relative file path inside workspace"},
                "content": {"type": "string", "description": "File content (utf-8)"},
                "overwrite": {"type": "boolean", "description": "Overwrite if exists", "default": True},
            },
            "required": ["path", "content"],
        },
    },
    {
        "type": "function",
        "name": "run_shell",
        "description": "Run a shell command in the workspace. Use for tests/build/search.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to run"},
                "timeout_ms": {"type": "integer", "description": "Timeout in milliseconds", "default": 60000},
            },
            "required": ["command"],
        },
    },
]

TOOL_IMPL = {
    "list_dir": lambda args: tool_list_dir(**args),
    "read_file": lambda args: tool_read_file(**args),
    "write_file": lambda args: tool_write_file(**args),
    "run_shell": lambda args: tool_run_shell(**args),
}


# ---------------------------
# ---------------------------
# ---------------------------
# TTE agent loop
# ---------------------------
# ---------------------------
# ---------------------------

SYSTEM_INSTRUCTIONS = """You may ONLY access files via the provided tools and ONLY within the workspace.
Goal: run a "Toot-Toot Engineering" workflow to the end of the PLAN:
- Output  "Greetings, I am a TTE agent. I'm in the workshop now, firing up the creative forge."
- Read the README and associated documents, then execute the workflow from the current step to the end of the PLAN.
- Do the current step in the workflow then begin the next step and continue until the PLAN is completed.
- Then output "Processing Completed!"
- Then output "EXCELENT!" on its own line and stop.

Constraints:
- Do NOT read or write secrets files (.env, id_rsa, ssh keys). If you see them, ignore.
"""


def find_readme() -> Optional[str]:
    for name in README_CANDIDATES:
        p = WORKSPACE / name
        if p.exists() and p.is_file():
            return name
    return None


def needs_user_choice(text: str) -> bool:
    lowered = text.lower()
    return "next cycle" in lowered and "prompt" in lowered and ("choose" in lowered or "select" in lowered)


def main():
    print("TOOT TOOT ENGINEERING is leaving the station.")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Oh Toot! Missing OPENAI_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    model = "gpt-5.2"
    client = OpenAI()

    readme_name = find_readme()
    if not readme_name:
        print("Oh Toot! No README.md found.", file=sys.stderr)
        sys.exit(1)

    # Conversation state: we’ll keep feeding prior tool outputs back to the model
    input_items: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        {"role": "user", "content": f"Start in workspace: {WORKSPACE.name}. The README file is {readme_name}."},
    ]

    max_steps = 100
    for step in range(1, max_steps + 1):
        resp = client.responses.create(
            model=model,
            input=input_items,
            tools=TOOLS,
        )

        # Collect any assistant text
        assistant_texts: List[str] = []
        tool_calls: List[Tuple[str, str, Dict[str, Any]]] = []
        output_items: List[Dict[str, Any]] = []

        for item in resp.output:
            # resp.output items may be dict-like or pydantic models.
            if hasattr(item, "model_dump"):
                item_dict = item.model_dump()
            elif hasattr(item, "dict"):
                item_dict = item.dict()
            else:
                item_dict = item
            output_items.append(item_dict)

            item_type = getattr(item, "type", None)
            if item_type is None:
                item_type = item.get("type")

            if item_type == "message":
                # message content can be an array of parts
                content = getattr(item, "content", None)
                if content is None:
                    content = item.get("content", [])
                for part in content:
                    part_type = getattr(part, "type", None)
                    if part_type is None:
                        part_type = part.get("type")
                    if part_type == "output_text":
                        text = getattr(part, "text", None)
                        if text is None:
                            text = part.get("text", "")
                        assistant_texts.append(text)
            elif item_type == "function_call":
                call_id = getattr(item, "call_id", None)
                if call_id is None:
                    call_id = item.get("call_id")
                name = getattr(item, "name", None)
                if name is None:
                    name = item.get("name")
                arguments = getattr(item, "arguments", None)
                if arguments is None:
                    arguments = item.get("arguments", "{}")
                tool_calls.append((call_id, name, json.loads(arguments)))

        if assistant_texts:
            print("\n".join(t.strip() for t in assistant_texts if t.strip()))

        if needs_user_choice("\n".join(assistant_texts)):
            input_items.append(
                {
                    "role": "user",
                    "content": (
                        "No selection will be provided. "
                        "List 3 possible next-cycle prompts and finish with EXCELENT!."
                    ),
                }
            )

        # Add assistant outputs (including tool calls) to the conversation state.
        input_items.extend(output_items)

        if not tool_calls:
            # No tool calls requested: continue unless the model signaled completion.
            combined_text = "\n".join(assistant_texts)
            if "EXCELENT!" in combined_text:
                return
            input_items.append(
                {
                    "role": "user",
                    "content": "Continue the workflow. Use tools when needed; if finished, say EXCELENT!",
                }
            )
            continue

        # Execute tool calls and append outputs as function_call_output items
        for call_id, name, args in tool_calls:
            try:
                result = TOOL_IMPL[name](args)
            except Exception as e:
                result = {"ok": False, "error": str(e)}

            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": json.dumps(result),
                }
            )

    print(f"\nStopped after {max_steps} steps (budget).", file=sys.stderr)


if __name__ == "__main__":
    main()
