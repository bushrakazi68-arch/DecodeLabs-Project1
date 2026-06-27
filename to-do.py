"""
DecodeLabs - Industrial Training Kit
Project 1: Enterprise Task Lifecycle Management (Web Interface Edition)

This script starts a local development server for your To-Do Tracker.
Run the script, then open http://localhost:8082 in any web browser.
"""

import http.server
import json
import string
import urllib.parse

# Phase 2: Core State Engine
# Task database stored cleanly as a mutable sequence of schemas
TASK_DATABASE = []


def add_task(title: str, priority: str) -> str:
    """Validates inputs and safely appends a new node to the task state."""
    if not title.strip():
        return "Error: Task description cannot be empty."
        
    task_item = {
        "id": len(TASK_DATABASE) + 1,
        "title": html_escape(title),
        "priority": priority,
        "status": "Pending"
    }
    TASK_DATABASE.append(task_item)
    return "Success: Task successfully committed to lifecycle database."


def complete_task(task_id: int) -> str:
    """Mutates task status within state arrays securely based on explicit user command."""
    for task in TASK_DATABASE:
        if task["id"] == task_id:
            task["status"] = "Completed"
            return "Success: Task marked as completed."
    return "Error: Target task element identifier not located."


def html_escape(text: str) -> str:
    """Sanitizes strings to protect user environment from script injection."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# HTML UI Template for Phase 3 Provisioning
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DecodeLabs - Task Operations Core</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #e2e8f0; padding: 40px; display: flex; justify-content: center; }}
        .card {{ background-color: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); max-width: 650px; width: 100%; border: 1px solid #334155; }}
        h2 {{ color: #38bdf8; margin-top: 0; text-align: center; border-bottom: 2px solid #334155; padding-bottom: 10px; }}
        label {{ display: block; margin: 15px 0 5px; font-weight: 600; color: #94a3b8; }}
        input, select {{ width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #475569; background-color: #0f172a; color: #fff; box-sizing: border-box; font-size: 16px; }}
        button {{ width: 100%; background-color: #0284c7; color: white; padding: 12px; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 20px; transition: background 0.2s; }}
        button:hover {{ background-color: #0369a1; }}
        .action-btn {{ width: auto; display: inline-block; padding: 6px 12px; font-size: 13px; margin: 0; background-color: #10b981; border-radius: 4px; }}
        .action-btn:hover {{ background-color: #059669; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 25px; }}
        th, td {{ padding: 12px 10px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ color: #94a3b8; font-weight: 600; }}
        .status-badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        .badge-pending {{ background-color: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid #f59e0b; }}
        .badge-completed {{ background-color: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid #10b981; }}
        .priority-high {{ border-left: 4px solid #f43f5e; }}
        .priority-medium {{ border-left: 4px solid #f59e0b; }}
        .priority-low {{ border-left: 4px solid #10b981; }}
        .status-msg {{ padding: 10px; border-radius: 4px; font-size: 14px; margin-top: 10px; text-align: center; }}
        .status-success {{ background-color: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid #10b981; }}
        .status-error {{ background-color: rgba(244, 63, 94, 0.1); color: #f43f5e; border: 1px solid #f43f5e; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>DecodeLabs Task Lifecycle Tracker</h2>
        
        <form method="POST" action="/add-task">
            <label for="title">Task Objective / Description:</label>
            <input type="text" id="title" name="title" required placeholder="e.g., Run security verification patches">
            
            <label for="priority">Priority Tier Assignment:</label>
            <select id="priority" name="priority">
                <option value="High">High Priority</option>
                <option value="Medium" selected>Medium Priority</option>
                <option value="Low">Low Priority</option>
            </select>
            
            <button type="submit">Deploy Strategy To Pipeline</button>
        </form>

        {status_placeholder}

        <h3>System Execution Backlog</h3>
        <table>
            <thead>
                <tr>
                    <th>Objective</th>
                    <th>Tier</th>
                    <th>State</th>
                    <th style="text-align: right;">Action</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
</body>
</html>
"""


class TaskWebHandler(http.server.BaseHTTPRequestHandler):
    """System Interface Phase: Maps client routing and pipeline state updates."""
    
    def do_GET(self):
        """Phase 3 Provisioning: Compiles down and serves the active tracking UI."""
        self.render_dashboard()

    def do_POST(self):
        """Phase 1 Capture: Unpacks payload streams to invoke mutations or state closures."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)
        
        status_message = ""
        
        if self.path == "/add-task":
            title = params.get('title', [''])[0]
            priority = params.get('priority', ['Medium'])[0]
            
            result = add_task(title, priority)
            status_class = "status-success" if "Success" in result else "status-error"
            status_message = f"<div class='status-msg {status_class}'>{result}</div>"
            
        elif self.path == "/complete":
            try:
                task_id = int(params.get('id', [0])[0])
                result = complete_task(task_id)
                status_class = "status-success" if "Success" in result else "status-error"
                status_message = f"<div class='status-msg {status_class}'>{result}</div>"
            except (ValueError, TypeError):
                status_message = "<div class='status-msg status-error'>Flawed asset validation dropped.</div>"
                
        self.render_dashboard(status_message)

    def render_dashboard(self, status_html=""):
        """Iterates over task allocations using memory-optimized linear concatenation O(N)."""
        rows_list = []
        for item in TASK_DATABASE:
            badge_class = "badge-completed" if item["status"] == "Completed" else "badge-pending"
            priority_class = f"priority-{item['priority'].lower()}"
            
            # Conditionally supply action controls based on the current state of the array row
            action_td = '<span style="color:#64748b; font-size:13px;">Archived</span>'
            if item["status"] == "Pending":
                action_td = f"""
                <form method="POST" action="/complete" style="display:inline;">
                    <input type="hidden" name="id" value="{item['id']}">
                    <button type="submit" class="action-btn">Resolve</button>
                </form>
                """
            
            rows_list.append(
                f"<tr class='{priority_class}'><td><strong>{item['title']}</strong></td>"
                f"<td>{item['priority']}</td>"
                f"<td><span class='status-badge {badge_class}'>{item['status']}</span></td>"
                f"<td style='text-align: right;'>{action_td}</td></tr>"
            )
        
        table_rows = "".join(rows_list) if rows_list else "<tr><td colspan='4' style='color:#64748b; text-align:center;'>No active tasks registered inside engine.</td></tr>"
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        response_body = HTML_TEMPLATE.format(
            status_placeholder=status_html,
            table_rows=table_rows
        )
        self.wfile.write(response_body.encode('utf-8'))

    def log_message(self, format, *args):
        return  # Mutes logs to ensure terminal readability


if __name__ == "__main__":
    # Assigned to Port 8082 to guarantee zero address overlaps across all three portfolio projects
    PORT = 8082
    server = http.server.HTTPServer(('localhost', PORT), TaskWebHandler)
    print("=" * 60)
    print(f" DECODELABS TASK TRACKER CORE LIVE AT: http://localhost:{PORT} ")
    print(" [CONTROL] Press Ctrl+C in this terminal window to stop the server ")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Server terminated gracefully.")
        server.server_close()