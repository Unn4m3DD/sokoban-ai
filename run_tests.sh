git pull
python3 src/profiler.py > stats.txt
git add .
git commit -m "scores $(date)"
git push