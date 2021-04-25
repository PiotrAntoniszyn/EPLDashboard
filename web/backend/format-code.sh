flake8 --ignore=[W503, ] --max-line-length=128
black app/
isort app/
mypy --disallow-untyped-calls app/

