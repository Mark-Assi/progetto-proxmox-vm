param(
    [Parameter(Mandatory=$true)]
    [string]$msg
)

git add .
git commit -m "$msg"
git push