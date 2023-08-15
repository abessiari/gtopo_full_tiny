import os
import sys
import re
import numpy as np

def special():
    dataset = "gtopo_full_tiny"
    nRanks = 16
    pairs = set()
    # collect data from output
    for i in range(nRanks):
        fname = "kokkos_16/BranchDecomposition_Rank_{}_Block_0.txt".format(str(i))
        with open(fname, "r") as f:
            for line in f.readlines():
                formatted_line = (re.sub(' +', ' ', line.replace('\n',' '))).strip()
                ll = formatted_line.split(" ")
                try:
                    if len(ll) != 2:
                        raise ValueError
                    upper = int(ll[0])
                    lower = int(ll[1])
                    pairs.add((upper, lower))
                except ValueError:
                    print("Wrong format line: ", formatted_line)
                    continue
    
    pairs = list(pairs)
    np.savetxt("unsorted_output_{}.txt".format(dataset), np.asarray(pairs), fmt="%d", delimiter=" ")
    pairs.sort()
    np.savetxt("sorted_output_{}.txt".format(dataset), np.asarray(pairs), fmt="%d", delimiter=" ")

    # load ground truth
    gt_pairs = []
    gt_fname = "./out/branch_decomposition_volume_hybrid_{}.txt".format(dataset)
    with open(gt_fname, "r") as gt_f:
        for line in gt_f.readlines():
            formatted_line = (re.sub(' +', ' ', line.replace('\n',' '))).strip()
            ll = formatted_line.split(" ")
            try:
                if len(ll) != 2:
                    raise ValueError
                upper = int(ll[0])
                lower = int(ll[1])
                gt_pairs.append((upper, lower))
            except ValueError:
                print("Wrong format line: ", formatted_line)
                continue
    np.savetxt("unsorted_ground_truth_{}.txt".format(dataset), np.asarray(gt_pairs), fmt="%d", delimiter=" ")
    gt_pairs.sort()
    np.savetxt("sorted_ground_truth_{}.txt".format(dataset), np.asarray(gt_pairs), fmt="%d", delimiter=" ")
    import sys
    sys.exit(1)
    
    lpairs = len(pairs)
    lgt = len(gt_pairs)
    print("len(VTKm output):", lpairs)
    print("len(Ground Truth):", lgt)

    nErrors = abs(lpairs - lgt)
    for row in range(max(lpairs, lgt)):
        if row > lpairs:
            print("Missing branch:", gt_pairs[row])
        elif row > lgt:
            print("Wrongly appearing branch:", pairs[row])
        elif pairs[row][0] != gt_pairs[row][0] or pairs[row][1] != gt_pairs[row][1]:
            print("Inconsistent branch: {}-{} (VTKm) vs. {}-{} (Ground Truth)".format(
                str(pairs[row][0]), str(pairs[row][1]), 
                str(gt_pairs[row][0]), str(gt_pairs[row][1]), 
            ))
            nErrors += 1
    print("# of Errors:", nErrors)
    
special()
