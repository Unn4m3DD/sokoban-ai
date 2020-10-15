git pull
python3 src/profiler.py -s
mv stats_new.txt stats.txt
git add .
git commit -m "scores $(date)"
git push