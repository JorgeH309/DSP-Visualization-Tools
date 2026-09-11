# dspviz

dspviz is a visualization tool for fundamental Digital Signal Processing techniques and concepts.

# Tool Setup

Edit dspviz.sh to include path of dspviz.py

Convert the bash script into an executable.

```sh
chmod +x dspviz.sh
```

If you do not have a folder to store executables, run the following. 

```sh
mkdir -p ~/.local/bin
```

Define this directory in your PATH environment variable. Store it in .zshrc so that it is persistent in all terminal sessions. 

```sh
echo "export PATH="$HOME/.local/bin:$PATH"" >> ~/.zshrc
source ~/.zshrc
echo $PATH
```

Copy the bash script into the directory.

```sh
cp dspviz.sh ~/.local/bin/dspviz
```

Test the newly installed command.

```sh
dspviz complex-exponential
```

