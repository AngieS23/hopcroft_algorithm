import networkx as nx
import matplotlib.pyplot as plt

initial_states = {0}
states = {0, 1, 2, 3, 4, 5} 
alphabet = {'a', 'b'} 
transitions = { 0: {'a': 1, 'b': 2}, 
                1: {'a': 0, 'b': 3}, 
                2: {'a': 4, 'b': 5}, 
                3: {'a': 4, 'b': 5}, 
                4: {'a': 4, 'b': 5}, 
                5: {'a': 5, 'b': 5}
              } 
accepting_states = {1, 3, 5}

def visualize(states, transitions, accepting_states, initial_states, title):
  G = nx.DiGraph()

  for state in states:
    G.add_node(state)

  for state, trans in transitions.items():
    for symbol, target in trans.items():
      G.add_edge(state, target, label=symbol)

  color_map = []
  for state in states:
    if state in initial_states:
      color_map.append('#e9f7cb')
    elif state in accepting_states:
      color_map.append('#cbf7e2')
    else:
      color_map.append('#cbdaf7')

  pos = nx.spring_layout(G)
  nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=700, font_size=16, font_color='black', font_weight='bold', arrows=True)
  edge_labels = nx.get_edge_attributes(G, 'label')
  nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

  plt.title(title)
  plt.show()

def update_transitions(states, transitions, initial_states, accepting_states):
  pass

def split(set_state, transitions, alphabet, actual_sets):
  memory = {}
  transition = {}
  for state in set_state:
    for i in alphabet:
      original_transition = transitions.get(state, {}).get(i, None)
      for actual_set in actual_sets:
        if original_transition in actual_set:
          transition[i] = actual_set
          break
    transition_tuple = tuple(transition.items())
    if transition_tuple in memory:
      memory[transition_tuple].add(state)
    else:
      memory[transition_tuple] = {state}
  return {frozenset(states_set) for states_set in memory.values()}

def hopcroft_minimization(states, accepting_states, transitions, alphabet, initial_states):
  non_accepting_states = states - accepting_states
  states0 = {frozenset(non_accepting_states), frozenset(accepting_states)}
  states1 = {}

  visualize(states, transitions, accepting_states, initial_states, "Initial DFA")

  while states1 != states0:
    states1 = states0.copy()
    states0.clear()
    for set_state in states1:
      states0 = states0 | split(set_state, transitions, alphabet, states1)

  final_transitions, final_accepting, final_initial = update_transitions(states0, transitions, initial_states, accepting_states)
  visualize(states0, final_transitions, final_accepting, final_initial, "Minimized DFA")

hopcroft_minimization(states, accepting_states, transitions, alphabet, initial_states)
