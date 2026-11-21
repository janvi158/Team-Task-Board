#This Frontend is created by Madhura

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Team Task Board",
    page_icon="📋",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "id": 1,
            "title": "Design homepage",
            "assignee": "Alice",
            "priority": "High",
            "status": "To Do"
        },
        {
            "id": 2,
            "title": "Develop login API",
            "assignee": "Bob",
            "priority": "Medium",
            "status": "In Progress"
        },
        {
            "id": 3,
            "title": "Test dashboard",
            "assignee": "Charlie",
            "priority": "Low",
            "status": "Done"
        }
    ]

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
    .main {
        background-color: #f5f7fb;
    }

    .task-card {
        background: white;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin-bottom: 12px;
    }

    .task-title {
        font-size: 17px;
        font-weight: bold;
        color: #1f2937;
    }

    .subtitle {
        color: #64748b;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.title("📋 Team Task Board")
st.caption("Manage your team's tasks and track project progress.")

# ---------------- DASHBOARD ----------------

tasks = st.session_state.tasks

total = len(tasks)
todo = sum(t["status"] == "To Do" for t in tasks)
progress = sum(t["status"] == "In Progress" for t in tasks)
done = sum(t["status"] == "Done" for t in tasks)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Tasks", total)
c2.metric("To Do", todo)
c3.metric("In Progress", progress)
c4.metric("Completed", done)

st.divider()

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙️ Task Management")

members = ["Alice", "Bob", "Charlie", "David"]

with st.sidebar.expander("➕ Add New Task", expanded=True):

    with st.form("add_task_form"):
        title = st.text_input("Task Title")

        assignee = st.selectbox(
            "Assign To",
            members
        )

        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )

        status = st.selectbox(
            "Status",
            ["To Do", "In Progress", "Done"]
        )

        submit = st.form_submit_button(
            "Create Task",
            use_container_width=True
        )

        if submit:
            if title.strip():
                new_id = max(
                    [t["id"] for t in tasks],
                    default=0
                ) + 1

                st.session_state.tasks.append({
                    "id": new_id,
                    "title": title,
                    "assignee": assignee,
                    "priority": priority,
                    "status": status
                })

                st.success("Task created!")
                st.rerun()
            else:
                st.error("Please enter a task title.")

# ---------------- FILTERS ----------------

st.subheader("Task Overview")

filter_member = st.selectbox(
    "Filter by team member",
    ["All Members"] + members
)

filtered_tasks = [
    t for t in st.session_state.tasks
    if filter_member == "All Members"
    or t["assignee"] == filter_member
]

# ---------------- TASK BOARD ----------------

col1, col2, col3 = st.columns(3)

columns = {
    "To Do": col1,
    "In Progress": col2,
    "Done": col3
}

for status, column in columns.items():

    with column:
        st.subheader(status)

        status_tasks = [
            t for t in filtered_tasks
            if t["status"] == status
        ]

        st.caption(f"{len(status_tasks)} tasks")

        for task in status_tasks:

            with st.container(border=True):

                st.markdown(
                    f"**{task['title']}**"
                )

                st.caption(
                    f"👤 {task['assignee']}"
                )

                priority_color = {
                    "High": "🔴",
                    "Medium": "🟡",
                    "Low": "🟢"
                }

                st.write(
                    f"{priority_color[task['priority']]} "
                    f"{task['priority']} Priority"
                )

                new_status = st.selectbox(
                    "Update Status",
                    ["To Do", "In Progress", "Done"],
                    index=[
                        "To Do",
                        "In Progress",
                        "Done"
                    ].index(task["status"]),
                    key=f"status_{task['id']}"
                )

                if new_status != task["status"]:
                    task["status"] = new_status
                    st.rerun()

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task['id']}"
                ):
                    st.session_state.tasks.remove(task)
                    st.rerun()

st.divider()

# ---------------- TEAM SUMMARY ----------------

st.subheader("👥 Team Summary")

summary = []

for member in members:
    member_tasks = [
        t for t in st.session_state.tasks
        if t["assignee"] == member
    ]

    summary.append({
        "Team Member": member,
        "Total Tasks": len(member_tasks),
        "To Do": sum(
            t["status"] == "To Do"
            for t in member_tasks
        ),
        "In Progress": sum(
            t["status"] == "In Progress"
            for t in member_tasks
        ),
        "Completed": sum(
            t["status"] == "Done"
            for t in member_tasks
        )
    })

st.dataframe(
    pd.DataFrame(summary),
    use_container_width=True,
    hide_index=True
)
