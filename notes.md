# OPTIMIZATION IDEAS

- try using class instead of multiple maps

- optimize the last row. i.e. if the state is found
- store the zero position too in the heap or in other data structure
    - makes it slower
- instead of correct_position dict, use if else
- store only steps and backtrace the solution in the end
- store state as string or interger?
    - but dict key bust be non mutable
- reduce multiple calculations of heuristic function
- assign integers to up down right left
- choose directions based on the position of the zero
- [] vs .get()
    - lite

# Time
- working_integer_dir_reconstruction.py 
    - cool - 55 s
    - hot - 68 s
- working_combined_dict_reconstruction.py 
    - fluke - 60 s
    - hot - 72 s
- working_combined_dict_except_zeropos_reconstruction.py
    - hot - 72 s
- working_path_reconstruction.py
    - sometimes - 56 s
    - hot - 69 s
- working_integer_dir_reconstruction_with_combined_heuristic/py
    - hot - 90, 95 s