import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Parameters:
# - a list of subject areas for a paper
# - a list of "primary" subject areas
# - a list of "secondary" subject areas,
# - a "primary weight" (the weight given to the primary subject areas in the
#   weighted average between primary and secondary areas)
#
# Returns:
# - an affinity score between paper and area chair
def subject_area_affinity(paper_subject_areas, primary_subject_areas, secondary_subject_areas, primary_weight=0.7):

    paperset = set(paper_subject_areas)
    primaryset = set(primary_subject_areas)
    secondaryset = set(secondary_subject_areas)

    primary_overlap = float(len(paperset & primaryset))
    secondary_overlap = float(len(paperset & secondaryset))

    primary_affinity = primary_overlap/float(len(paperset))
    secondary_affinity = secondary_overlap/float(len(paperset))

    return (primary_affinity * primary_weight) + (secondary_affinity * (1-primary_weight))


# Parameters:
# - subject_list_A: a list (of any length) of subject area strings
# - subject_list_B: ""
#
# Returns:
# - an affinity score between subject_list_A and subject_list_B

def subject_area_overlap(subject_list_A, subject_list_B):
    subject_set_A = set(subject_list_A)
    subject_set_B = set(subject_list_B)
    intersection = int(len(subject_set_A & subject_set_B))
    max_denominator = max([int(len(s)) for s in [subject_set_A, subject_set_B]])
    if max_denominator > 0:
        return intersection / max_denominator
    else:
        return 0
