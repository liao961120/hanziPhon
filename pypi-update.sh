# Update version
num1=`cat VERSION`
echo $(echo $num1 + 1 | bc) > VERSION

# Build package
[[ -d build/ ]] && rm -r build/ 
[[ -d build/ ]] && rm -r build/ 
[[ -d dist/ ]] && rm -r dist/
[[ -d hanziPhon.egg-info/ ]] && rm -r hanziPhon.egg-info/
python3 setup.py sdist bdist_wheel &&
twine upload dist/*
