set -xe

repo=/repo/roman-desc-sims
tagged_collection=u/descdm/step2a_outputs_w_2024_22

#dstype_option=""
#dstype_option="--dataset-type visitSummary"
dstype_option="--dataset-type packages"
#dstype_option="--dataset-type ccdVisitTable"
#dstype_option="--dataset-type isolated_star_cat"
#dstype_option="--dataset-type ccdVisitTable"

#butler query-collections ${repo} u/descdm/step2a_???_w_2024_22/2024*

#butler query-datasets --collections ${tagged_collection} ${repo}

#butler remove-collections ${repo} ${tagged_collection}

butler associate ${dstype_option} --collections u/descdm/step2a_000_w_2024_22/20240806T210454Z ${repo} ${tagged_collection}
butler associate ${dstype_option} --collections u/descdm/step2a_001_w_2024_22/20240807T001556Z ${repo} ${tagged_collection}
