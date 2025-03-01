import streamlit as st
import plotly.graph_objs as go
import numpy as np
from random import uniform

# Function to generate random positions for agents
def generate_positions(num_agents=2, bounds=(0, 10)):
    return np.array([[uniform(*bounds), uniform(*bounds)] for _ in range(num_agents)])

# Initialize Streamlit app
st.title("Agent Movement Simulation")

# Sidebar Controls
num_agents = st.sidebar.slider("Number of Agents", 1, 10, 2)

# Session state to carry forward positions and simulation state
if 'positions' not in st.session_state:
    st.session_state.positions = generate_positions(num_agents)

if 'fig' not in st.session_state:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=st.session_state.positions[:, 0],
        y=st.session_state.positions[:, 1],
        mode='markers+text',
        marker=dict(size=15),
        text=[f'A{i+1}' for i in range(num_agents)]))
    fig.update_layout(
    title="Agent Movement Simulation",
    xaxis=dict(range=[0, 10]),
    yaxis=dict(range=[0, 10]),
    hovermode="closest")
    st.session_state.fig = fig

if 'start_simulation' not in st.session_state:
    st.session_state.start_simulation = False
if 'stop_simulation' not in st.session_state:
    st.session_state.stop_simulation = True

start_simulation = st.sidebar.button("Start Simulation")
stop_simulation = st.sidebar.button("Stop Simulation")

if stop_simulation and st.session_state.start_simulation:
    st.session_state.start_simulation = False
    st.session_state.stop_simulation = True
elif start_simulation and st.session_state.stop_simulation:
    st.session_state.start_simulation = True
    st.session_state.stop_simulation = False

# Simulation logic
print(st.session_state.positions, st.session_state.start_simulation, st.session_state.stop_simulation)
if st.session_state.start_simulation and not st.session_state.stop_simulation:
    new_positions = st.session_state.positions + np.random.uniform(-0.5, 0.5, size=st.session_state.positions.shape)
    st.session_state.positions[:] = np.clip(new_positions, 0, 10)  # Ensure agents stay within bounds

    st.session_state.fig.update_traces(go.Scatter(x=st.session_state.positions[:, 0], y=st.session_state.positions[:, 1], 
                        mode='markers+text', marker=dict(size=15), 
                        text=[f'A{i+1}' for i in range(num_agents)]))
    st.plotly_chart(st.session_state.fig, use_container_width=True)
    st.rerun()  # Using experimental_rerun for automatic updates

else:
    st.plotly_chart(st.session_state.fig, use_container_width=True)
