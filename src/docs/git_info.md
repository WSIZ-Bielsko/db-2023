
## aliases

```shell
alias gRM='git rm -r --cached .'
alias g_gather_last='git reset --soft HEAD~1'
alias ga='git add -A'
alias gb='git branch'
alias gc='git commit -m'
alias gco='git checkout'
alias gf='git fetch'
alias gl='git log --oneline -n 7'
alias gpu='git pull'

```


## checking out remote branch under different name

```shell
git fetch <remote>
git checkout -b <local-branch> <remote>/<remote-branch>
```