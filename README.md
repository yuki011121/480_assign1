# 480_assign1
python3 make_vacuum_world.py 5 5 0.2 3 > test_world.txt 

python3 planner.py uniform-cost test_world.txt

python3 planner.py depth-first test_world.txt