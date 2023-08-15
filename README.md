GTOPO TINY Set

### Data Split into 4 x 4 parts

```
srun -n16 -c1 --gpus-per-task=1 --gpu-bind=closest ContourTree_Distributed --vtkm-device Kokkos --preSplitFiles --saveOutputData --augmentHierarchicalTree --computeVolumeBranchDecomposition --numBlocks=16 gtopo_full_tiny_part_%d_of_16.txt
```
