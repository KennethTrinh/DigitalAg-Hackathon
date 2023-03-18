import math

import numpy as np

archaea_base = np.array([0.105, 64.232, 0.726, 35.028])
bacteria_base = np.array([5.34, 1.449, 46.701, 1.517, 3.620,
                            0.981, 0.943, 5.597, 4.349, 3.365, 1.282, 1.07, 0.745])
# microbiome impact on methane production
def microbiome_impact(archaea_props, bacteria_props):
    archaea_effects = np.array([84.6, 0.08, 0.58, -0.08])
    bacteria_effects = np.array(
        [1.06, 6.34, -0.08, 2.51, -2.65, 0.27, 5.32, -1.52, 1.16, -2.01, 5.31, -5.9, 7.92])

    archaea_props -= archaea_base
    bacteria_props -= bacteria_base

    return np.sum(np.dot(archaea_effects, archaea_props)) + np.sum(np.dot(bacteria_effects, bacteria_props))

# microbiome impact on a child's methane production

def microbiome_heredity_impact(archaea_props, bacteria_props):
    archaea_std_dev = np.array([0.025, 22.5, 1.653, 22.1])
    bacteria_std_dev = np.array([1.216, 1.14, 10.411, 0.856, 1.604, 0.193, 0.65, 1.948, 1.838, 1.492, 0.526, 0.479, 0.465])
    archaea_heredity = np.array([0, 0.18, 0.07, 0.2])
    bacteria_heredity = np.array(
        [0.17, 0.13, 0.07, 0.15, 0.02, 0.03, 0, 0.04, 0.03, 0.02, 0.08, 0, 0])
    
    # convert to z score
    archaea_props -= archaea_base
    bacteria_props -= bacteria_base
    archaea_props /= archaea_std_dev
    bacteria_props /= bacteria_std_dev

    return microbiome_impact(archaea_base + np.dot(archaea_props * archaea_heredity, archaea_std_dev), bacteria_base + np.dot(bacteria_props * bacteria_heredity, bacteria_std_dev))


def generate_recommendations(archaea_props, bacteria_props):
    recommendations = []
    archaea_props -= archaea_base
    bacteria_props -= bacteria_base
    if(archaea_props[1] > 0):
        recommendations.append(
            "Adding red seaweed to your feed can decrease the proportion of methanobacteria \
            in the microbiome, lowering methane emissions.")
        
    if(archaea_props[1] > 0 or bacteria_props[2] < 0 or bacteria_props[7] < 0 or bacteria_props[6] < 0 or bacteria_props[9] < 0):
        recommendations.append(
            "Adding wheat to your feed can increase the proportions of methane-consuming \
            bacteria like Veilonellaceae, Fibrobacteraceae, Lachnospiraceae, and \
            Prevotellaceae. In addition, it can decrease the proportion of methanobacteria \
            in the microbiome, lowering methane production.")
        
    if(archaea_props[1] > 0):
        recommendations.append("Adding tannins to your feed can decrease the \
            proportion of methanobacteria in the microbiome, lowering methane emissions.")
        
    if(bacteria_props[2] < 0 or bacteria_props[8] > 0):
        recommendations.append(
                "Adding saponins to your feed can increase the proportion of methane-consuming \
                bacteria like Prevotellaceae in the microbiome, while decreasing \
                the proportion of methane emitters like Ruminococcaceae.")
    
    if(bacteria_props[1] > 0 or bacteria_props[3] > 0 or bacteria_props[8] > 0):
        recommendations.append(
            "Adding fatty oils and starch to your feed can decrease the proportion \
            of methane emitters like Ruminococcaceae, BS11, and RF16.")
        
    return recommendations