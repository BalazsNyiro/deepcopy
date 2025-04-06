

DIR_START=$(pwd)
for DIR_NAME in src/*; do 
    if test -d $DIR_NAME; then
        echo "=== Dir, to check cover with tests: $DIR_NAME ==="
        cd $DIR_NAME
        python3 -m coverage run -m unittest
        python3 -m coverage report
        cd $DIR_START
    fi
done


