# Parameters:
# - a list of subject areas for a paper
# - a list of "primary" subject areas
# - a list of "secondary" subject areas,
# - a "primary weight" (the weight given to the primary subject areas in the
# 	weighted average between primary and secondary areas)
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
