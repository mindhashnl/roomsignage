python3 manage.py check
sh .buildkite/wait-for-it.sh db:5432 -- python3 manage.py makemigrations --check
if [[ $? == 0 ]]; then
    echo "All models are reflected in migrations"
else
    echo "ERROR: Not all models are relfected in migrations. Please run manage.py makemigrations"
    exit 1
fi