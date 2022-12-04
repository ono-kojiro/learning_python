export PYENV_ROOT="$HOME/.pyenv"

echo ":$PATH:" | grep ":$PYENV_ROOT/bin:" > /dev/null 2>&1
if [ $? -ne 0 ]; then
  export PATH="$PYENV_ROOT/bin:$PATH"
fi

eval "$(pyenv init --path)"

eval "$(pyenv init -)"
