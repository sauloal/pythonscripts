DSC=$1
branch=pypeline
gituser=sauloal
gitemail=sauloal@yahoo.com.br
gitrepo=pythonscripts
gitnick=github_$gitrepo

git config --global user.name "$gituser" 2>/dev/null
git config --global user.email $gitemail 2>/dev/null
git remote add $gitnick git@github.com:$gituser/$gitrepo.git

NAME=`date --rfc-3339=seconds | tr " |,|:|\-|\+" _`

git add .

if [[ ! -z $(git ls-files --deleted) ]]; then
    git rm $(git ls-files --deleted)  2>&1 | tee -a $LOG
fi

if [[ ! -z "$DSC" ]]; then
    NAME="$NAME $DSC"
fi

git commit -am "$NAME"
git push -u $gitnick master:$branch

